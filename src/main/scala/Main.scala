import java.util.{Date, Calendar}
import main.scala.helloc.HelloWorld
import main.scala.jnahello.test.TestLibrary

import scala.sys.process._
import org.bridj.Pointer._
import org.bridj.Pointer
//import scala.actors.threadpool.{Callable, Future, Executors, ExecutorService}
import java.lang.Runtime
import java.util.Scanner
object Main {

  def main(args:Array[String]): Unit = {
    try {
      // Can only call methods statically
      val pairCount = TestLibrary.PAIRS_COUNT
      println("PairsCount: "+pairCount)
//      val testFunc = TestLibrary.testFunc(3)
//      println("TestFunc: "+testFunc)
      println("CTest:"+HelloWorld.test())
/*
      val uptimeProc = Runtime.getRuntime().exec("uptime")
      println(uptimeProc)
      val in = new Scanner(uptimeProc.getInputStream())
      print(in.nextLine())
      /*
      Pointer<Byte> message = pointerToCString("Message from Java");
      someCFunction(message);
      SomeClass c = new SomeClass(1234);
      int value = c.someMethod(message);
      assertEquals(1234, value);
      */
//      val test = new TestClass
//      val pTest = pointerTo(test)
      //val output = test.testVirtualAdd(3,4)
//      println("output: "+output)

      val argSettings = args.map(_.split("=")).map(arr => arr(0) -> (if(arr.length>1) arr(1) else "")).toMap
      val testOnly=argSettings.getOrElse("testOnly","false")
      val array1d = allocateFloats(100)
      for(i <- 0 to 99){
        array1d(i) = i
      }
      for(i <- 0 to 99){
        //println(array1d(i))
      }
      println("testOnly: "+testOnly)
      print("Chandan start..")
      */
    } catch {
      case e:Throwable =>
        println("Error:\n" + e.toString)
        e.printStackTrace()
        throw e
    }
  }
}