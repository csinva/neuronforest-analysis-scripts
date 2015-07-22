import java.util.{Date, Calendar}
import com.sun.jna.{Library, Native}
import main.scala.CLib.CTestJava
import main.scala.{CLib, ClibLibrary}
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
      def malisLoss(@Ptr dims: Long, @Ptr conn: Long, @Ptr nhood: Long, @Ptr seg: Long, margin: Double, pos: Boolean, @Ptr losses: Long, loss: Double, classErr: Double, randIndex: Double)
    }
    try {
      val dimsList:Array[Int] =Array(4,4,4,3)
      val NUM = dimsList(0)*dimsList(1)*dimsList(2)
      //inputs
      val dims = allocateInts(4)
      for(i<-0 until 4){dims(i)=dimsList(i)}
      val conn = allocateFloats(NUM) //needs dims
      val nhood = allocateDoubles(3)
      val seg = allocateInts(NUM)
      val margin:Double = .3
      val pos:Boolean = true
      //outputs
      val losses = allocateFloats(NUM)
      val loss:Double = 0
      val classErr:Double = 0
      val randIndex:Double = 0

      for(i <- 0 until NUM){
        conn(i) = i
        seg(i) = i
      }
      val ctest: CLibScala = Native.loadLibrary("ctest", classOf[CLibScala]).asInstanceOf[CLibScala]
      ctest.helloFromC
      println(ctest.arrDouble(Pointer.getPeer(seg),Pointer.getPeer(seg),NUM))
      ctest.malisLoss(Pointer.getPeer(dims),Pointer.getPeer(conn),Pointer.getPeer(nhood),Pointer.getPeer(seg),margin,pos,Pointer.getPeer(losses),loss,classErr,randIndex)
      //      println(ctest.arrSum(array1d,100))
//      println(ctest.arrTest(5))
     //val ctest: ClibLibrary = Clib//Native.loadLibrary("ctest", classOf[ClibLibrary]).asInstanceOf[ClibLibrary]


    } catch {
      case e:Throwable =>
        println("Error:\n" + e.toString)
        e.printStackTrace()
        throw e
    }
  }
}