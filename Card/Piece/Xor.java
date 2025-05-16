
package Piece;

import Model.ChessModel;
import Model.GameBoard;
import java.awt.*;
import java.util.List;

//  The Xor class represents a bishop-like piece in Kawazam Chess.
//  The Xor moves diagonally across the board until blocked.

public class Xor extends _Piece{
    //Author : Lim Jia Wei
    //Constructor
    public Xor(int row, int col, String color) {
        super(row, col, color, "Image//{color}Xor.png");

    }
  
    //Author : Siow Zhi Jin
    //calculate the possible move for Xor
    @Override
    protected List<Point> calculatePossibleMoves() {
        possibleMove.clear();
        GameBoard gameBoard = ChessModel.getModel().getBoard();
        int[][] directions = {
            {1, 1},   // Down-right
            {-1, -1}, // Up-left
            {1, -1},  // Down-left
            {-1, 1}   // Up-right
        };

        for (int[] dir : directions) {
            int dRow = dir[0];
            int dCol = dir[1];
            for (int i = 1; i < 8; i++) {
                int newRow = row + i * dRow;
                int newCol = col + i * dCol;
                if (newRow < 0 || newRow >= 8 || newCol < 0 || newCol >= 5) break; // Out of bounds
                if (gameBoard.checkBlock(newRow, newCol)) break; // Block encountered
                if (gameBoard.checkEnemy(newRow,newCol)) {
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
        return "Xor";
    };
}
