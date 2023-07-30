import java.io.IOException;
import java.util.ArrayList;

public  interface tools {
    ArrayList<String> QueryByName(String str, String name) throws IOException;

    ArrayList<String> QueryByElectricity(String str, double electricity) throws IOException;

    ArrayList<String> QueryByWater(String str, double water) throws IOException;
    ArrayList<String> QueryByUnit(String unit) throws IOException;
    ArrayList<String> QueryById(int id) throws IOException;

    String read(String fileName) throws IOException;

    String show() throws IOException;

    String modify( String s,String op,String end) ;

    void delete(String ob, int id) throws IOException;
    String isFinished() throws IOException;
    String  calculate(String ob, int id) throws IOException;

    double electricity(String fileName) throws IOException;
    double water(String fileName) throws IOException;

}

