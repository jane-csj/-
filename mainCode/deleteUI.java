import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import java.util.Objects;

public  class deleteUI implements ItemListener, KeyListener, ActionListener {
    private JTextPane TP;
    private JTextField TF;
    private final String[] units = {"学生", "教工"};
    private JComboBox<String> combUnit;
    private JLabel idLabel;

    public JPanel createDeletedUI() {

        Font font = new Font("宋体", Font.BOLD, 24);


        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(2,1));
        panel.setLocation(0, 0);

        TP = new JTextPane();
        TP.setFont(font);
        TP.setEditable(false);
        GridBagConstraints gcTP = new GridBagConstraints();
        gcTP.gridx = 0;gcTP.gridy = 0;
        gcTP.gridheight = 10;
        panel.add(TP,gcTP);
        panel.add(TP);

        JPanel p = new JPanel();

        p.setLayout(new GridBagLayout());
        GridBagConstraints gcP = new GridBagConstraints();
        gcP.gridx = 0;gcP.gridy = 10;
        gcP.gridheight = 20;
        panel.add(p,gcP);

        JLabel unitLabel = new JLabel("单位");
        unitLabel.setFont(font);
        GridBagConstraints gcUnit = new GridBagConstraints();
        gcUnit.gridx = 0;
        gcUnit.gridy = 0;
        gcUnit.weightx = 0.3;
        gcUnit.weighty = 0.2;
        p.add(unitLabel, gcUnit);

        combUnit = new JComboBox<>(units);
        combUnit.addItemListener(this);
        combUnit.setFont(font);
        GridBagConstraints gcComb = new GridBagConstraints();
        gcComb.gridx = 2;
        gcComb.gridy = 0;
        gcComb.weightx = 0.7;
        gcComb.weighty = 0.2;
        gcComb.fill = GridBagConstraints.HORIZONTAL;
        gcComb.insets = new Insets(15, 0, 0, 200);
        p.add(combUnit, gcComb);

        idLabel = new JLabel("学号");
        idLabel.setFont(font);
        GridBagConstraints gcId = new GridBagConstraints();
        gcId.gridx = 0;
        gcId.gridy = 1;
        gcId.weightx = 0.3;
        gcId.weighty = 0.2;
        p.add(idLabel, gcId);

        TF = new JTextField();
        TF.addKeyListener(this);
        TF.setFont(font);
        GridBagConstraints gcTF = new GridBagConstraints();
        gcTF.gridx = 2;
        gcTF.gridy = 1;
        gcTF.weightx = 0.7;
        gcTF.weighty = 0.2;
        gcTF.fill = GridBagConstraints.HORIZONTAL;
        gcTF.insets = new Insets(15, 0, 0, 200);
        p.add(TF, gcTF);


        JButton deleted = new JButton("删除");
        deleted.addActionListener(this);
        GridBagConstraints gcDel = new GridBagConstraints();
        gcDel.gridx = 2;
        gcDel.gridy = 2;
        gcDel.weightx = 0.7;
        gcDel.weighty = 0.6;
        gcDel.fill = GridBagConstraints.HORIZONTAL;
        gcDel.insets = new Insets(0, 0, 0, 200);
        p.add(deleted, gcDel);

        return panel;
    }

    @Override
    public void itemStateChanged(ItemEvent e) {
        if (combUnit.getSelectedItem() == "教工") {
            idLabel.setText("职工号");
        } else {
            idLabel.setText("学号");
        }
    }

    @Override
    public void keyTyped(KeyEvent e) {

    }

    @Override
    public void keyPressed(KeyEvent e) {
        String unit ;
        if (e.getKeyCode() == KeyEvent.VK_ENTER) {
            UI ui = new UI();
            String fileName;
            if (combUnit.getSelectedItem() == "学生") {
                fileName = Student.studentFile;
                unit = "学号：";
            }
            else {fileName = Teacher.teacherFile;unit = "职工号：";}
            try {
                String content = ui.read(fileName);
                String[] split = content.split("\n");
                for (String s : split) {
                    if (s.contains(unit + TF.getText() + ",")) {
                        TP.setText("查询到的信息：" + s);
                        return ;
                    }
                }
                TP.setText("查询不到此人的信息，请确认该人已注册，请重试");
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }

        }
    }

    @Override
    public void keyReleased(KeyEvent e) {

    }

    @Override
    public void actionPerformed(ActionEvent e) {
        UI ui = new UI();
        String fileName ,unit;
        if (combUnit.getSelectedItem() == "学生"){ fileName = Student.studentFile;unit = "学号：";}
        else {fileName = Teacher.teacherFile;unit = "职工号：";}
        try {
            String content = ui.read(fileName);
            String[] split = content.split("\n");
            for (String s : split) {
                if (s.contains(unit + TF.getText() + ",")) {
                    int result = JOptionPane.showConfirmDialog(null, "确定删除吗", "系统提醒", JOptionPane.YES_NO_OPTION);
                    if (result == JOptionPane.YES_OPTION) {
                        try {
                            new UI().delete(Objects.requireNonNull(combUnit.getSelectedItem()).toString(), Integer.parseInt(TF.getText()));
                            JOptionPane.showMessageDialog(null, "删除成功");
                        } catch (IOException ex) {
                            throw new RuntimeException(ex);
                        }

                    }
                }
            }
            if (!content.contains(unit + TF.getText() + ",")) {
                JOptionPane.showMessageDialog(null, "查询不到此人信息，请重试");
            }
        } catch (IOException ex) {
            throw new RuntimeException(ex);
        }
    }
}

