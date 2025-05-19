package Model;

import Piece.*;
import java.awt.Point;
import java.util.HashMap;
import java.util.Map;


// Model of the Kawazam Chess
// The GameBoard class represents the Model in the MVC architecture for the Kawazam Chess game.
// This class focus on the piece logic such as :

// Initializing and resetting the chessboard with all pieces.
// Handling movement, capturing, and checking for winning conditions.
// Swapping special pieces (Tor & Xor).
// Flipping the board when turns change.
// Checking for move legality (block & enemy detection).

public class GameBoard {
    private final ChessModel model;
    private final Map<Point, _Piece> PIECE_POS = new HashMap<>();
    private _Piece killedPiece;
    private boolean isKilled;
    
    //Author : Lim Jia Wei
    protected GameBoard(ChessModel model){
        this.model = model;
    }

    //add the chess to the chess board
    public void initializePieces(){
        PIECE_POS.clear();
        PIECE_POS.put(new Point(6, 0), new Ram(6, 0, "blue"));
        PIECE_POS.put(new Point(6, 1), new Ram(6, 1, "blue"));
        PIECE_POS.put(new Point(6, 2), new Ram(6, 2, "blue"));
        PIECE_POS.put(new Point(6, 3), new Ram(6, 3, "blue"));
        PIECE_POS.put(new Point(6, 4), new Ram(6, 4, "blue"));
        PIECE_POS.put(new Point(7, 1), new Biz(7, 1, "blue"));
        PIECE_POS.put(new Point(7, 3), new Biz(7, 3, "blue"));
        PIECE_POS.put(new Point(7, 0), new Tor(7, 0, "blue"));
        PIECE_POS.put(new Point(7, 4), new Xor(7, 4, "blue"));
        PIECE_POS.put(new Point(7, 2), new Sau(7, 2, "blue"));
        PIECE_POS.put(new Point(1, 0), new Ram(1, 0, "red"));
        PIECE_POS.put(new Point(1, 1), new Ram(1, 1, "red"));
        PIECE_POS.put(new Point(1, 2), new Ram(1, 2, "red"));
        PIECE_POS.put(new Point(1, 3), new Ram(1, 3, "red"));
        PIECE_POS.put(new Point(1, 4), new Ram(1, 4, "red"));
        PIECE_POS.put(new Point(0, 1), new Biz(0, 1, "red"));
        PIECE_POS.put(new Point(0, 3), new Biz(0, 3, "red"));
        PIECE_POS.put(new Point(0, 0), new Tor(0, 0, "red"));
        PIECE_POS.put(new Point(0, 4), new Xor(0, 4, "red"));
        PIECE_POS.put(new Point(0, 2), new Sau(0, 2, "red"));
    }

    //Author : Siow Zhi Jin
    //check got other piece block the move (can't skip the chess)
    public boolean checkBlock(int row, int col) {
        Point point = new Point(row, col);
        _Piece piece = PIECE_POS.get(point);
        return piece != null && piece.getColor().equals(model.getState().getcurrentPlayer());
    }

    //Check for enemies in the possible move
    public boolean checkEnemy(int row, int col) {
        Point point = new Point(row, col);
        _Piece piece = PIECE_POS.get(point);
        return piece != null && !piece.getColor().equals(model.getState().getcurrentPlayer());
    }

        //Logic for moving selected piece to new position + check for winner when capturing Sau    
    public void movePiece(Point selectedPiece, Point moveTo){
        _Piece needMovePiece = PIECE_POS.get(selectedPiece);
        if(PIECE_POS.get(moveTo) != null){
            killedPiece = PIECE_POS.get(moveTo);
            isKilled = true;
            if(killedPiece instanceof Sau){
                model.getState().setWinner(needMovePiece.getColor());
            }
        }
        PIECE_POS.remove(selectedPiece);
        PIECE_POS.put(moveTo, needMovePiece);
        needMovePiece.setCols(moveTo.y);
        needMovePiece.setRows(moveTo.x);
    }

    //swap Tor to Xor (vice-versa)
    public void swapTorXor() {
        // Store positions of pieces to swap
        Map<Point, _Piece> swaps = new HashMap<>();
    
        for (Map.Entry<Point, _Piece> entry : PIECE_POS.entrySet()) {
            Point pos = entry.getKey();
            _Piece piece = entry.getValue();
    
            if (piece instanceof Tor) {
                swaps.put(pos, new Xor(piece.getRows(), piece.getCols(), piece.getColor()));
            } else if (piece instanceof Xor) {
                swaps.put(pos, new Tor(piece.getRows(), piece.getCols(), piece.getColor()));
            }
        }
        // Apply swaps
        PIECE_POS.putAll(swaps);
    }    

    //Author : Siow Zhi Jin + Tee Jing Tong
    //logic for flipping the board 
    public void flipBoard() {
        Map<Point, _Piece> flippedPositions = new HashMap<>();
        int maxRows = 7; // Assuming a board with 8 rows (indexed 0 to 7)
        int maxCols = 4; // Assuming a board with 5 columns (indexed 0 to 4)
    
        for (Map.Entry<Point, _Piece> entry : PIECE_POS.entrySet()) {
            Point originalPos = entry.getKey();
            _Piece piece = entry.getValue();
    
            // Calculate the flipped position
            int flippedRow = maxRows - originalPos.x;
            int flippedCol = maxCols - originalPos.y;
            Point flippedPoint = new Point(flippedRow, flippedCol);
    
            // Update the piece's internal row and column
            piece.setRows(flippedRow);
            piece.setCols(flippedCol);
            
            checkPiece(piece);

            if(piece instanceof Ram ram&& (originalPos.x == 0 || originalPos.x == 7)){
                if(!ram.getReverse()) {
                    ram.setReverse(true);
                    ram.setSReverse("Reverse");
                    checkPiece(piece);
                }
            }
            // Add to the new map
            flippedPositions.put(flippedPoint, piece);
        }
    
        // Replace the original positions with the flipped ones
        PIECE_POS.clear();
        PIECE_POS.putAll(flippedPositions);
    }

    public void checkPiece(_Piece piece){
        if (piece instanceof Ram || piece instanceof Sau) {
            if(piece instanceof Ram ramPiece){
                ramPiece.flipDirection();} // Reverse the movement direction
            if(piece.getCurrentImage().equals(piece.getImage()))
                piece.setCurrentImage(piece.getReverseImage());
            else 
                piece.setCurrentImage(piece.getImage());   
        }
    }
    
    //Setter
    public void setKill(boolean isKilled){
        this.isKilled = isKilled;
    }

    public void setKillPiece(_Piece piece){
        this.killedPiece = piece;
    }

    //Getter
    public Map<Point, _Piece> getPiecePositions() {
        return PIECE_POS;
    }

    public boolean getKill(){
        return isKilled;
    }

    public _Piece getKilledPiece(){
        return killedPiece;
    }
}
