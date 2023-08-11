import javax.swing.*;
import javax.swing.plaf.basic.BasicButtonUI;
import javax.swing.text.AbstractDocument;
import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import java.util.Objects;

public  class statSystem extends Achieve implements ActionListener, ItemListener, KeyListener {
    private String content;

    public statSystem() throws IOException {
        UI ui = new UI();
        this.content = ui.isFinished();
    }

    private JPanel panel1;
    private JPanel panelRight;
    private JButton btnAll, btnById, stuEleBtn, teaEleBtn, stuWaterBtn, teaWaterBtn;
    private CardLayout card;
    private JLabel labelId;
    private JTextPane queryTP;
    private JComboBox<String> comboBox;
    private JTextField TF;

    public void createUI() throws IOException {
        myFrame frame = new myFrame();
        panelRight = new JPanel();
        card = new CardLayout();
        panelRight.setLayout(card);


        //       欢迎界面
        JPanel welPanel = new JPanel();
        JLabel label = new JLabel("欢迎使用统计功能");
        label.setFont(new Font("宋体", Font.BOLD,24));
        welPanel.add(label);
        panelRight.add(welPanel);

        //        全部未缴费名单
        JPanel panel = new showText().showPanel(content);
        panelRight.add("all", panel);
        add();

        queryById();

        //        窗口左边
        panel1 = new JPanel();
        panel1.setLayout(new GridLayout(7, 1, 1, 5));
        BtnInit();


        JFrame fr = frame.createFrame("统计系统", panel1, panelRight);

        fr.setVisible(true);
        fr.setResizable(true);

    }

    private JPanel checkUI(String s) {
        JPanel panel = new JPanel();
        panel.setLayout(new FlowLayout());
        JTextPane TP = new JTextPane();
        TP.setEditable(false);
        TP.setFont(new Font("宋体", Font.BOLD,16));
        TP.setText(s);
        panel.add(TP);

        return panel;
    }

    //    添加文本
    private void add() throws IOException {

        double total = new statSystem().electricity(Student.studentFile);
        panelRight.add("stuEle", checkUI("所有学生所需要交的电费为：" + String.format("%.2f",total) + "\n"
                + "学生平均要交的电费为：" + String.format("%.2f",total / Achieve.getNumber()[0])));


        total = new statSystem().water(Student.studentFile);
        panelRight.add("stuWater", checkUI("所有学生所需要交的水费为：" + String.format("%.2f",total) + "\n"
                + "学生平均要交的水费为：" + String.format("%.2f",total / Achieve.getNumber()[0])));


        total = new statSystem().electricity(Teacher.teacherFile);
        panelRight.add("teaEle", checkUI("所有教工所需要交的电费为：" + String.format("%.2f",total) + "\n"
                + "教工平均要交的电费为：" + String.format("%.2f",total / Achieve.getNumber()[1])));


        total = new statSystem().water(Teacher.teacherFile);
        panelRight.add("teaWater", checkUI("所有教工所需要交的水费为：" + String.format("%.2f",total) + "\n"
                + "教工平均要交的电水费为：" + String.format("%.2f",total / Achieve.getNumber()[1])));
    }

    //    通过ID查询
    private void queryById() {
        Font font = new Font("宋体",Font.BOLD,16);
        String[] units = {"学生", "教工"};
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(5, 1,0,20));
        queryTP = new JTextPane();
        queryTP.setFont(font);
        queryTP.setEditable(false);
        panel.add(queryTP);

        JPanel p = new JPanel();
        p.setLayout(new GridLayout(3, 2));
        JLabel labelUnit = new JLabel("单位");
        labelUnit.setHorizontalAlignment(JLabel.CENTER);
        labelUnit.setFont(font);
        p.add(labelUnit);
        comboBox = new JComboBox<>(units);
        comboBox.addItemListener(this);
        p.add(comboBox);

        labelId = new JLabel("学号");
        labelId.setHorizontalAlignment(JLabel.CENTER);
        labelId.setFont(font);
        p.add(labelId);

        TF = new JTextField();
        ((AbstractDocument) TF.getDocument()).setDocumentFilter(new NumberFilter());
        TF.addKeyListener(this);
        p.add(TF);
        panel.add(p);

        JButton queryBtn = new JButton("查询");
        queryBtn.setFont(font);
        queryBtn.addActionListener(this);
        panel.add(queryBtn);

        panelRight.add("queryById", panel);
    }


    //    初始化按钮
    private void BtnInit() {
        btnAll = new JButton("未交费名单");
        btnAll.addActionListener(this);
        btnAll.setUI(new BasicButtonUI());
        btnById = new JButton("查询个人缴费信息");
        btnById.setUI(new BasicButtonUI());
        btnById.addActionListener(this);
        stuEleBtn = new JButton("学生要交的电费");
        stuEleBtn.setUI(new BasicButtonUI());
        stuEleBtn.addActionListener(this);
        stuWaterBtn = new JButton("学生要交的水费");
        stuWaterBtn.setUI(new BasicButtonUI());
        stuWaterBtn.addActionListener(this);
        teaEleBtn = new JButton("教工要交的电费");
        teaEleBtn.setUI(new BasicButtonUI());
        teaEleBtn.addActionListener(this);
        teaWaterBtn = new JButton("教工要交的水费");
        teaWaterBtn.setUI(new BasicButtonUI());
        teaWaterBtn.addActionListener(this);
        panel1.add(btnAll);
        panel1.add(btnById);
        panel1.add(stuEleBtn);
        panel1.add(stuWaterBtn);
        panel1.add(teaEleBtn);
        panel1.add(teaWaterBtn);
    }



    @Override
    public void actionPerformed(ActionEvent e) {
        if (e.getSource() == btnAll) {
            card.show(panelRight, "all");
        } else if (e.getSource() == stuEleBtn) {
            card.show(panelRight, "stuEle");
        } else if (e.getSource() == stuWaterBtn) {
            card.show(panelRight, "stuWater");
        } else if (e.getSource() == teaEleBtn) {
            card.show(panelRight, "teaEle");
        } else if (e.getSource() == teaWaterBtn) {
            card.show(panelRight, "teaWater");
        } else if (e.getSource() == btnById) {
            card.show(panelRight, "queryById");
        } else if (((JButton) e.getSource()).getText().equals("查询")) {
            try {
                if (!Objects.equals(TF.getText(), "")) {
                    queryTP.setText(calculate(Objects.requireNonNull(comboBox.getSelectedItem()).toString(),
                            Integer.parseInt(TF.getText())));
                }
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        }
    }

    @Override
    public void itemStateChanged(ItemEvent e) {
        if (Objects.equals(comboBox.getSelectedItem(), "学生")) {
            labelId.setText("学号");

        } else {
            labelId.setText("职工号");
        }
        if (!Objects.equals(TF.getText(), "")) {
            try {
                queryTP.setText(calculate(Objects.requireNonNull(comboBox.getSelectedItem()).toString(),
                        Integer.parseInt(TF.getText())));
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        }
    }

    @Override
    public void keyTyped(KeyEvent keyEvent) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        if (e.getKeyCode() == KeyEvent.VK_ENTER && !Objects.equals(TF.getText(), "")) {
            try {
                queryTP.setText(calculate(Objects.requireNonNull(comboBox.getSelectedItem()).toString(),
                        Integer.parseInt(TF.getText())));
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        }
    }

    @Override
    public void keyReleased(KeyEvent keyEvent) {

    }
}

