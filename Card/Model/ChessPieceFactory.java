package Model;

import Piece.*;
import java.util.HashMap;
import java.util.Map;


//Author : Law Li Ting
public class ChessPieceFactory {
    private final Map<String, PieceCreator> pieceRegistry = new HashMap<>();

    public ChessPieceFactory() {
        // Register creator classes for each piece type
        registerPiece("Ram", new RamCreator());
        registerPiece("Biz", new BizCreator());
        registerPiece("Tor", new TorCreator());
        registerPiece("Xor", new XorCreator());
        registerPiece("Sau", new SauCreator());
    }

    // Register a new piece type
    private void registerPiece(String pieceType, PieceCreator creator) {
        pieceRegistry.put(pieceType, creator);
    }
    
    // Factory method to create a piece
    public _Piece createPiece(String pieceType, int x, int y, String color) {
        PieceCreator creator = pieceRegistry.get(pieceType);
        if (creator == null) {
            return null;
        }
        return creator.create(x, y, color);
    }

    // Inner creator classes for each piece
    public class RamCreator implements PieceCreator {
        @Override
        public _Piece create(int x, int y, String color) {
            return new Ram(x, y, color);
        }
    }
    
    public class BizCreator implements PieceCreator {
        @Override
        public _Piece create(int x, int y, String color) {
            return new Biz(x, y, color);
        }
    }
    
    public class TorCreator implements PieceCreator {
        @Override
        public _Piece create(int x, int y, String color) {
            return new Tor(x, y, color);
        }
    }
    
    public class XorCreator implements PieceCreator {
        @Override
        public _Piece create(int x, int y, String color) {
            return new Xor(x, y, color);
        }
    }
    
    public class SauCreator implements PieceCreator {
        @Override
        public _Piece create(int x, int y, String color) {
            return new Sau(x, y, color);
        }
    }
}
