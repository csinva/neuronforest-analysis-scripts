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
    }
    try {
      val NUM = 100
      //inputs
      val conn = allocateFloats(NUM) //needs dims
      val nhood = allocateDoubles(9) //needs dims
      val seg = allocateInts(NUM)
      val margin:Double = .3
      val pos:Boolean = true
      //outputs
      val losses = allocateFloats(NUM)
      val loss:Double = 0
      val classErr:Double = 0
      val randIndex:Double = 0

      val testArr = allocateInts(NUM)

      for(i <- 0 until NUM){
        conn(i) = i
        seg(i) = i
      }
      val ctest: CLibScala = Native.loadLibrary("ctest", classOf[CLibScala]).asInstanceOf[CLibScala]
      ctest.helloFromC
      println(ctest.arrDouble(Pointer.getPeer(seg),Pointer.getPeer(testArr),NUM))
      for(i <- 0 until NUM){
        print(testArr(i)+" ")
      }

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