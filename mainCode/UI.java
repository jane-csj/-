import javax.swing.*;
import javax.swing.plaf.basic.BasicButtonUI;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

public  class UI extends Achieve implements ActionListener {
    String []tools = {
            "查询","修改","统计"
    };
    JFrame fr = new JFrame("水电管理系统");
    public void createUI() {


        fr.setLocation(400,300);
        fr.setSize(600, 400);
        fr.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        fr.setLayout(null);
        fr.setLocationRelativeTo(null);



        JPanel panel = new JPanel();
        GridLayout grid = new GridLayout(5,1);
        panel.setLayout(grid);
        panel.add(new JPanel());
        for(int i=0;i<3;i++){
            JButton button = new JButton(tools[i]);
            button.addActionListener(this);
            button.setUI(new BasicButtonUI());
            panel.add(button);
        }
        panel.setBounds(0,50,fr.getWidth(),350);



        JLabel label = new JLabel("欢迎使用水电管理系统");
        //        label.setSize(100,100);
        label.setFont(new Font("SimHei", Font.BOLD,16));
        label.setForeground(Color.blue);
        label.setBounds(200,0,fr.getWidth(),50);


        fr.add(label);
        fr.add(panel);

        fr.setVisible(true);
    }

    public static void main(String[] args) {
        UI ui = new UI();
        ui.createUI();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        JButton button = (JButton)e.getSource();
        if(button.getText().equals("查询")){
            querySystem qs = new querySystem();
            qs.createUI();
        }else if(button.getText().equals("修改")){
            editSystem ui = new editSystem();
            ui.createUI();
        }else{
            statSystem statSystem;
            try {
                statSystem = new statSystem();
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
            try {
                statSystem.createUI();
            } catch (IOException ex) {
                throw new RuntimeException(ex);
            }
        }
    }
}
