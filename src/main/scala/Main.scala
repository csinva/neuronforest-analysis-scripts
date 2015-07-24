import java.io.RandomAccessFile
import java.nio.{FloatBuffer, ByteBuffer}
import java.util.{Date, Calendar}
import breeze.linalg.min
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
      val ss = 65
      //this makes the assumption of nearest neighbors
      val dimsList:Array[Int] =Array(ss,ss,ss,3)
      def identity(x:Int,y:Int):Double = if(x==y) 1 else 0
      val NUM = dimsList(0)*dimsList(1)*dimsList(2)

      //load things
      val seg:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/malis/000/segs.raw") //this errors if it is lower
      val predArrInit:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/malis/000/predsArr.raw") //saved as y,x,z
      val predArr:Array[Float] = Array.fill[Float](predArrInit.size)(0)
      for(x<-0 until ss)
        for(y<-0 until ss)
          for(z<-0 until ss)
            for(i<-0 until 3)
              predArr(x*ss*ss*3+y*ss*3+z*3+i)=predArrInit(y*ss*ss*3+x*ss*3+z*3+i)
      val labelArr:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/malis/000/points.raw")  //saved as x,y,z
      println("len:"+predArr.size)
      println("sum:"+predArr.sum)
      println("len:"+labelArr.size)
      println("sum:"+labelArr.sum)
      //val predTuples:Array[DoubleTuple] = pointsAndPreds.map(_._2)
      //val predArr:Array[Double] = predTuples.flatMap(x=>List(x._2,x._1,x._3))

      //inputs - todo: make these assignments all done with map
      val dims = allocateInts(4)
      for(i<-0 until 4){dims(i)=dimsList(i)}

      val conn = allocateFloats(NUM*3) //should be [y,x,z,#edges]
//      for(i<-0 until NUM*3) conn(i) = predArr(i)
      for(x<-0 until ss)
        for(y<-0 until ss)
          for(z<-0 until ss)
            for(i<-0 until 3)
              conn(x+y*ss+z*ss*ss+i*3*ss*ss)=predArr(x*ss*ss*3+y*ss*3+z*3+i)

      val segC = allocateInts(NUM) //should be [y,x,z]
      for(x<-0 until ss)
        for(y<-0 until ss)
          for(z<-0 until ss)
            segC(x+y*ss+z*ss*ss) = seg(y*ss*ss+x*ss+z).toInt
      /*
      for(x<-0 until ss)
        for(y<-0 until ss)
          for(z<-0 until ss)
            for(i<-0 until 3)
              predArr(x*ss*ss*3+y*ss*3+z*3+i)=predArr(y*ss*ss*3+x*ss*3+z*3+i)
              */
      for(i<-0 until 100) print(conn(i)+" ")
//      predArr = min(predArr,labelArr)
      println()

      val nhood = allocateDoubles(dims(3)*dims(3))

      for(i<-0 until 3)
        for(j<-0 until 3)
          nhood(i*3+j)= identity(i,j)



      val margin:Double = .3
      val pos:Boolean = false

      //outputs
      val losses = allocateFloats(NUM)
      val loss = allocateDouble()
      val classErr = allocateDouble()
      val randIndex = allocateDouble()
      val ctest: CLibScala = Native.loadLibrary("ctest", classOf[CLibScala]).asInstanceOf[CLibScala]
      ctest.helloFromC
//      println(ctest.arrDouble(Pointer.getPeer(seg),Pointer.getPeer(seg),NUM))
      ctest.malisLoss(Pointer.getPeer(dims),Pointer.getPeer(conn),Pointer.getPeer(nhood),Pointer.getPeer(segC),
        margin,pos,Pointer.getPeer(losses),Pointer.getPeer(loss),Pointer.getPeer(classErr),Pointer.getPeer(randIndex))
      println("randIndex:"+randIndex(0))
     //val ctest: ClibLibrary = Clib//Native.loadLibrary("ctest", classOf[ClibLibrary]).asInstanceOf[ClibLibrary]


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
}