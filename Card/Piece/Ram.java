package Piece;

import Model.ChessModel;
import Model.GameBoard;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import javax.swing.ImageIcon;


// Author: Tee Jing Tong
// The Ram class is child class of _Piece which represents a specialized chess piece in Kawazam Chess.
// Rams move in a straight line (forward or backward) and can change direction when reaching the edge.

public class Ram extends _Piece {
    private String SReverse = "NonReverse";
    private boolean reverse;
    private boolean movingForward = true; // Tracks the movement direction (true: forward, false: backward)
    private final Image REVERSE_IMAGE;
    private final String REVERSE_IMAGE_PATH;
    //Author : Lim Jia Wei
    // Constructor
    public Ram(int row, int col, String color) {
        super(row, col, color, "Image//" + color + "Ram.png");
        this.REVERSE_IMAGE_PATH = "Image//" + color + "RamRe.png";
        this.REVERSE_IMAGE = new ImageIcon(REVERSE_IMAGE_PATH.replace("{color}", color)).getImage();
        setReverseImage(REVERSE_IMAGE);
        this.movingForward = color.equalsIgnoreCase("red"); // Red Rams move forward, Blue Rams move backward
    }

    // Toggle the movement direction
    public void flipDirection() {
        movingForward = !movingForward; // Reverse the direction
    }

    @Override
    protected List<Point> calculatePossibleMoves() {
        possibleMove = new ArrayList<>(); // Clear and initialize the list
        GameBoard gameBoard = ChessModel.getModel().getBoard();

        // Determine movement direction
        int direction = movingForward ? 1 : -1;

        // Calculate the new position based on the current direction
        int newRow = row + direction;
        int newCol = col;
        // Check if the new position is within bounds
        if (isWithinBounds(newRow, newCol)) {
            if (gameBoard.checkEnemy(newRow, newCol)) {
                possibleMove.add(new Point(newRow, newCol)); // Enemy piece is a valid move
            } else if (!gameBoard.checkBlock(newRow, newCol)) {
                possibleMove.add(new Point(newRow, newCol)); // Unblocked square is a valid move
            }
        }
        return possibleMove;
    }

    public void setReverse(boolean re){
        this.reverse = re;
    }

    public void setSReverse(String reverse){
        if(SReverse.equals("NonReverse")){
            this.SReverse = reverse;}
        else
            this.SReverse = "NonReverse";
    }

    public boolean  getReverse(){
        return  reverse;
    }

    public String getSReverse(){
        return SReverse;
    }

    // Check if the position is within bounds
    private boolean isWithinBounds(int row, int col) {
        return row >= 0 && row < 8 && col >= 0 && col < 5;
    }

    @Override
    protected String Type() {
        return "Ram";
    }
}

