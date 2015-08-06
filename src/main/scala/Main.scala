import java.io
import java.io.{FileWriter, RandomAccessFile}
import java.nio.{FloatBuffer, ByteBuffer}
import java.util.{Date, Calendar}
import breeze.linalg.{sum, reshape, max, min}
import com.sun.jna.{Library, Native}
import main.scala._
import org.apache.spark.{SparkContext, SparkConf}
import org.apache.spark.rdd.RDD
import org.bridj.Pointer
import org.bridj.Pointer._
import org.bridj.ann.Ptr

//Tests calling MALIS from Scala
object Main {

  def main(args:Array[String]): Unit = {
    // Can only call methods statically
    trait CLibScala extends Library {
      def helloFromC
      def malisLoss(@Ptr dims: Long, @Ptr conn: Long, @Ptr nhood: Long, @Ptr seg: Long, margin: Double, pos: Boolean,
                    @Ptr losses: Long, @Ptr loss: Long, @Ptr randIndex: Long)
      def arrTest(testNum: Int)
    }

    try {

      val clibOne: CLibScala = Native.loadLibrary("/groups/turaga/home/singhc/analysis-scripts/src/main/cpp/clib.so",classOf[CLibScala]).asInstanceOf[CLibScala]
      val conf = new SparkConf().setAppName("Hello").set("spark.shuffle.spill", "false").set("spark.logConf", "true")
      conf.setMaster("local[1]")
      val sc = new SparkContext(conf)

      val clibs:RDD[Int] = sc.parallelize(List.fill(1)(3))
//      val clibs:RDD[CLibScala] = sc.parallelize(List.fill(1)(clibOne))
      println("clibs size: "+clibs.partitions.size)
      val clib: CLibScala = clibOne // clibs.first()
      clib.helloFromC
      clib.arrTest(3)
      val ss = 78



      //this makes the assumption of nearest neighbors
      val dimsList:Array[Int] =Array(ss,ss,ss,3)
      def identity(x:Int,y:Int):Double = if(x==y) 1 else 0
      val NUM = dimsList(0)*dimsList(1)*dimsList(2)
      val NUM3 = NUM*3

      //load things
      val predArr:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/testData/malis/predsArr.raw") //saved as x,y,z
      val labelArr:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/testData/malis/pointsArr.raw")  //saved as x,y,z
      val seg:Array[Float] = loadFeatures("/groups/turaga/home/singhc/analysis-scripts/testData/malis/segArr.raw") //this errors if it is lower
      val affPos:Array[Float] = min(predArr,labelArr)
      val affNeg:Array[Float] = max(predArr,labelArr)

      //inputs
      val margin:Double = .3
      val pos:Boolean = true
      val neg:Boolean = false
      val dims = allocateInts(4)
      val connPos = allocateFloats(NUM3) //should be [y,x,z,#edges]
      val connNeg = allocateFloats(NUM3) //should be [y,x,z,#edges]
      val segC = allocateInts(NUM) //should be [y,x,z]

      for(i<-0 until 4)
        dims(i)=dimsList(i)

      val nhood = allocateDoubles(dims(3)*dims(3))
      for(i<-0 until 3;j<-0 until 3)
        nhood(i*3+j)= -identity(i,j)

      //order everything in Fortran Order - todo: do this is the c++
      for(x<-0 until ss;y<-0 until ss;z<-0 until ss){
        segC(z*ss*ss + y * ss + x ) = seg(x * ss * ss + y * ss + z).toInt
        for (i <- 0 until 3) {
          connPos(i * ss * ss * ss + z * ss * ss + y * ss + x) = affPos(x * ss * ss * 3 + y * ss * 3 + z * 3 + i)
          connNeg(i * ss * ss * ss + z * ss * ss + y * ss + x) = affNeg(x * ss * ss * 3 + y * ss * 3 + z * 3 + i)
        }
      }

      //outputs
      val gradsPos = allocateFloats(NUM*3)
      val gradsNeg = allocateFloats(NUM*3)
      val lossPos = allocateDouble()
      val lossNeg = allocateDouble()
      val randIndex = allocateDouble()


      clib.malisLoss(Pointer.getPeer(dims),Pointer.getPeer(connPos),Pointer.getPeer(nhood),Pointer.getPeer(segC),
        margin,pos,Pointer.getPeer(gradsPos),Pointer.getPeer(lossPos),Pointer.getPeer(randIndex))
      println("randIndex pos:"+randIndex(0))
      clib.malisLoss(Pointer.getPeer(dims),Pointer.getPeer(connNeg),Pointer.getPeer(nhood),Pointer.getPeer(segC),
        margin,neg,Pointer.getPeer(gradsNeg),Pointer.getPeer(lossNeg),Pointer.getPeer(randIndex))
      println("randIndex neg:"+randIndex(0))

      //undo Fortran ordering
      val gradsArrPos:Array[Double]=Array.fill[Double](NUM3)(0)
      val gradsArrNeg:Array[Double]=Array.fill[Double](NUM3)(0)
      val gradsArr:Array[Double]=Array.fill[Double](NUM3)(0)

      var count=0
      for(x<-0 until ss;y<-0 until ss;z<-0 until ss;i<-0 until 3){
        gradsArrPos(count) = gradsPos(i * ss * ss * ss + z * ss * ss + y * ss + x).toDouble
        gradsArrNeg(count) = gradsNeg(i * ss * ss * ss + z * ss * ss + y * ss + x).toDouble
        gradsArr(count)=gradsArrPos(count)+gradsArrNeg(count)
        count+=1
      }
      val loss = (lossPos(0)+lossNeg(0))/(.5*NUM3*(NUM3-1)) //divide by the total number of pairs
      val grads:Array[DoubleTuple] = Array.fill[DoubleTuple](NUM)(DoubleTuple.Zero)
      for(i<-0 until NUM){
        val offset = i*3
        grads(i) = DoubleTuple(gradsArr(offset),gradsArr(offset+1),gradsArr(offset+2))
      }
      println("total loss: "+loss)

      save3D("testData/malis","lossesPos.raw",gradsArrPos,(ss,ss,ss))
      save3D("testData/malis","lossesNeg.raw",gradsArrNeg,(ss,ss,ss))
      save3D("testData/malis","losses.raw",gradsArr,(ss,ss,ss))
      save3DTuple("testData/malis","gradTuples.raw",grads,(ss,ss,ss))

    } catch {
      case e:Throwable =>
        println("Error:\n" + e.toString)
        e.printStackTrace()
        throw e
    }
  }
  def loadFeatures(path:String):Array[Float] = {
//    println("loading raw feature data: " + path)

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
  def save3DTuple(path:String, filename:String, that:Array[DoubleTuple], dims:(Int, Int, Int)): Unit = {
    println("Saving 3D: " + path + "/" + filename)
    val dir =  new io.File(path)
    if(!dir.exists) dir.mkdirs()

    val fwdims = new FileWriter(path + "/dims.txt", false)
    fwdims.write(dims._1 + " " + dims._2 + " " + dims._3)
    fwdims.close()

    val fc = new RandomAccessFile(path + "/" + filename, "rw").getChannel
    val byteBuffer = ByteBuffer.allocate(4 * 3) //must be multiple of 4 for floats
    val floatBuffer =  byteBuffer.asFloatBuffer()
    that.foreach { d3 =>
      Seq(d3._1, d3._2, d3._3).foreach(d => floatBuffer.put(d.toFloat))
      fc.write(byteBuffer)
      byteBuffer.rewind()
      floatBuffer.clear()
    }
    fc.close()
  }
}