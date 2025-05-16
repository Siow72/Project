package View;

import Model.ChessModel;
import Piece.*;
import java.awt.*;
import java.util.List;
import java.util.Map;
import javax.swing.*;

// View of the Kawazam Chess game

//BoardDisplay is focus on display the GUI of the game board and the piece position
//and display the message box 

public class BoardDisplay extends JPanel {
    private Graphics2D g2d;
    private final ChessModel MODEL;
    private int tileSize = 85; // Size of each tile in pixels
    private final int COLS = 5;            // Number of columns on the board
    private final int ROWS = 8;            // Number of ROWS on the board
    private int xOffset, yOffset;
    private Point selectedTile = null; // To track the selected tile
    private List<Point> possibleMove = null;
    private boolean isFlipBoard;
    private final Map<Point, _Piece> PIECE_POS;
    private final Color POSSIBLE_COLOR = new Color(144, 238, 144, 128);
    private final int ADDITIONAL_HEIGHT = 30; // Smaller height for the current player row

    //Author : Lim Jia Wei
    /**
     * Constructor for the BoardDisplay class.
     * Sets the preferred size of the JPanel based on the grid dimensions and additional row for current player.
     */
    public BoardDisplay(ChessModel model) {
        this.PIECE_POS = model.getBoard().getPiecePositions();
        this.MODEL = model;
        setPreferredSize(new Dimension(COLS * tileSize, ROWS * tileSize + ADDITIONAL_HEIGHT)); // Adjust height for the additional row
    }

    /**
     * Custom painting logic for the game board.
     * Draws a grid with alternating tile colors and renders pieces.
     * @param g Graphics object used for painting.
     */
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        g2d = (Graphics2D) g;

        // Calculate tile size to fit the board within the panel
        tileSize = Math.min(getWidth() / COLS, (getHeight() - ADDITIONAL_HEIGHT) / ROWS); // Adjust for additional row height

        // Calculate offsets for centering the board (adjusted for the additional row)
        xOffset = (getWidth() - (COLS * tileSize)) / 2;
        yOffset = (getHeight() - (ROWS * tileSize + ADDITIONAL_HEIGHT)) / 2 + ADDITIONAL_HEIGHT; // Adjust for current player row

        // Draw the board
        if (!isFlipBoard) {
            for (int r = 0; r < ROWS; r++) {
                for (int c = 0; c < COLS; c++) {
                    if ((r + c) % 2 == 0) {
                        g2d.setColor(new Color(227, 198, 181)); // Light tile color
                    } else {
                        g2d.setColor(new Color(157, 105, 53));  // Dark tile color
                    }
                    g2d.fillRect(xOffset + c * tileSize, yOffset + r * tileSize, tileSize, tileSize);
                }
            }
        } else {
            for (int r = 0; r < ROWS; r++) {
                for (int c = 0; c < COLS; c++) {
                    if ((r + c) % 2 == 0) {
                        g2d.setColor(new Color(157, 105, 53));  // Dark tile color
                    } else {
                        g2d.setColor(new Color(227, 198, 181)); // Light tile color
                    }
                    g2d.fillRect(xOffset + c * tileSize, yOffset + r * tileSize, tileSize, tileSize);
                }
            }
        }

        // Highlight the selected tile
        if (selectedTile != null) {
            g2d.setColor(new Color(255, 255, 0, 128)); // Semi-transparent yellow
            int x = xOffset + selectedTile.y * tileSize;
            int y = yOffset + selectedTile.x * tileSize;
            g2d.fillRect(x, y, tileSize, tileSize);

            // Highlight the possible move
            g2d.setColor(POSSIBLE_COLOR);
            if (possibleMove != null) {
                for (Point move : possibleMove) {
                    if (move.x >= 0 && move.x < ROWS && move.y >= 0 && move.y < COLS) {
                        int moveX = xOffset + move.y * tileSize;
                        int moveY = yOffset + move.x * tileSize;
                        g2d.fillRect(moveX, moveY, tileSize, tileSize);
                    }
                }
            }
        }

        // Draw the pieces
        for (Map.Entry<Point, _Piece> entry : PIECE_POS.entrySet()) {
            Point pos = entry.getKey();
            _Piece piece = entry.getValue();

            // Calculate the position of each piece
            int x = xOffset + pos.y * tileSize;
            int y = yOffset + pos.x * tileSize;
            
            // Draw the piece
            piece.draw(g2d, x, y, tileSize);
        }
        
        //Author : Law Li Ting
        // Display current player at the top of the board
        g2d.setColor(Color.BLACK);
        g2d.setFont(new Font("Times", Font.BOLD, 14)); // Smaller font size for the current player
        String currentPlayer = "Current Player: " + MODEL.getState().getcurrentPlayer().toUpperCase() + " | Current Round : " + MODEL.getState().getTurn();

        // Calculate the width of the text
        FontMetrics metrics = g2d.getFontMetrics();
        int textWidth = metrics.stringWidth(currentPlayer);
        int textHeight = metrics.getHeight();

        // Horizontal positioning: Center the text
        int xText = (getWidth() - textWidth) / 2;

        // Vertical positioning: Center the text vertically within the row
        int yText = (ADDITIONAL_HEIGHT - textHeight) / 2 + ADDITIONAL_HEIGHT / 2;

        // Draw the current player text
        g2d.drawString(currentPlayer, xText, yText);
    }

    //Author : Law Li Ting
    /**
     * Opens a file chooser dialog for the user to select a location to save the game.
     * Ensures that the selected file has a `.txt` extension.
     * 
     * @return The absolute path of the selected file as a String, or "null" if the operation is canceled.
     */
    public String selectSaveFile(){
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Save Game");
        fileChooser.setFileFilter(new javax.swing.filechooser.FileNameExtensionFilter("Text Files", "txt"));
        int result = fileChooser.showSaveDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            String filename = fileChooser.getSelectedFile().getAbsolutePath();
            if (!filename.endsWith(".txt")) { // Ensure it ends with .txt
                filename += ".txt";
                return filename;
            }
            return filename;
        }
        return "null";
    }

    //Opens a file chooser dialog for the user to select a file to load
    public String selectLoadFile(){
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setDialogTitle("Load Game");
        int result = fileChooser.showOpenDialog(this);
        if (result == JFileChooser.APPROVE_OPTION) {
            String filename = fileChooser.getSelectedFile().getAbsolutePath();
            if (filename.endsWith(".txt")) { // Ensure it ends with .txt
                return filename;
            }else{
                return "null";}
        }
        return "null";
    }

    //Author : Siow Zhi Jin
    //Getter

    public int getTileSize(){
        return tileSize;
    }

    public int getXOffSet(){
        return xOffset;
    }

    public int getYOffSet(){
        return yOffset;
    }

    public int getROWS() {
        return ROWS;
    }

    public int getCOLS() {
        return COLS;
    }

    public BoardDisplay getBoardDisplay() {
        return this;
    }

    public Point getSelected(){
        return selectedTile;
    }
    
    public boolean getIsFlip(){
        return isFlipBoard;
    }

    //Setter
    public void setSelected(Point clicked){
        selectedTile = clicked;
    }

    public void setPossibleMove(List<Point> move){
        this.possibleMove = move;
    }
    
    public void setFlipBoard(boolean flip){
        this.isFlipBoard = flip;
    }
    
    //Message Dialog for error step
    public void displayErrorStepMessage(){
        JOptionPane.showMessageDialog(this, "Invalid move!\n\nChoice : \nPlease Select valid move\nClick on another chess\nClick again the selected chess", "Invalid Move", JOptionPane.ERROR_MESSAGE);
    }

    //Message Dialog for asking select a chess
    public void displaySelectPieceMessage(){
        JOptionPane.showMessageDialog(this, "Please Select a piece!", "Select Piece", JOptionPane.ERROR_MESSAGE);
    }

    //Message Dialog for selecting a invalid chess (chess color not same as player color)
    public void displayInvalidPiece(String currentPlayer){
        JOptionPane.showMessageDialog(this, "Invalid Chess selected. \nCurrent Player : " + currentPlayer, "Invalid Player", JOptionPane.ERROR_MESSAGE);
    }

    //Message Dialog for kill a chess
    public void displayKilledPiece(String currentPlayer,_Piece piece){
        JOptionPane.showMessageDialog(this, "Player " + currentPlayer + " has capture the " + piece.getColor() + " "+ piece.getType(), "CAPTURE",JOptionPane.INFORMATION_MESSAGE);
    }

    public void displayWinner(String Winner,int Turn){
        JOptionPane.showMessageDialog(this, "Player " + Winner + " WIN THE GAME!!!!\n Total Round used : " +Turn, "WINN",JOptionPane.INFORMATION_MESSAGE);
    }
    
        public void displaySave(String filename) {
        JOptionPane.showMessageDialog(this, "Game Saved Successfully!\nFile: " + filename, "Save", JOptionPane.INFORMATION_MESSAGE);
    }

    // Method to show load success message
    public void displayLoad(String filename) {
        JOptionPane.showMessageDialog(this, "Game Loaded Successfully!\nFile: " + filename, "Load", JOptionPane.INFORMATION_MESSAGE);
    }

    // Method to show error message for saving
    public void displaySaveError(String errorMessage) {
        JOptionPane.showMessageDialog(this, "Error saving game : " + errorMessage, "Error", JOptionPane.ERROR_MESSAGE);
    }

    // Method to show error message for loading
    public void displayLoadError() {
        JOptionPane.showMessageDialog(this, "Error loading game : Please select file end with .txt", "Error", JOptionPane.ERROR_MESSAGE);
    }
    
    public void displayNewGame(){
        JOptionPane.showMessageDialog(this,"New game started", "Complete",JOptionPane.INFORMATION_MESSAGE);
    }

    public void displayCancelNewGame(){
        JOptionPane.showMessageDialog(this,"You have cancel restart the game", "Cancel Restart",JOptionPane.INFORMATION_MESSAGE);
    }  
    
    public void displayCancelExitGame(){
        JOptionPane.showMessageDialog(this,"You have cancel exit the game", "Cancel Exit",JOptionPane.INFORMATION_MESSAGE);
    }    

    public int askNewGame(){
        int res =JOptionPane.showConfirmDialog(
            this,
            "Are you sure you want to start a new game? Current progress will be lost.",
            "New Game Confirmation",
            JOptionPane.YES_NO_OPTION
            );
        return res;
    }
    
    public int askEnd(){
        int res =JOptionPane.showConfirmDialog(
            this,
            "Are you sure you want to exit game? Current progress will be lost.",
            "exit Game Confirmation",
            JOptionPane.YES_NO_OPTION
            );
        return res;
    }
}