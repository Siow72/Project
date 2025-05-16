package View;

/**
 * This class represents the start page of the Kwazam Chess game. 
 *
 * @author (Jia Wei)
 * @version (18/12/24)
 */

import java.awt.*;
import javax.swing.*;

/**
 * This class represents the start page of the Kwazam Chess game. 
 * It serves as the main entry point and initializes the GUI components.
 */

public class StartPage {
    JButton startGameButton;
    JButton loadGameButton;
    JButton helpButton;
    JButton exitButton;
    JFrame frame;
    /**
     * Constructor initializes the start page by setting up the JFrame and adding GUI components like buttons and labels.
     */
    public StartPage() {
        // Create the main frame
        frame = new JFrame("Kwazam Chess");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(300, 300);
        frame.setLocationRelativeTo(null); // Center the window

        // Create the main panel with a custom background image
        JPanel panel = new BackgroundPanel("Image//chess.jpg");
        panel.setLayout(new BorderLayout());

        // Title
        JLabel titleLabel = new JLabel("Kwazam Chess", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Serif", Font.BOLD, 24));
        titleLabel.setForeground(Color.BLACK); // Adjust font color for visibility
        panel.add(titleLabel, BorderLayout.NORTH);

        // Buttons panel
        JPanel buttonsPanel = new JPanel();
        buttonsPanel.setLayout(new GridLayout(4, 1, 10, 10));
        buttonsPanel.setOpaque(false); // Make buttons panel transparent

        // Start Game button
        startGameButton = new JButton("Start Game");
        buttonsPanel.add(startGameButton);

        // Load Game button
        loadGameButton = new JButton("Load Game");
        buttonsPanel.add(loadGameButton);

        // Rules button
        helpButton = new JButton("Help");
        buttonsPanel.add(helpButton);

        // Exit button
        exitButton = new JButton("Exit");
        buttonsPanel.add(exitButton);

        panel.add(buttonsPanel, BorderLayout.CENTER);

        // Add padding around the buttons panel
        panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        // Add the panel to the frame
        frame.add(panel);

        // Make the frame visible
        frame.setVisible(true);
    }

    public JFrame getFrame(){
        return frame;
    }

    public JButton getStartButton(){
        return startGameButton;
    }
    public JButton getLoadButton(){
        return loadGameButton;
    }
    public JButton getHelpButton(){
        return helpButton;
    }
    public JButton getExitButton(){
        return exitButton;
    }
}




