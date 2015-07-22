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
      def malisLoss(@Ptr dims: Long, @Ptr conn: Long, @Ptr nhood: Long, @Ptr seg: Long, margin: Double, pos: Boolean,
                    @Ptr losses: Long, @Ptr loss: Long, @Ptr classErr: Long, @Ptr randIndex: Long)
    }
    try {
      def identity(x:Int,y:Int): Double =if(x==y) 1 else 0
//      print(identity(1,1))
      val dimsList:Array[Int] =Array(4,4,4,3)
      val NUM = dimsList(0)*dimsList(1)*dimsList(2)
      //inputs
      val dims = allocateInts(4)
      for(i<-0 until 4){dims(i)=dimsList(i)}
      val conn = allocateFloats(NUM)

      val nhood = allocateDoubles(dims(3)*dims(3))

      for(i<-0 until 3){
        for(j<-0 until 3){
          //nhood(i*3+j)=identity(i,j)
        }
      }

      val seg = allocateInts(NUM)
      val margin:Double = .3
      val pos:Boolean = true

      //outputs
      val losses = allocateFloats(NUM)
      val loss = allocateDouble()
      val classErr = allocateDouble()
      val randIndex = allocateDouble()
      val ctest: CLibScala = Native.loadLibrary("ctest", classOf[CLibScala]).asInstanceOf[CLibScala]
      ctest.helloFromC
//      println(ctest.arrDouble(Pointer.getPeer(seg),Pointer.getPeer(seg),NUM))
      ctest.malisLoss(Pointer.getPeer(dims),Pointer.getPeer(conn),Pointer.getPeer(nhood),Pointer.getPeer(seg),
        margin,pos,Pointer.getPeer(losses),Pointer.getPeer(loss),Pointer.getPeer(classErr),Pointer.getPeer(randIndex))
//      println("randIndex:"+randIndex(0))
     //val ctest: ClibLibrary = Clib//Native.loadLibrary("ctest", classOf[ClibLibrary]).asInstanceOf[ClibLibrary]


    } catch {
      case e:Throwable =>
        println("Error:\n" + e.toString)
        e.printStackTrace()
        throw e
    }
  }
}