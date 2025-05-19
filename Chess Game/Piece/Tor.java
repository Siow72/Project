package Piece;

import Model.ChessModel;
import Model.GameBoard;
import java.awt.*;
import java.util.List;


 //The Tor class represents a rook-like piece in Kawazam Chess.
 //The Tor moves in straight lines (horizontally and vertically) until blocked.
 
public class Tor extends _Piece {
    //Author : Lim Jia Wei
    //Constructor
    public Tor(int row, int col, String color) {
        super(row, col, color, "Image//{color}Tor.png");
     }
  
    //Author : Siow Zhi Jin
    //calculate the possible move for Tor
    @Override
    protected List<Point> calculatePossibleMoves() {
        possibleMove.clear();
        GameBoard gameBoard = ChessModel.getModel().getBoard();
        int[][] directions = {
            {1, 0},   // up
            {-1, 0},  // down
            {0, 1},  // left
            {0, -1}   // right
        };

        for (int[] dir : directions) {
            int dRow = dir[0];
            int dCol = dir[1];
            for (int i = 1; i < 8; i++) {
                int newRow = row + i * dRow;
                int newCol = col + i * dCol;
                if (newRow < 0 || newRow >= 8 || newCol < 0 || newCol >= 5) break; // Out of bounds
                if (gameBoard.checkBlock(newRow, newCol)) break; // Block encountered
                if (gameBoard.checkEnemy(newRow,newCol)) { // find the enemy
                    possibleMove.add(new Point(newRow, newCol));
                    break;
                }
                possibleMove.add(new Point(newRow, newCol));
            }
        }    
        return possibleMove;
    }

    //Getter
    @Override
    protected String Type() {
        return "Tor";
    };
}
