import javax.swing.*;
import java.io.*;
import java.nio.charset.StandardCharsets;

public  class Student implements add {
    static final String studentFile = "student.txt";
    boolean finished = false;
    String is;
    int id, age;//学号
    String name, sex, group;
    double electricity, water;

    Student(String name, String sex, int age, int id, String group, double electricity, double water) {
        this.name = name;
        this.sex = sex;
        this.age = age;
        this.id = id;
        this.group = group;
        this.electricity = electricity;
        this.water = water;
    }


    public void setFinished(boolean finished) {
        this.finished = finished;
    }



    @Override
    public String toString() {
        if (finished) is = "是";
        else is = "否";
        return "学号：" + id +
                ", 姓名：" + name +
                ", 性别：" + sex +
                ", 年龄：" + age +
                ", 班级：" + group +
                ", 用电量：" + electricity +
                ", 用水量：" + water +
                ", 是否缴费：" + is + "\n";
    }

    @Override
    public boolean add_message() throws IOException {

        File file = new File(studentFile);
        FileInputStream in = new FileInputStream(file);
        InputStreamReader is = new InputStreamReader(in);
        BufferedReader br = new BufferedReader(is);
        String content;
        while ((content = br.readLine()) != null) {
            if (content.contains("学号：" + this.id + ",")) {
                //                学号存在
                return false;
            }
        }
        in.close();
        is.close();
        br.close();

        int result = JOptionPane.showConfirmDialog(null,this.toString(),"请确认信息是否正确",JOptionPane.YES_NO_OPTION);
        if(!(result  == JOptionPane.YES_OPTION)){
            return true;
        }
        FileOutputStream fos = new FileOutputStream(file, true);
        try (OutputStreamWriter osw = new OutputStreamWriter(fos, StandardCharsets.UTF_8)) {
            osw.write(this.toString());
            osw.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        fos.close();
        return true;
    }

}
