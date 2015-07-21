package main.scala.helloc;

import com.sun.jna.Library;
import com.sun.jna.Native;

/**
 * Created by singhc on 7/21/15.
 */
/* HelloWorld.java */

public class HelloWorld {
    public interface CTest extends Library {
        public void helloFromC();
    }
    public static void main(String argv[]) {
        System.out.println("TEST");
        CTest ctest = (CTest) Native.loadLibrary("ctest", CTest.class);
        ctest.helloFromC();
    }
    public static int test(){
        CTest ctest = (CTest) Native.loadLibrary("ctest", CTest.class);
        ctest.helloFromC();
        return 0;
    }
}
