package Model;

import Piece.*;
import java.awt.Point;
import java.io.*;
import java.util.*;

// Model of the Kawazam Chess
// The ChessModel class represents the Model in the MVC architecture for the Kawazam Chess game.
// It is responsible for managing the game state, handling piece positions, and saving/loading game data.
public class ChessModel {    
    private String color;
    private _Piece loadPiece;
    private final List<_Piece> LOAD_PIECE_LIST;
    private final GameBoard G_BOARD;
    private final GameState G_STATE;
    private final ChessPieceFactory PIECE_FACTORY;
    private static ChessModel instance;

    //Author : Siow Zhi Jin
    // Constructor for chess model
    public ChessModel(){
        this.G_BOARD = new GameBoard(this);
        G_BOARD.initializePieces();
        this.G_STATE = new GameState(G_BOARD);
        this.LOAD_PIECE_LIST = new ArrayList<>();
        this.PIECE_FACTORY = new ChessPieceFactory();
    }

    // Getter for model
    //implement of singleton pattern - ensure that
    //chessmodel only have one instance in whole program
    public static ChessModel getModel() {
        if (instance == null) {
            instance = new ChessModel();
        }
        return instance;
    }

    // Getter for board
    public GameBoard getBoard(){
        return G_BOARD;
    }

    // Getter for game state
    public GameState getState(){
        return G_STATE;
    }
    
    //Author : Law Li Ting
    // Save game to file
    public String saveGame(String filename) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            // Save pieces
            Map<Point, _Piece> piecePos = G_BOARD.getPiecePositions();
            for (Map.Entry<Point, _Piece> entry : piecePos.entrySet()) {
                Point point = entry.getKey();
                _Piece piece = entry.getValue();
                if (piece instanceof Ram ram) {
                    writer.write(piece.getType() + " " + point.x + " " + point.y + " " + piece.getColor() + " " + ram.getSReverse());
                } else {
                    writer.write(piece.getType()+ " " + point.x + " " + point.y + " " + piece.getColor());
                }
                writer.newLine();  // New line after each piece's data
            }
            writer.write("Current Player: " + G_STATE.getcurrentPlayer());
            writer.newLine();
            writer.write("Current Turn: " + G_STATE.getTurn());  // Save the current turn
            writer.newLine();
            return filename;
        } catch (IOException e) {
            e.printStackTrace();
            return e.getMessage();
        }
    }

    // Load game from file 
    public String loadGame(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            Map<Point, _Piece> piecePos = G_BOARD.getPiecePositions();
            piecePos.clear();  // Clear current board before loading
            
            // Load pieces from file
            while ((line = reader.readLine()) != null) {
                if (line.startsWith("Current Player: ")) {
                    String getcurrentPlayer = line.substring("Current Player: ".length());
                    G_STATE.setCurrentPlayer(getcurrentPlayer);  // Correctly set the current player
                } else if (line.startsWith("Current Turn: ")) {  // Fixed syntax error here
                    String getTurn = line.substring("Current Turn: ".length());
                    G_STATE.setTurn(Integer.parseInt(getTurn));  // Correctly set the current turn
                } else {
                    String[] parts = line.split(" ");
                    if (parts.length == 4||parts.length == 5) {
                        String pieceType = parts[0];
                        int x = Integer.parseInt(parts[1]);
                        int y = Integer.parseInt(parts[2]);
                        color = parts[3];
                        loadPiece = PIECE_FACTORY.createPiece(pieceType, x, y, color);
                        if(loadPiece != null)
                        {    
                            if (loadPiece instanceof Ram ram && parts.length == 5) {
                                String reverse = parts[4];
                                if ("Reverse".equals(reverse)) {
                                    getBoard().checkPiece(ram);
                                    ram.setReverse(true);
                                    ram.setSReverse(reverse);
                                }
                            }
                            LOAD_PIECE_LIST.add(loadPiece);
                            piecePos.put(new Point(x, y), loadPiece);
                        }
                    }
                }
            }

            if(color.equals("red")){
                for(_Piece loadPieceCheck : LOAD_PIECE_LIST)
                    getBoard().checkPiece(loadPieceCheck);
            }
            
            return filename;
            // Call BoardDisplay to show the success message
        } catch (IOException e) {
            // Call BoardDisplay to show the error message
            return e.getMessage();
        }
    }
}
