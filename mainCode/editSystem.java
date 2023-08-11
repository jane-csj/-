import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.plaf.basic.BasicButtonUI;
import javax.swing.text.AbstractDocument;
import java.awt.*;
import java.awt.event.*;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.nio.charset.StandardCharsets;
import java.util.Objects;

public  class editSystem implements ActionListener, ItemListener, KeyListener, DocumentListener {
    private final String[] idName = {"学生", "教工"};
    private final String[] Sex = {"男", "女"};
    private final String[] finish = {"是", "否"};
    private final String[] stuSelection = {"班级", "姓名", "年龄", "性别", "是否缴费", "用电量", "用水量"};
    private final double weighty = 0.1;
    private JLabel idLab;
    private JTextPane tp;
    private JButton add, deleted, modify, sure, selected, send;
    private JTextField tf, nameTF, ageTF, electricityTF, waterTF, modifyTF;
    private JPanel p;
    private JPanel panelRight;
    private JComboBox<String> comboBox, comboBoxSex, comboBoxFinish, comSelect;
    private CardLayout card;
    private JLabel groupLabel, modifyIdLabel;
    private JTextField groupTF;
    private JComboBox<String> modifyCom;
    private JTextField modifyIdTF;
    private DefaultComboBoxModel<String> model;

    public void createUI() {
        Font font = new Font("宋体", Font.BOLD, 16);
        //        左半部分
        JPanel panelLeft = new JPanel();
        panelLeft.setLayout(new GridLayout(5, 1,0,30));
        add = new JButton("添加");
        modify = new JButton("修改");
        deleted = new JButton("删除");
        add.setUI(new BasicButtonUI());
        modify.setUI(new BasicButtonUI());
        deleted.setUI(new BasicButtonUI());
        add.addActionListener(this);
        modify.addActionListener(this);
        deleted.addActionListener(this);
        panelLeft.add(new JPanel());
        panelLeft.add(add);
        panelLeft.add(modify);
        panelLeft.add(deleted);

        //        右半部分，使用卡片布局
        panelRight = new JPanel();
        card = new CardLayout();
        panelRight.setLayout(card);

        //      添加部分的布局
        JPanel panelTemp = new JPanel();
        panelTemp.setLayout(new GridBagLayout());
        p = new JPanel();
        p.setLayout(new GridBagLayout());

        //        右半部分上面的面板
        tp = new JTextPane();
        tp.setText("请认真填写要添加的信息，请勿留空。");
        tp.setFont(new Font("宋体", Font.BOLD, 12));
        tp.setEditable(false);


        //        单位
        JLabel label = new JLabel("单位");
        label.setFont(font);
        GridBagConstraints gc = new GridBagConstraints();
        gc.gridx = 0;
        gc.gridy = 0;
        gc.weightx = 0.3;
        gc.weighty = 0.2;
        p.add(label, gc);
        comboBox = new JComboBox<>(idName);
        comboBox.setFont(font);
        comboBox.addItemListener(this);
        GridBagConstraints gc1 = new GridBagConstraints();
        gc1.gridx = 2;
        gc1.gridy = 0;
        gc1.weightx = 0.7;
        gc1.weighty = weighty;
        gc1.fill = GridBagConstraints.HORIZONTAL;
        gc1.insets = new Insets(0, 0, 0, 200);
        p.add(comboBox, gc1);


        //        学号
        idLab = new JLabel("学号");
        idLab.setFont(font);
        GridBagConstraints gc2 = constraints(0, 1, 0.3, weighty);
        tf = new JTextField();
        tf.setFont(font);
        GridBagConstraints gcTf = constraints(2, 1, 0.7, weighty);
        gcTf.insets = new Insets(15, 0, 0, 200);
        gcTf.fill = GridBagConstraints.HORIZONTAL;
        p.add(idLab, gc2);
        p.add(tf, gcTf);

        //        姓名
        nameTF = newLabel("姓名", 2);

        //        性别
        comboBoxSex = newSex();
        comboBoxSex.addItemListener(this);
        //        年龄
        ageTF = newLabel("年龄", 4);

        //        班级
        groupLabel = new JLabel("班级");
        groupLabel.setFont(font);
        GridBagConstraints gc3 = constraints(0, 5, 0.3, weighty);
        groupTF = new JTextField();
        groupTF.setFont(font);
        GridBagConstraints gcGroup = constraints(2, 5, 0.7, weighty);
        gcGroup.insets = new Insets(15, 0, 0, 200);
        gcGroup.fill = GridBagConstraints.HORIZONTAL;
        p.add(groupLabel, gc3);
        p.add(groupTF, gcGroup);

        //        用电量
        electricityTF = newLabel("用电量", 6);
        //        用水量
        waterTF = newLabel("用水量", 7);
        //        为输入添加键盘监听
        addListener();
        //        缴费
        JLabel finishLabel = new JLabel("是否缴费");
        finishLabel.setFont(font);
        GridBagConstraints gcFinish = constraints(0, 8, 0.3, weighty);
        p.add(finishLabel, gcFinish);
        comboBoxFinish = new JComboBox<>(finish);
        comboBoxFinish.setFont(font);
        comboBoxFinish.addItemListener(this);
        GridBagConstraints gcCombo = constraints(2, 8, 0.7, weighty);
        gcCombo.fill = GridBagConstraints.HORIZONTAL;
        gcCombo.insets = new Insets(15, 0, 0, 200);
        p.add(comboBoxFinish, gcCombo);

        //        添加按钮
        sure = new JButton("添加");
        sure.setFont(font);
        sure.addActionListener(this);
        GridBagConstraints gcSure = constraints(1, 10, 1, weighty);
        p.add(sure, gcSure);

        GridBagConstraints gcTP = constraints(0, 0, 1, 0.2);
        gcTP.fill = GridBagConstraints.HORIZONTAL;

        GridBagConstraints gcP = constraints(0, 1, 1, 0.8);
        gcP.fill = GridBagConstraints.HORIZONTAL;

        panelTemp.add(tp, gcTP);
        panelTemp.add(p, gcP);

        init();
        //        添加功能
        panelRight.add("add", panelTemp);

        //        删除功能
        JPanel deletePanel = new deleteUI().createDeletedUI();
        panelRight.add("delete", deletePanel);

        //        修改功能
        JPanel modifyPanel = modifyPanel();
        panelRight.add("modify", modifyPanel);

        myFrame frame = new myFrame();
        JFrame fr = frame.createFrame("编辑系统", panelLeft, panelRight);

        fr.setVisible(true);

    }

    //    性别选择
    private JComboBox<String> newSex() {
        JLabel label = new JLabel("性别");
        label.setFont(new Font("宋体", Font.BOLD, 16));
        GridBagConstraints gcLab = constraints(0, 3, 0.3, weighty);
        p.add(label, gcLab);
        JComboBox<String> cb = new JComboBox<>(Sex);
        cb.setFont(new Font("宋体", Font.BOLD, 16));
        GridBagConstraints gc1 = new GridBagConstraints();
        gc1.gridx = 2;
        gc1.gridy = 3;
        gc1.weightx = 0.7;
        gc1.weighty = weighty;
        gc1.fill = GridBagConstraints.HORIZONTAL;
        gc1.insets = new Insets(15, 0, 0, 200);
        p.add(cb, gc1);
        return cb;
    }

    //    修改功能
    private JPanel modifyPanel() {
        Font font = new Font("宋体", Font.BOLD, 16);
        JPanel p = new JPanel();
        p.setLayout(new GridBagLayout());
        GridBagConstraints gc = new GridBagConstraints();
        gc.gridx = 0;
        gc.weighty = 0.2;
        p.add(tp);

        JPanel p1 = new JPanel();
        gc.gridy = 1;
        gc.weightx = 1;
        gc.fill = GridBagConstraints.HORIZONTAL;
        gc.insets = new Insets(15, 0, 0, 200);
        p1.setLayout(new GridLayout(1, 2));

        JLabel label = new JLabel("单位");
        label.setFont(font);
        modifyCom = new JComboBox<>(idName);
        modifyCom.setFont(font);
        modifyCom.addItemListener(this);
        p1.add(label);
        p1.add(modifyCom);
        p.add(p1, gc);

        JPanel p2 = new JPanel();
        gc.gridx = 0;
        gc.gridy = 2;
        p2.setLayout(new GridLayout(1, 2));
        modifyIdLabel = new JLabel("学号");
        modifyIdLabel.setFont(font);
        p2.add(modifyIdLabel);
        modifyIdTF = new JTextField();
        modifyIdTF.getDocument().addDocumentListener(this);
        modifyIdTF.addKeyListener(this);
        ((AbstractDocument) modifyIdTF.getDocument()).setDocumentFilter(new NumberFilter());
        modifyIdTF.setFont(font);
        p2.add(modifyIdTF);
        p.add(p2, gc);

        JPanel p3 = new JPanel();
        gc.gridy = 3;
        p3.setLayout(new GridLayout(1, 3));
        JLabel label1 = new JLabel("新记录");
        label1.setFont(font);
        p3.add(label1);
        modifyTF = new JTextField();
        modifyTF.setFont(font);
        modifyTF.getDocument().addDocumentListener(this);
        p3.add(modifyTF);
        comSelect = new JComboBox<>();
        comSelect.setFont(font);
        comSelect.addItemListener(this);
        model = new DefaultComboBoxModel<>();
        comSelect.setModel(model);
        for(String s : stuSelection){
            model.addElement(s);
        }
        p3.add(comSelect);
        p.add(p3, gc);

        JPanel p4 = new JPanel();
        p4.setLayout(new GridLayout(1, 2));
        gc.gridy = 4;
        selected = new JButton("修改");
        selected.setFont(font);
        selected.addActionListener(this);
        selected.setEnabled(false);
        p4.add(selected);
        send = new JButton("提交");
        send.addActionListener(this);
        send.setFont(font);
        send.setEnabled(false);
        p4.add(send);
        gc.insets = new Insets(0, 0, 0, 0);
        p.add(p4, gc);

        return p;
    }

    //    给所有按钮添加监听器
    private void addListener() {
        tf.addKeyListener(this);
        nameTF.addKeyListener(this);
        groupTF.addKeyListener(this);
        ageTF.addKeyListener(this);
        electricityTF.addKeyListener(this);
        waterTF.addKeyListener(this);
    }

    //    给文本框添加过滤器
    private void init() {
        ((AbstractDocument) tf.getDocument()).setDocumentFilter(new NumberFilter());
        ((AbstractDocument) ageTF.getDocument()).setDocumentFilter(new NumberFilter());
        ((AbstractDocument) waterTF.getDocument()).setDocumentFilter(new DecimalFilter());
        ((AbstractDocument) electricityTF.getDocument()).setDocumentFilter(new DecimalFilter());
    }

    public GridBagConstraints constraints(int gridX, int gridY, double weightX, double weightY) {
        GridBagConstraints c = new GridBagConstraints();
        c.gridx = gridX;
        c.gridy = gridY;
        c.weightx = weightX;
        c.weighty = weightY;
        return c;
    }

    //    创建标签和文本框
    public JTextField newLabel(String name, int gridY) {
        Font font = new Font("宋体", Font.BOLD, 16);
        JLabel label = new JLabel(name);
        label.setFont(font);
        GridBagConstraints gc = constraints(0, gridY, 0.3, weighty);
        p.add(label, gc);
        JTextField t = new JTextField();
        t.setFont(font);
        GridBagConstraints gc1 = constraints(2, gridY, 0.7, weighty);
        gc1.insets = new Insets(15, 0, 0, 200);
        gc1.fill = GridBagConstraints.HORIZONTAL;
        p.add(t, gc1);
        return t;
    }

    @Override
    public void actionPerformed(ActionEvent e) {

        if (e.getSource() == add) {
            card.first(panelRight);
        } else if (e.getSource() == deleted) {
            card.show(panelRight, "delete");
        } else if (e.getSource() == modify) {
            card.show(panelRight, "modify");

        } else if (e.getSource() == sure) {
            if (NotEmpty()) {
                try {
                    if (!addMessage(Objects.requireNonNull(comboBox.getSelectedItem()).toString()))
                        JOptionPane.showMessageDialog(null, idLab.getText() + "已存在");
                } catch (IOException ex) {
                    throw new RuntimeException(ex);
                }
            } else {
                JOptionPane.showMessageDialog(null, "请填写所有信息");
            }
        } else if (e.getSource() == selected) {
            if (Objects.equals(modifyIdTF.getText(), "")) {
                JOptionPane.showMessageDialog(null, "请输入学号或职工号");
                return ;
            }
            if(comSelect.getSelectedItem()=="是否缴费"&&(!Objects.equals(modifyTF.getText(), "是")&&!Objects.equals(modifyTF.getText(), "否")))
            {
            	JOptionPane.showMessageDialog(null,"该信息只能填写是或否");
            	return ;
            }
            if(comSelect.getSelectedItem()=="性别"&&(!Objects.equals(modifyTF.getText(), "男")&&!Objects.equals(modifyTF.getText(), "女")))
            {
            	JOptionPane.showMessageDialog(null,"该信息只能填写男或女");
            	return ;
            }
            if(Objects.equals(tp.getText(), "")){
                JOptionPane.showMessageDialog(null,"该" + modifyCom.getSelectedItem() + "不存在，请在" + modifyCom.getSelectedItem()+"输入框中点击回车后重试，若上方没有信息则表示该生不存在");
                return ;
            }
            tp.setText(modifyMessage(tp.getText()));
        } else if (e.getSource() == send) {
            String fileName;
            if (modifyCom.getSelectedItem() == "学生") {
                fileName = Student.studentFile;
            } else {
                fileName = Teacher.teacherFile;
            }
            try {
                new Achieve().delete(
                        Objects.requireNonNull(modifyCom.getSelectedItem()).toString(),
                        Integer.parseInt(modifyIdTF.getText()));
                writeMessage(fileName, tp.getText()+"\n");
                JOptionPane.showMessageDialog(null,"修改成功");
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        }
    }

    //    判断文本框是否有空白
    private boolean NotEmpty() {
        return !Objects.equals(tf.getText(), "") &&
                !Objects.equals(nameTF.getText(), "") &&
                !Objects.equals(ageTF.getText(), "") &&
                !Objects.equals(groupTF.getText(), "") &&
                !Objects.equals(electricityTF.getText(), "") &&
                !Objects.equals(waterTF.getText(), "");
    }

    @Override
    public void itemStateChanged(ItemEvent e) {


        if (e.getSource() == comboBox) {
            if (e.getItem() == "教工") {
                groupLabel.setText("部门");
                idLab.setText("职工号");
            } else {
                idLab.setText("学号");
                groupLabel.setText("班级");
            }
        } else if (e.getSource() == modifyCom) {
            if(Objects.equals(modifyCom.getSelectedItem(), "学生")) {
                tp.setText(idExist());
                modifyIdLabel.setText("学号");
                model.removeElement("部门");
                if(model.getIndexOf("班级") == -1) {
                    model.insertElementAt("班级", 0);
                }
            } else if (Objects.equals(modifyCom.getSelectedItem(), "教工")) {
                modifyIdLabel.setText("职工号");
                model.removeElement("班级");
                if(model.getIndexOf("部门") == -1) {
                    model.insertElementAt("部门", 0);
                }
            }

        } else if (e.getSource()==comSelect) {
            modifyTF.setText("");
            ((AbstractDocument)modifyTF.getDocument()).setDocumentFilter(null);
            if(Objects.equals(comSelect.getSelectedItem(), "用电量")
                    ||Objects.equals(comSelect.getSelectedItem(), "用水量")||Objects.equals(comSelect.getSelectedItem(), "年龄")
            ){
                ((AbstractDocument)modifyTF.getDocument()).setDocumentFilter(new DecimalFilter());
            }
        }
    }

    @Override
    public void keyTyped(KeyEvent keyEvent) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        JTextField TF = (JTextField) e.getSource();
        if (tf.equals(TF)) {
            if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                nameTF.requestFocus();
            }
        } else if (nameTF.equals(TF)) {
            if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                ageTF.requestFocus();
            }
        } else if (ageTF.equals(TF)) {
            if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                groupTF.requestFocus();
            }
        } else if (groupTF.equals(TF)) {
            if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                electricityTF.requestFocus();
            }
        } else if(electricityTF.equals(TF)) {
            if (e.getKeyCode() == KeyEvent.VK_ENTER) {
                waterTF.requestFocus();
            }
        } else if (modifyIdTF.equals(TF)) {
            tp.setText(idExist());
        }
    }

    @Override
    public void keyReleased(KeyEvent keyEvent) {

    }


    //    添加功能
    private boolean addMessage(String name) throws IOException {
        if (name.equals("教工")) {
            try {
                Teacher teacher = new Teacher(
                        nameTF.getText(),
                        (String) comboBoxSex.getSelectedItem(),
                        Integer.parseInt(ageTF.getText()),
                        Integer.parseInt(tf.getText()),
                        groupTF.getText(), Double.parseDouble(electricityTF.getText()),
                        Double.parseDouble(waterTF.getText()));
                teacher.setFinished(comboBoxFinish.getSelectedItem() == "是");
                return teacher.add_message();
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(null, "输入格式错误");
            }
        } else {
            try {
                Student student = new Student(
                        nameTF.getText(),
                        (String) comboBoxSex.getSelectedItem(),
                        Integer.parseInt(ageTF.getText()),
                        Integer.parseInt(tf.getText()),
                        groupTF.getText(), Double.parseDouble(electricityTF.getText()),
                        Double.parseDouble(waterTF.getText()));
                student.setFinished(comboBoxFinish.getSelectedItem() == "是");
                return student.add_message();
            } catch (NumberFormatException e) {
                JOptionPane.showMessageDialog(null, "输入格式错误");
            }
        }
        return false;
    }

    //    修改信息
    private String modifyMessage(String content) {
        return new Achieve().modify(
                content,
                Objects.requireNonNull(comSelect.getSelectedItem()).toString(),
                modifyTF.getText());
    }

    private void listenModifyBtn() {
        if(modifyIdTF.getText().length()>0 && modifyTF.getText().length()>0){
            selected.setEnabled(true);
            send.setEnabled(true);
        }else{
            selected.setEnabled(false);
            send.setEnabled(false);
        }
    }

    @Override
    public void insertUpdate(DocumentEvent e) {
        listenModifyBtn();
    }

    @Override
    public void removeUpdate(DocumentEvent e) {
        listenModifyBtn();
    }

    @Override
    public void changedUpdate(DocumentEvent e) {
        listenModifyBtn();
    }

    private void writeMessage(String fileName, String content) throws IOException {
        File file = new File(fileName);
        FileOutputStream fos = new FileOutputStream(file,true);
        try (OutputStreamWriter osw = new OutputStreamWriter(fos, StandardCharsets.UTF_8)) {
            osw.write(content);
            osw.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        fos.close();
    }

    private String idExist() {
        try {
            String fileName, idName;
            if (modifyCom.getSelectedItem() == "学生") {
                fileName = Student.studentFile;
                idName = "学号：";
            } else {
                fileName = Teacher.teacherFile;
                idName = "职工号：";
            }
            String content =  new Achieve().read(fileName);
            for(String s : content.split("\n")){
                if(s.contains(idName + modifyIdTF.getText() + ",")){
                    return s;
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        return null;
    }
}
