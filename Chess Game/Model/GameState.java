package Model;

// Model of the Kawazam Chess
// The GameState class represents the Model in the MVC architecture for the Kawazam Chess game.
// This class focus on modify the game's state during game play
// Including tracking turns, determining the current player, and handling win conditions.

public class GameState {
    private final GameBoard gameBoard;
    private String currentPlayer;
    private boolean isWinner;
    private int currentTurn;
    private String Winner;
    private final String P1 ="blue"; // blue
    private final String P2 = "red"; // red

    //Author : Siow Zhi Jin
    //Constructor
    public GameState(GameBoard gameBoard) 
    {
        this.gameBoard = gameBoard;
        this.isWinner = false;
        this.Winner =null;
        this.currentTurn = 0;
        this.currentPlayer = P1;
    }
    
    //check for the next player
    public void nextPlayer(){
        currentTurn++;
        if(currentPlayer.equals(P1))
            currentPlayer = P2;
        else
            currentPlayer = P1;

        //call every 2 turn
        if(currentTurn % 4 == 0){
            gameBoard.swapTorXor();}
    }

    public void resetState(){
        this.isWinner = false;
        this.Winner =null;
        this.currentTurn = 0;
        this.currentPlayer = P1;
    }

    public void setWinner(String Winner){
        this.Winner = Winner;
        isWinner = true;
    }

    public void setTurn(int turn){
        this.currentTurn = turn;
    }
    
    public void setCurrentPlayer(String currentPlayer) {
        this.currentPlayer = currentPlayer;
    }
    
    //Getter
    public String getcurrentPlayer(){
        return currentPlayer;
    }

    public int getTurn(){
        return currentTurn;
    }

    public String getP1(){
        return P1;
    }

    public String getP2(){
        return P2;
    }

    public String getWinner(){
        return Winner;
    }

    public boolean getIsWinner(){
        return  isWinner;
    }
}
