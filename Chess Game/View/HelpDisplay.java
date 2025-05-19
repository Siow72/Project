package View;

import java.awt.*;
import javax.swing.*;

// Author: Law Li Ting
public class HelpDisplay extends JFrame {

    private static final Font TEXT_FONT = new Font("Arial", Font.PLAIN, 15);
    private static final Font TITLE_FONT = new Font("Arial", Font.BOLD, 40);

    public HelpDisplay() {
        super("Game Manual");
        this.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE); // Close only this window
        setSize(700, 800);  // Initial size
        setResizable(true); // Allow resizing

        // Create the main background panel with GridBagLayout
        BackgroundPanel backgroundPanel = new BackgroundPanel("Image/Manual.jpg");
        backgroundPanel.setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(15, 15, 15, 15); // Add padding

        // Add the title
        JLabel titleLabel = new JLabel("Help");
        titleLabel.setFont(TITLE_FONT);
        titleLabel.setHorizontalAlignment(SwingConstants.CENTER);
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setBorder(BorderFactory.createEmptyBorder(10, 0, 20, 0));
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        backgroundPanel.add(titleLabel, gbc);

        // Add the help text area with scroll pane
        JTextArea helpContentArea = new JTextArea(getHelpContent());
        helpContentArea.setFont(TEXT_FONT);
        helpContentArea.setEditable(false);
        helpContentArea.setOpaque(false);
        helpContentArea.setForeground(Color.WHITE);
        helpContentArea.setLineWrap(true);
        helpContentArea.setWrapStyleWord(true);

        JScrollPane scrollPane = new JScrollPane(helpContentArea);
        scrollPane.setOpaque(false);
        scrollPane.getViewport().setOpaque(false);
        scrollPane.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.WHITE), "Game Rules", 0, 0, TEXT_FONT, Color.WHITE));
        gbc.gridy = 1;
        gbc.weightx = 1.0;
        gbc.weighty = 0.5;
        gbc.fill = GridBagConstraints.BOTH;
        backgroundPanel.add(scrollPane, gbc);

        // Add the piece descriptions panel
        JPanel piecePanel = createPieceDescriptions();
        JScrollPane pieceScrollPane = new JScrollPane(piecePanel);
        pieceScrollPane.setOpaque(false);
        pieceScrollPane.getViewport().setOpaque(false);
        pieceScrollPane.setBorder(BorderFactory.createTitledBorder(BorderFactory.createLineBorder(Color.WHITE), "Piece Descriptions", 0, 0, TEXT_FONT, Color.WHITE));
        gbc.gridy = 2;
        gbc.weighty = 1.0;
        backgroundPanel.add(pieceScrollPane, gbc);

        // Set the background panel as the content pane
        setContentPane(backgroundPanel);
        setVisible(true);
    }

    private JPanel createPieceDescriptions() {
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(5, 1, 10, 10));
        panel.setOpaque(false);

        // Add individual piece panels
        panel.add(createPiecePanel("Image/blueRam.png", "RAM: Moves forward 1 step at a time and can't skip pieces."));
        panel.add(createPiecePanel("Image/blueBiz.png", "BIZ: Moves in a 3x2 L-shape. This is the only piece that can skip over others."));
        panel.add(createPiecePanel("Image/blueTor.png", "TOR: Moves orthogonally but can't skip over pieces. After 2 turns, it transforms into XOR."));
        panel.add(createPiecePanel("Image/blueXor.png", "XOR: Moves diagonally but can't skip over pieces. After 2 turns, it transforms into TOR."));
        panel.add(createPiecePanel("Image/blueSau.png", "SAU: Moves 1 step in any direction. The game ends when the Sau is captured."));

        return panel;
    }

    private JPanel createPiecePanel(String imagePath, String description) {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setOpaque(false);

        // Add the image
        JLabel imageLabel = new JLabel(new ImageIcon(getScaledImage(imagePath, 50, 50)));
        imageLabel.setToolTipText(description); // Tooltip for better context
        panel.add(imageLabel, BorderLayout.WEST);

        // Add the description
        JLabel descriptionLabel = new JLabel("<html>" + description + "</html>");
        descriptionLabel.setFont(TEXT_FONT);
        descriptionLabel.setForeground(Color.WHITE);
        panel.add(descriptionLabel, BorderLayout.CENTER);

        return panel;
    }

    private Image getScaledImage(String path, int width, int height) {
        ImageIcon icon = new ImageIcon(path);
        return icon.getImage().getScaledInstance(width, height, Image.SCALE_SMOOTH);
    }

    private String getHelpContent() {
        return """
            Welcome to Kwazam Chess!

            Game Rules:
            1. The game is played on a 5x8 board.
            2. The goal is to capture the opponent's Sau piece. The game ends when the Sau is captured.

            Piece Movement Rules:
            - Ram: Moves forward 1 step at a time. If it reaches the end of the board, it turns around and moves back. Cannot skip over other pieces.
            - Biz: Moves in a 3x2 L-shape (like a knight in standard chess). This is the only piece that can skip over others.
            - Tor: Moves orthogonally but cannot skip over pieces. Transforms into Xor after 2 turns.
            - Xor: Moves diagonally but cannot skip over pieces. Transforms into Tor after 2 turns.
            - Sau: Moves 1 step in any direction. The game ends when the Sau is captured.

            Special Rules:
            - Pieces transform after 2 turns:
              - Tor transforms into Xor.
              - Xor transforms into Tor.
            - None of the pieces can skip over others except Biz.
            - Each move by blue and red counts as 1 turn.
        """;
    }
}
