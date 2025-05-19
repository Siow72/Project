package Piece;

import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import javax.swing.*;

/**
 * Abstract base class for all chess pieces in Kwazam Chess.
 */

public abstract class _Piece{
    public static _Piece piece;
    protected int maxRow;
    protected int maxCol;
    protected int row;
    protected int col;
    protected Image currentImage;
    protected Image image;
    protected Image reverseImage;
    protected String color; // "red" or "blue"
    protected List<Point> possibleMove;

    //Author : Lim Jia Wei
    //Constructor
    public _Piece(int row, int col, String color, String imagePath) {
        this.row = row;
        this.col = col;
        this.color = color;
        this.image = new ImageIcon(imagePath.replace("{color}", color)).getImage();
        this.currentImage = image;
        this.possibleMove = new ArrayList<>();
    }

    /* 
    * Draw the piece on the board.
    * @param g Graphics object for rendering.
    * @param tileSize Size of each tile in pixels.
    */
    
    public void draw(Graphics2D g, int x, int y, int tileSize) {
        g.drawImage(currentImage, x, y, tileSize, tileSize, null);
    }

    //Author : Siow Zhi Jin
    //get the type name
    protected abstract String Type();

    //calculate the possible move
    protected abstract List<Point> calculatePossibleMoves();

    //Setter
    public void setCols(int y){
        col = y;
    }

    public void setRows(int x){
        row = x;
    }

    public void setReverseImage(Image reimage){
        this.reverseImage = reimage;
    }

    public void setCurrentImage(Image curImage){
        this.currentImage = curImage;
    }

    //Getter
    public String getType(){
        return Type();
    }

    public List<Point> getPossibleMove(){
        return calculatePossibleMoves();
    }

    public String getColor(){
        return color;
    }

    public int getRows(){
        return row;
    }

    public int getCols(){
        return col;
    }

    public Image getImage(){
        return image;
    }

    public Image getReverseImage(){
        return  reverseImage;
    }

    public Image getCurrentImage(){
        return currentImage;
    }
}
