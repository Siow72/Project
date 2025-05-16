//Author : Lim Jia Wei

package View;
import java.awt.*;
import javax.swing.*;

// View of the Kawazam Chess game
/**
 * BackgroundPanel is a custom JPanel that allows setting a background image.
 * The image is scaled to fit the entire panel dynamically.
 */

public class BackgroundPanel extends JPanel {
    private final Image backgroundImage;

    // Constructor to load the image
    public BackgroundPanel(String imagePath) {
        backgroundImage = new ImageIcon(imagePath).getImage();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // Draw the image to fill the entire panel
        if (backgroundImage != null) {
            g.drawImage(backgroundImage, 0, 0, getWidth(), getHeight(), this);
        }
    }
}
