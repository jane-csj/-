import javax.swing.*;
import javax.swing.plaf.basic.BasicButtonUI;
import javax.swing.text.AbstractDocument;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.IOException;
import java.util.ArrayList;

public  class querySystem implements ActionListener, KeyListener {
    private final int btnLength = 6;
    private JPanel panelLeft;
    private JPanel panel;
    private CardLayout card;
    private JTextPane tp;
    private JTextField nameTF;
    private JButton query;
    JLabel label;
    private final JButton[] buttons = new JButton[btnLength];
    private final String[] btnStr = {"查询全部", "通过姓名查询", "通过单位查询", "通过用电量查询", "通过用水量查询", "通过ID查询"};
    private final String[] btnStr2 = {"查询", "姓名查询", "单位查询", "用电量查询", "用水量查询", "ID查询"};
    private JButton queryAll;
    private Font font;

    public void createUI() {
        panelLeft = new JPanel();
        panelLeft.setLayout(new GridLayout(6, 1));
        initBtn();


        JPanel panelRight = new JPanel();
        card = new CardLayout();
        panelRight.setLayout(new GridLayout(2, 1));
        tp = getTP();
        panelRight.add(tp);


        panel = new JPanel();
        panel.setLayout(card);

        JPanel all = new JPanel();
        all.setLayout(new GridBagLayout());
        GridBagConstraints gc = new GridBagConstraints();
        gc.gridx=0;
        gc.gridy=0;
        gc.weightx=1;
        gc.weighty = 0.5;
        gc.gridheight = 2;
        gc.fill = GridBagConstraints.HORIZONTAL;
        queryAll = new JButton("查询");

        queryAll.setFont(font);
        queryAll.addActionListener(this);
        all.add(queryAll,gc);
        gc.gridy=1;
        all.add(new JPanel(),gc);
        panel.add("all", all);
        JPanel name = namePanel();
        panel.add("queryByName", name);

        panelRight.add(panel);
        JFrame fr = new myFrame().createFrame("查询系统", panelLeft, panelRight);
        fr.setVisible(true);
    }

    private JPanel namePanel() {
        font = new Font("宋体", Font.BOLD,16);
        JPanel p = new JPanel();
        p.setLayout(new GridLayout(3, 2,0,50));
        label = new JLabel("姓名");
        label.setHorizontalAlignment(JLabel.CENTER);
        label.setFont(font);
        p.add(label);
        nameTF = new JTextField();
        nameTF.addKeyListener(this);
        p.add(nameTF);
        query = new JButton("确认");
        query.addActionListener(this);
        p.add(query);

        JButton btn = new JButton("清空");
        btn.addActionListener(this);
        p.add(btn);
        return p;
    }

    private JTextPane getTP() {
        JTextPane tp = new JTextPane();
        tp.setEditable(false);
        tp.setText("欢迎使用查询功能");
        tp.setFont(new Font("Arial", Font.BOLD, 15));
        tp.setAutoscrolls(true);
        return tp;
    }

    private void initBtn() {
        for (int i = 0; i < buttons.length; i++) {
            buttons[i] = new JButton(btnStr[i]);
            buttons[i].addActionListener(this);
            buttons[i].setUI(new BasicButtonUI());
            panelLeft.add(buttons[i]);
        }

    }

    public static void main(String[] args) {
        querySystem qs = new querySystem();
        qs.createUI();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        JButton btn = (JButton) e.getSource();
        if (btn.getText().equals(btnStr[0])) {
            card.show(panel, "all");
            tp.setText("欢迎使用查询功能,请输入你要查询的条件，请勿留空");

        } else if (btn.getText().equals(btnStr[1])) {
            label.setText("姓名");
            query.setText(btnStr2[1]);
            nameTF.setText("");
            ((AbstractDocument)nameTF.getDocument()).setDocumentFilter(null);
            tp.setText("欢迎使用查询功能,请输入你要查询的条件，请勿留空");
            card.show(panel, "queryByName");
        } else if (btn.getText().equals(btnStr[2])) {
            label.setText("单位");
            query.setText(btnStr2[2]);
            tp.setText("欢迎使用查询功能,请输入你要查询的条件，请勿留空");
            ((AbstractDocument)nameTF.getDocument()).setDocumentFilter(null);
            nameTF.setText("");
            card.show(panel, "queryByName");
        } else if (btn.getText().equals(btnStr[3])) {
            label.setText("用电量");
            query.setText(btnStr2[3]);
            tp.setText("欢迎使用查询功能,请输入你要查询的条件，请勿留空");
            nameTF.setText("");
            ((AbstractDocument)nameTF.getDocument()).setDocumentFilter(new DecimalFilter());
            card.show(panel, "queryByName");
        } else if (btn.getText().equals(btnStr[4])) {
            label.setText("用水量");
            query.setText(btnStr2[4]);
            nameTF.setText("");
            ((AbstractDocument)nameTF.getDocument()).setDocumentFilter(new DecimalFilter());
            tp.setText("欢迎使用查询功能,请输入你要查询的条件，请勿留空");
            card.show(panel, "queryByName");
        } else if (btn.getText().equals(btnStr[5])) {
            label.setText("ID");
            query.setText(btnStr2[5]);
            tp.setText("欢迎使用查询功能,请输入你要查询的条件，请勿留空");
            nameTF.setText("");
            ((AbstractDocument)nameTF.getDocument()).setDocumentFilter(new DecimalFilter());
            card.show(panel, "queryByName");
        } else if (btn.getText().equals(btnStr2[2])) {
            ArrayList<String> str;
            try {
                str = new Achieve().QueryByUnit(nameTF.getText());
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
            if (str.size()==0) {
                tp.setText("该单位不存在");
            }else{
                StringBuilder s = new StringBuilder();
                for(String st : str) {
                    s.append(st).append("\n");
                }
                tp.setText(s.toString());
            }
        } else if (btn.getText().equals("清空")) {
            nameTF.setText("");
        } else if (btn.equals(queryAll)) {
            try {
                tp.setText(new Achieve().show());
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        } else if (btn.getText().equals("姓名查询")) {
            StringBuilder sb = new StringBuilder();
            try {
                ArrayList<String> stu = new Achieve().QueryByName("学生", nameTF.getText());
                ArrayList<String> tea = new Achieve().QueryByName("教工", nameTF.getText());
                if (stu.size() == 0 && tea.size() == 0) {
                    tp.setText("此人不存在");
                } else {
                    for (String s : stu) {
                        sb.append(s).append("\n");
                    }
                    for (String s : tea) {
                        sb.append(s).append("\n");
                    }
                    tp.setText(sb.toString());
                }
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        } else if (btn.getText().equals(btnStr2[3])) {
            StringBuilder sb = new StringBuilder();
            try {
                ArrayList<String> stu = new Achieve().QueryByElectricity("学生",
                        Double.parseDouble(nameTF.getText()));
                ArrayList<String> tea = new Achieve().QueryByElectricity("教工",
                        Double.parseDouble(nameTF.getText()));
                if (stu.size() == 0 && tea.size() == 0) {
                    tp.setText("没有高于用电量" + nameTF.getText() + "的人");
                } else {
                    for (String s : stu) {
                        sb.append(s).append("\n");
                    }
                    for (String s : tea) {
                        sb.append(s).append("\n");
                    }
                    tp.setText(sb.toString());
                }
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }catch (NumberFormatException nex){
                JOptionPane.showMessageDialog(null,"输入错误");
                nameTF.setText("");
            }
        } else if (btn.getText().equals(btnStr2[4])) {

            StringBuilder sb = new StringBuilder();
            try {
                ArrayList<String> stu = new Achieve().QueryByWater("学生",
                        Double.parseDouble(nameTF.getText()));
                ArrayList<String> tea = new Achieve().QueryByWater("教工",
                        Double.parseDouble(nameTF.getText()));
                if (stu.size() == 0 && tea.size() == 0) {
                    tp.setText("没有用水量超过" + nameTF.getText() + "的人");
                } else {
                    for (String s : stu) {
                        sb.append(s).append("\n");
                    }
                    for (String s : tea) {
                        sb.append(s).append("\n");
                    }
                    tp.setText(sb.toString());
                }

            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }catch (NumberFormatException nex){
                JOptionPane.showMessageDialog(null,"输入错误");
                nameTF.setText("");
            }

        } else if (btn.getText().equals(btnStr2[5])) {
            ArrayList<String> str;
            try {
                str = new Achieve().QueryById(Integer.parseInt(nameTF.getText()));
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
            if (str.size()==0) {
                tp.setText("该单位不存在");
            }else{
                StringBuilder s = new StringBuilder();
                for(String st : str) {
                    s.append(st).append("\n");
                }
                tp.setText(s.toString());
            }
        }
    }

    @Override
    public void keyTyped(KeyEvent keyEvent) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        if(e.getKeyCode() == KeyEvent.VK_ENTER){
            query.doClick();
        }
    }

    @Override
    public void keyReleased(KeyEvent keyEvent) {

    }
}




