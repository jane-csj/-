import javax.swing.*;
import java.awt.*;

public  class showText {
    public JPanel showPanel(String content){
        JPanel panel = new JPanel();
        panel.setLayout(new GridBagLayout());
        GridBagConstraints gc = new GridBagConstraints();
        gc.gridx=0;
        gc.gridy=0;
        gc.weightx=1.0;
        gc.weighty=1.0;
        gc.fill = GridBagConstraints.BOTH;
        JTextPane jTextPane = new JTextPane();
        jTextPane.setText(content);
        jTextPane.setEditable(false);
        jTextPane.setFont(new Font("Arial", Font.BOLD,16));
        panel.add(jTextPane,gc);
        return panel;
    }
}
