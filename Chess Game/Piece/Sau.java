package Piece;

import Model.ChessModel;
import Model.GameBoard;
import java.awt.*;
import java.util.List;
import javax.swing.ImageIcon;

// The Sau class is child class of _Piece which represents a specialized chess piece in Kawazam Chess.
// The Sau moves one step in any direction (similar to a King in standard chess).

public class Sau extends _Piece {
    private final Image REVERSE_IMAGE;
    private final String REVERSE_IMAGE_PATH;
    //Author : Lim Jia Wei
    //Constructor
    public Sau(int row, int col, String color) {
        super(row, col, color, "Image//" + color + "Sau.png");
        this.REVERSE_IMAGE_PATH = "Image//" + color + "SauRe.png";
        this.REVERSE_IMAGE = new ImageIcon(REVERSE_IMAGE_PATH.replace("{color}", color)).getImage();
        setReverseImage(REVERSE_IMAGE);
        
    }
    // Author: Tee Jing Tong

    // Calculate the possible moves for Sau
    @Override
    protected List<Point> calculatePossibleMoves() {
        possibleMove.clear();
        GameBoard gameBoard = ChessModel.getModel().getBoard();
        
        // Sau can move one step in any cardinal direction
        int[][] directions = {
            {1, 0},   // down
            {-1, 0},  // up
            {0, 1},   // right
            {0, -1},   // left
            {1,-1},
            {1,1},
            {-1,-1},
            {-1,1}
        };

        // Loop through all possible directions
        for (int[] dir : directions) {
            int newRow = row + dir[0];
            int newCol = col + dir[1];

            // Check if the move is within bounds
            if (newRow >= 0 && newRow < 8 && newCol >= 0 && newCol < 5) {
                // If the square is occupied by an enemy, add it and stop
                if (gameBoard.checkEnemy(newRow, newCol)) {
                    possibleMove.add(new Point(newRow, newCol));
                }
                // If the square is not blocked, add it
                else if (!gameBoard.checkBlock(newRow, newCol)) {
                    possibleMove.add(new Point(newRow, newCol));
                }
            }
        }

        return possibleMove;
    }

    // Getter for the type
    @Override
    protected String Type() {
        return "Sau";
    }
}

