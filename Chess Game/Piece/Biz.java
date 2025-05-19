package Piece;

import Model.ChessModel;
import Model.GameBoard;
import java.awt.*;
import java.util.List;

// The Biz class is child class of _Piece which represents a specialized chess piece in Kawazam Chess.
// This Biz class handle the Biz's move
// This piece moves in an "L" shape, similar to a knight in standard chess.

public class Biz extends _Piece {
    //Author : Lim Jia Wei
    //Constructor
    public Biz(int row, int col, String color) {
        super(row, col, color, "Image//{color}Biz.png");
    }
    // Author: Tee Jing Tong

    @Override
    protected List<Point> calculatePossibleMoves() {
        possibleMove.clear();
        GameBoard gameBoard = ChessModel.getModel().getBoard();

        // Define knight-like L-shaped movement directions
        int[][] directions = {
            {2, -1}, {2, 1}, 
            {-2, -1}, {-2, 1},
            {1, -2}, {1, 2}, 
            {-1, -2}, {-1, 2}
        };

        // Loop through each direction and calculate moves
        for (int[] dir : directions) {
            int dRow = dir[0];
            int dCol = dir[1];
            int newRow = row + dRow;
            int newCol = col + dCol;

            // Check for out-of-bounds
            if (newRow < 0 || newRow >= 8 || newCol < 0 || newCol >= 5) continue;

            // Check for obstacles
            if (gameBoard.checkBlock(newRow, newCol)) continue;

            // Check for enemies
            if (gameBoard.checkEnemy(newRow, newCol)) {
                possibleMove.add(new Point(newRow, newCol));
            } else {
                possibleMove.add(new Point(newRow, newCol));
            }
        }
        return possibleMove;
    }

    @Override
    protected String Type() {
        return "Biz";
    }
}