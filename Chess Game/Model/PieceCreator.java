package Model;

import Piece.*;
// Interface for the Factory Design Pattern, used to create chess pieces.
public interface PieceCreator {
    _Piece create(int x, int y, String color);
}