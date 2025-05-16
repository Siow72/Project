import Controller.*;
import View.*;

//Start at here :)
public class ChessMain {
 public static void main(String[] args) {
     StartPage view = new StartPage();
     new ChessController(view);
 }   
}
