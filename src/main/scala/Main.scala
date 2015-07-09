import java.io
import java.io._
import java.text.SimpleDateFormat
import java.util.{Date, Calendar}


//import scala.actors.threadpool.{Callable, Future, Executors, ExecutorService}

object Main {

  def main(args:Array[String]): Unit = {
    try {
      val argSettings = args.map(_.split("=")).map(arr => arr(0) -> (if(arr.length>1) arr(1) else "")).toMap
      val testOnly=argSettings.getOrElse("testOnly","false")
      println("testOnly: "+testOnly)
      print("Chandan start..")
    } catch {
      case e:Throwable =>
        println("Error:\n" + e.toString)
        e.printStackTrace()
        throw e
    }
  }
}