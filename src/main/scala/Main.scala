import java.io
import java.io.{FileWriter, RandomAccessFile}
import java.nio.{FloatBuffer, ByteBuffer}
import java.util.{Date, Calendar}
import breeze.linalg.{sum, reshape, max, min}
import com.sun.jna.{Library, Native}
import main.scala.CLib.CTestJava
import main.scala.{DoubleTuple, CLib, ClibLibrary}
import org.bridj.Pointer
import org.bridj.Pointer._
import org.bridj.ann.Ptr


object Main {

  def main(args:Array[String]): Unit = {
    // Can only call methods statically
    trait CLibScala extends Library {
      def helloFromC
      def arrTest(size: Int): Int
      def arrDouble(@Ptr arr: Long,@Ptr arr2: Long, size: Int): Int
      def malisLoss(@Ptr dims: Long, @Ptr conn: Long, @Ptr nhood: Long, @Ptr seg: Long, margin: Double, pos: Boolean,
                    @Ptr losses: Long, @Ptr loss: Long, @Ptr classErr: Long, @Ptr randIndex: Long)
    }
    try {
      val ss = 78
      //this makes the assumption of nearest neighbors
      val dimsList:Array[Int] =Array(ss,ss,ss,3)
      def identity(x:Int,y:Int):Double = if(x==y) 1 else 0
      val NUM = dimsList(0)*dimsList(1)*dimsList(2)

      //load things
      var predArr:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/malis/001/predsArr.raw") //saved as x,y,z
      val labelArr:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/malis/001/pointsArr.raw")  //saved as x,y,z
      val seg:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/malis/001/segArr.raw") //this errors if it is lower
      val affPos:Array[Float] = min(predArr,labelArr)
      val affNeg:Array[Float] = max(predArr,labelArr)

      //inputs - todo: make these assignments all done with map
      val margin:Double = .3
      val pos:Boolean = true
      val neg:Boolean = false
      val dims = allocateInts(4)
      val conn = allocateFloats(NUM*3) //should be [y,x,z,#edges]
      val connArr = Array.ofDim[Float](ss,ss,ss,3)
      val segC = allocateInts(NUM) //should be [y,x,z]

      for(i<-0 until 4)
        dims(i)=dimsList(i)

      val nhood = allocateDoubles(dims(3)*dims(3))
      for(i<-0 until 3)
        for(j<-0 until 3)
          nhood(i*3+j)= -identity(i,j)

      //order everything in Fortran Order
      for(x<-0 until ss)
        for(y<-0 until ss)
          for(z<-0 until ss)
            for (i <- 0 until 3)
              conn(i * ss * ss * ss + z * ss * ss + y * ss + x) = affPos(x * ss * ss * 3 + y * ss * 3 + z * 3 + i)
      for(x<-0 until ss)
        for(y<-0 until ss)
          for(z<-0 until ss)
            segC(z*ss*ss + y * ss + x ) = seg(x * ss * ss + y * ss + z).toInt

      //outputs
      val lossesPos = allocateFloats(NUM*3)
      val lossesNeg = allocateFloats(NUM*3)
      val loss = allocateDouble()
      val classErr = allocateDouble()
      val randIndex = allocateDouble()


      val ctest: CLibScala = Native.loadLibrary("ctest", classOf[CLibScala]).asInstanceOf[CLibScala]
      ctest.helloFromC
      ctest.malisLoss(Pointer.getPeer(dims),Pointer.getPeer(conn),Pointer.getPeer(nhood),Pointer.getPeer(segC),
        margin,pos,Pointer.getPeer(lossesPos),Pointer.getPeer(loss),Pointer.getPeer(classErr),Pointer.getPeer(randIndex))
      ctest.malisLoss(Pointer.getPeer(dims),Pointer.getPeer(conn),Pointer.getPeer(nhood),Pointer.getPeer(segC),
        margin,neg,Pointer.getPeer(lossesNeg),Pointer.getPeer(loss),Pointer.getPeer(classErr),Pointer.getPeer(randIndex))

      val lossArrPos:Array[Double]=Array.fill[Double](NUM*3)(0)
      val lossArrNeg:Array[Double]=Array.fill[Double](NUM*3)(0)
      for(x<-0 until ss)
        for(y<-0 until ss)
          for(z<-0 until ss)
            for(i<-0 until 3) {
              lossArrPos(x * ss * ss * 3 + y * ss * 3 + z * 3 + i) = lossesPos(i * ss * ss * ss + z * ss * ss + y * ss + x).toDouble
              lossArrNeg(x * ss * ss * 3 + y * ss * 3 + z * 3 + i) = lossesNeg(i * ss * ss * ss + z * ss * ss + y * ss + x).toDouble
            }

      println("randIndex:"+randIndex(0))
      save3D("malis/001","lossesPos.raw",lossArrPos,(ss,ss,ss))
      save3D("malis/001","lossesNeg.raw",lossArrNeg,(ss,ss,ss))

    } catch {
      case e:Throwable =>
        println("Error:\n" + e.toString)
        e.printStackTrace()
        throw e
    }
  }
  def loadFeatures(path:String):Array[Float] = {
    println("loading raw feature data: " + path)

    val file = new RandomAccessFile(path, "r")
    val fileChannel = file.getChannel

    val byteBuffer = ByteBuffer.allocate(4 * 10000) //must be multiple of 4 for floats
    val outFloatBuffer = FloatBuffer.allocate((fileChannel.size/4).toInt)

    var bytesRead = fileChannel.read(byteBuffer)
    while(bytesRead > 0) {
      byteBuffer.flip()
      outFloatBuffer.put(byteBuffer.asFloatBuffer())
      byteBuffer.clear()
      bytesRead = fileChannel.read(byteBuffer)
    }

    outFloatBuffer.array()
  }
  def save3D(path:String, filename:String, that:Array[Double], dims:(Int, Int, Int)): Unit = {
    println("Saving 3D: " + path + "/" + filename)
    val dir =  new io.File(path)
    if(!dir.exists) dir.mkdirs()

    val fwdims = new FileWriter(path + "/dims.txt", false)
    fwdims.write(dims._1 + " " + dims._2 + " " + dims._3)
    fwdims.close()

    val fc = new RandomAccessFile(path + "/" + filename, "rw").getChannel
    val byteBuffer = ByteBuffer.allocate(4 * 1) //must be multiple of 4 for floats
    val floatBuffer =  byteBuffer.asFloatBuffer()
    that.foreach { d =>
      floatBuffer.put(d.toFloat)
      fc.write(byteBuffer)
      byteBuffer.rewind()
      floatBuffer.clear()
    }
    fc.close()
  }
}