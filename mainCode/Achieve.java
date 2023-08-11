import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;

public  class Achieve implements tools {

    private static final int ELECTRICITY = 10;
    private static final int WATER = 8;
    private static final double ELE_PRICE = 0.2;
    private static final double WATER_PRICE = 0.2;
    String fileName;

    //    通过名字查询
    @Override
    public ArrayList<String> QueryByName(String str, String name) throws IOException {
        if (str.equals("学生")) {
            fileName = Student.studentFile;
        } else {
            fileName = Teacher.teacherFile;
        }
        File file = new File(fileName);
        FileInputStream is = new FileInputStream(file);
        InputStreamReader dis = new InputStreamReader(is, StandardCharsets.UTF_8);
        BufferedReader br = new BufferedReader(dis);
        String msg;
        ArrayList<String> names = new ArrayList<>();
        while ((msg = br.readLine()) != null) {
            int pos = msg.indexOf("姓名：");
            int end = msg.indexOf(",", pos);
            if (end == -1) end = msg.length();

            String studentName = msg.substring(pos + 3, end);
            if (name.equals(studentName)) {
                names.add(msg);
            }
        }
        return names;
    }

    //    通过用电量查询
    @Override
    public ArrayList<String> QueryByElectricity(String str, double electricity) throws IOException {

        if (str.equals("学生")) {
            fileName = Student.studentFile;
        } else {
            fileName = Teacher.teacherFile;
        }
        File file = new File(fileName);
        FileInputStream is = new FileInputStream(file);
        InputStreamReader dis = new InputStreamReader(is, StandardCharsets.UTF_8);
        BufferedReader br = new BufferedReader(dis);
        String msg;
        ArrayList<String> ele = new ArrayList<>();
        while (true) {
            msg = br.readLine();
            if (msg == null) break;
            int pos = msg.indexOf("用电量：");
            int end = msg.indexOf(",", pos);
            if (end == -1) {
                end = msg.length();
            }
            double studentElectricity = Double.parseDouble(msg.substring(pos + 4, end));
            if (electricity <= studentElectricity) {
                ele.add(msg);
            }
        }
        return ele;
    }

    //通过用水量查询
    @Override
    public ArrayList<String> QueryByWater(String str, double water) throws IOException {
        if (str.equals("学生")) {
            fileName =Student.studentFile;
        } else {
            fileName = Teacher.teacherFile;
        }
        File file = new File(fileName);
        FileInputStream is = new FileInputStream(file);
        InputStreamReader dis = new InputStreamReader(is, StandardCharsets.UTF_8);
        BufferedReader br = new BufferedReader(dis);

        ArrayList<String> ele = new ArrayList<>();
        while (true) {
            String msg = br.readLine();
            if (msg == null) break;

            int pos = msg.indexOf("用水量：");
            int end = msg.indexOf(",", pos);
            if (end == -1) {
                end = msg.length();
            }
            double studentWater = Double.parseDouble(msg.substring(pos + 4, end));
            if (water <= studentWater) {
                ele.add(msg);
            }
        }
        is.close();
        dis.close();
        br.close();
        return ele;
    }

    @Override
    public ArrayList<String> QueryByUnit(String unit) throws IOException {
        ArrayList<String> result = new ArrayList<>();
        String str = show();
        String[] split = str.split("\n");
        for(String s : split) {
            if(s.contains("部门：" + unit + ",")||s.contains("班级：" + unit +",")) {
                result.add(s + "\n");
            }
        }
        return result;
    }

    @Override
    public ArrayList<String> QueryById(int id) throws IOException {
        ArrayList<String> result = new ArrayList<>();
        String str = show();
        String[] split = str.split("\n");
        for(String s : split) {
            if(s.contains("职工号：" + id +",")||s.contains("学号：" + id +",")) {
                result.add(s + "\n");
            }
        }
        return result;

    }

    //读取文件中的信息
    @Override
    public String read(String fileName) throws IOException {
        File file = new File(fileName);
        FileInputStream is = new FileInputStream(file);
        InputStreamReader dis = new InputStreamReader(is, StandardCharsets.UTF_8);
        BufferedReader br = new BufferedReader(dis);
        String msg;
        StringBuilder sb = new StringBuilder();
        while ((msg = br.readLine()) != null) {
            sb.append(msg).append("\n");
        }
        return sb.toString();
    }

    // 展示学生和教工的信息
    @Override
    public String show() throws IOException {

        return read(Student.studentFile) + "\n" +
                read(Teacher.teacherFile) + "\n";
    }

    //修改信息
    @Override
    public String modify(String s,String op,String end)  {
        int pos = s.indexOf(op);
        int endPos = s.indexOf(",",pos);
        if (endPos == -1){
            endPos = s.length();
        }
        String temp = s.substring(pos + op.length() + 1, endPos);
        return s.replace(temp,end);
    }

    // 删除信息
    @Override
    public void delete(String ob, int id) throws IOException {
        String idName;
        if (ob.equals("学生")) {
            idName = "学号：";
            fileName = Student.studentFile;
        } else if (ob.equals("教工")) {
            idName = "职工号：";
            fileName = Teacher.teacherFile;
        } else {
            System.out.println("error");
            return;
        }
        File file = new File(fileName);
        FileInputStream is = new FileInputStream(file);
        InputStreamReader isr = new InputStreamReader(is);
        BufferedReader br = new BufferedReader(isr);
        String line;
        String msg = null;
        StringBuilder sb = new StringBuilder();
        while ((line = br.readLine()) != null) {
            String s = line.substring(line.indexOf(idName) + idName.length(), line.indexOf(",", line.indexOf(idName)));
            if (!s.equals(String.valueOf(id))) {
                sb.append(line).append("\n");
            } else {
                msg = line;
            }
        }
        if (msg == null) {
            System.out.println("没有此人");
            return;
        }
        isr.close();
        br.close();
        is.close();
        //        FileOutputStream fos = new FileOutputStream(file);
        FileWriter fw = new FileWriter(file);
        BufferedWriter bw = new BufferedWriter(fw);
        bw.write(sb.toString());
        bw.close();
        fw.close();
    }

    //    返回未缴费的信息
    @Override
    public String isFinished() throws IOException {
        StringBuilder sbStudent = queryNotFinished(Student.studentFile);
        StringBuilder sbTeacher = queryNotFinished(Teacher.teacherFile);
        return sbStudent + sbTeacher.toString() + "\n";
    }

    //    查询用水量
    @Override
    public String calculate(String ob, int id) throws IOException {
        String idName;
        if (ob.equals("学生")) {
            idName = "学号：";
            this.fileName = Student.studentFile;
        } else {
            idName = "职工号：";
            this.fileName = Teacher.teacherFile;
        }
        StringBuilder sb = new StringBuilder();
        File file = new File(this.fileName);
        FileInputStream fis = new FileInputStream(file);
        InputStreamReader isr = new InputStreamReader(fis);
        BufferedReader br = new BufferedReader(isr);
        String line;
        double total = 0;

        while ((line = br.readLine()) != null) {
            if (line.contains(idName + id + ",")) {
                int pos = line.indexOf("用电量：");
                double electricity = Double.parseDouble(line.substring(pos + 4, line.indexOf(",", pos)));
                sb.append("用电量：").append(electricity).append("\n");
                pos = line.indexOf("用水量：");
                int end = line.indexOf(",", pos);
                if (end == -1) {
                    end = line.length();
                }
                double water = Double.parseDouble(line.substring(pos + 4, end));
                sb.append("用水量：").append(water).append("\n");
                if (electricity >= ELECTRICITY && water >= WATER) {
                    total = (electricity - ELECTRICITY) * ELE_PRICE + (water - WATER) * WATER_PRICE;
                } else if (electricity >= ELECTRICITY && water <= WATER) {
                    total = (electricity - ELECTRICITY) * ELE_PRICE;
                } else if (electricity <= ELECTRICITY && water >= WATER) {
                    total = (water - WATER) * WATER_PRICE;
                }
                sb.append("总费用：").append(String.format("%.2f",total)).append("\n");

                if (line.contains("是否缴费：是")) {
                    sb.append("是否缴费：是").append("\n");
                    sb.append("应付金额：0").append("\n");
                } else {
                    sb.append("是否缴费：否").append("\n");
                    sb.append("应付金额：").append(String.format("%.2f",total)).append("\n");
                }
                br.close();
                isr.close();
                fis.close();
                return sb.toString();
            }
        }
        br.close();
        isr.close();
        fis.close();
        return "没有此人";
    }

    @Override
    public double electricity(String fileName) throws IOException {
        File file = new File(fileName);
        FileReader reader = new FileReader(file);
        BufferedReader br = new BufferedReader(reader);
        String line;
        double total = 0;
        while ((line = br.readLine()) != null) {
            int beg = line.indexOf("用电量：");
            int end = line.indexOf(",", beg);
            double sum = Double.parseDouble(line.substring(beg + "用电量：".length(), end));
            if (sum >= ELECTRICITY && line.contains("是否缴费：否")) total += (sum - ELECTRICITY);

        }
        reader.close();
        br.close();
        return total * ELE_PRICE;
    }

    @Override
    public double water(String fileName) throws IOException {
        File file = new File(fileName);
        FileReader reader = new FileReader(file);
        BufferedReader br = new BufferedReader(reader);
        String line;
        double total = 0;
        while ((line = br.readLine()) != null) {
            int beg = line.indexOf("用水量：");
            int end = line.indexOf(",", beg);
            double sum = Double.parseDouble(line.substring(beg + "用水量：".length(), end));
            if (sum >= WATER && line.contains("是否缴费：否")) total += (sum - WATER) ;
        }
        reader.close();
        br.close();
        return total* WATER_PRICE;
    }

    private StringBuilder queryNotFinished(String fileName) throws IOException {
        File file = new File(fileName);
        FileInputStream fis = new FileInputStream(file);
        InputStreamReader isr = new InputStreamReader(fis);
        BufferedReader br = new BufferedReader(isr);
        String line;
        StringBuilder sb = new StringBuilder();
        while ((line = br.readLine()) != null) {
            int pos = line.indexOf("是否缴费：");
            int end = line.indexOf(",", pos);
            if (end == -1) {
                end = line.length();
            }
            String is = line.substring(pos + 5, end);
            if (is.equals("否")) {
                sb.append(line).append('\n');
            }
        }
        fis.close();
        br.close();
        isr.close();
        return sb;
    }
    public static double[] getNumber() throws IOException {
        double [] num= new double[2];
        String content = new Achieve().read(Student.studentFile);
        num[0] = content.split("\n").length;
        num[1] = new Achieve().read(Teacher.teacherFile).split("\n").length;
        return num;
    }
}