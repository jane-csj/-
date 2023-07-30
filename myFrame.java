import javax.swing.*;
import java.awt.*;

public  class myFrame extends JFrame {
    public JFrame createFrame(String title,JPanel panel1,JPanel panel2){
        Toolkit toolkit = Toolkit.getDefaultToolkit();

        // 获取屏幕的尺寸
        Dimension screenSize = toolkit.getScreenSize();

        // 获取屏幕的宽度和高度
        int screenWidth = screenSize.width;
        int screenHeight = screenSize.height;

        JFrame fr = new JFrame(title);
        fr.setSize(800,600);
        fr.setDefaultCloseOperation(HIDE_ON_CLOSE);
        fr.setLayout(new GridBagLayout());
        GridBagConstraints gc = new GridBagConstraints();
        gc.gridx=0;gc.gridy=0;gc.weightx=0.3;
        gc.weighty=1;
        gc.fill = GridBagConstraints.BOTH;
        fr.add(panel1,gc);

        GridBagConstraints gc1 = new GridBagConstraints();
        gc1.gridy = 0;gc1.gridx=1;gc1.weightx=0.7;
        gc1.weighty=1;
        gc1.fill = GridBagConstraints.BOTH;

        fr.add(panel2,gc1);
        fr.setLocation(screenWidth/2-400,screenHeight/2-300);
        return fr;
    }
}
