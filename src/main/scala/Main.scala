import java.util.{Date, Calendar}
import com.sun.jna.{Library, Native}
import org.bridj.Pointer._


object Main {

  def main(args:Array[String]): Unit = {
    trait CTest extends Library {
      def helloFromC
      def arrTest(size: Int): Int
      //def arrSum(x: Pointer[Integer], size: Int): Int
    }
    try {
      // Can only call methods statically
      val ctest: CTest = Native.loadLibrary("ctest", classOf[CTest]).asInstanceOf[CTest]
      ctest.helloFromC

      val array1d = allocateInts(100)
      for(i <- 0 to 99){
        array1d(i) = i
      }
      //println(ctest.arrSum(array1d,100))
      println(ctest.arrTest(5))

      val argSettings = args.map(_.split("=")).map(arr => arr(0) -> (if(arr.length>1) arr(1) else "")).toMap
      val testOnly=argSettings.getOrElse("testOnly","false")


      for(i <- 0 to 99){
        //println(array1d(i))
      }

    } catch {
      case e:Throwable =>
        println("Error:\n" + e.toString)
        e.printStackTrace()
        throw e
    }
  }
}