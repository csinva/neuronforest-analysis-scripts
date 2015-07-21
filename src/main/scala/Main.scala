import java.util.{Date, Calendar}
import com.sun.jna.{Library, Native}
import main.scala.CLib.CTestJava
import main.scala.{CLib, ClibLibrary}
import org.bridj.Pointer
import org.bridj.Pointer._
import org.bridj.ann.Ptr


object Main {

  def main(args:Array[String]): Unit = {
    trait CTest extends Library {
      def helloFromC
      def arrTest(size: Int): Int
      def arrSum(@Ptr arr: Long, size: Int): Int
    }
    try {
      // Can only call methods statically

//      val ctest: CTest = Native.loadLibrary("ctest", classOf[CTest]).asInstanceOf[CTest]
//      val x:Library = Native.loadLibrary("ctest", classOf[CTest]).asInstanceOf[Library]
//      ctest.helloFromC

      val array1d = allocateInts(100)
      for(i <- 0 to 99){
        array1d(i) = i
      }
//      println(ctest.arrSum(array1d,100))
//      println(ctest.arrTest(5))
     //val ctest: ClibLibrary = Clib//Native.loadLibrary("ctest", classOf[ClibLibrary]).asInstanceOf[ClibLibrary]
      val ctest: CTestJava = Native.loadLibrary("ctest", classOf[CTestJava]).asInstanceOf[CTestJava]
      ctest.helloFromC()
//      println(CLib.arrSum(array1d,100))
      println(ctest.arrSum(Pointer.getPeer(array1d),100))


    } catch {
      case e:Throwable =>
        println("Error:\n" + e.toString)
        e.printStackTrace()
        throw e
    }
  }
}