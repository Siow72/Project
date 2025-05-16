package Controller;

import Model.ChessModel;
import Piece.*;
import View.*;
import java.awt.BorderLayout;
import java.awt.Point;
import java.awt.event.*;
import java.util.*;
import javax.swing.*;

//Controller of the Kawazam Chess :
//Responsible for handling user interactions and updating the view and model accordingly.

public class ChessController {
    private final ChessModel model;
    private final MenuBar menu;
    private final JFrame frame;
    private final BoardDisplay boardDisplay;
    private String filename, getSaveString;
    private boolean isFirstClicked,checkStep;
    private List<Point> move;
    private _Piece firstClickedPiece;

    //Author : Siow Zhi Jin
    //Constructor
    public ChessController(StartPage view) {
        this.menu = new MenuBar();
        this.model = ChessModel.getModel();
        this.frame = view.getFrame();
        this.boardDisplay = new BoardDisplay(model);

        // Add listeners to buttons
        view.getStartButton().addActionListener(new StartButtonListener());
        view.getLoadButton().addActionListener(new ViewLoadButtonListener());
        view.getHelpButton().addActionListener(new HelpButtonListener());
        view.getExitButton().addActionListener(new ExitButtonListener());

        // menu bar listeners
        menu.getExitItem().addActionListener(new ExitButtonListener());
        menu.getHelpItem().addActionListener(new HelpButtonListener());
        menu.getLoadItem().addActionListener(new MenuLoadItemListener());
        menu.getSaveItem().addActionListener(new SaveButtonListener());
        menu.getNewGame().addActionListener(new NewGameButtonListener());
        
        // Add a listener to the board
        boardDisplay.addMouseListener(new BoardMouseListener());
    }

    // Author : Siow Zhi Jin
    //start a new game
    private class NewGameButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent evt) {
            int response = boardDisplay.askNewGame();
            if (response == JOptionPane.YES_OPTION) {
                model.getBoard().initializePieces();
                clearAll();
                frame.repaint();
                boardDisplay.displayNewGame();
            }else
            boardDisplay.displayCancelExitGame();
        }
    }

    //Author : Lim Jia Wei
    // Listener for the Start button
    private class StartButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent evt) {
            frame.add(boardDisplay, BorderLayout.CENTER);
            frame.setJMenuBar(menu.getMenu());
            frame.setContentPane(boardDisplay);
            frame.pack(); // Automatically adjusts the frame to fit the new content
            frame.setLocationRelativeTo(null); // Center the frame on the screen
            frame.revalidate(); // Refresh the frame
            frame.repaint(); // Redraw the frame

        }
    }
    
    //Author : Law Li Ting
    private class ViewLoadButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent evt) {
            frame.add(boardDisplay, BorderLayout.CENTER);
            frame.setJMenuBar(menu.getMenu());
            frame.setContentPane(boardDisplay);
            frame.pack(); // Automatically adjusts the frame to fit the new content
            frame.setLocationRelativeTo(null); // Center the frame on the screen
            frame.revalidate(); // Refresh the frame
            frame.repaint(); // Redraw the frame
            loadGame();
        }
    }


    // Listener for the Load button
    private class MenuLoadItemListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent evt) {            
            loadGame();
        }
    }

    private class SaveButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent evt) {
            filename = boardDisplay.selectSaveFile();
            if(!filename.equals("null")){
                getSaveString = model.saveGame(filename);
                if (getSaveString.equals(filename))
                    boardDisplay.displaySave(getSaveString);
                else
                    boardDisplay.displaySaveError(getSaveString);
            }
        }
    }

    //Author : Lim Jia Wei
    // Listener for the Help button
    private class HelpButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent evt) {
            new HelpDisplay();
        }
    }

    //Author : Lim Jia Wei
    // Listener for the Exit button
    private class ExitButtonListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent evt) {
            int response = boardDisplay.askEnd();
            if (response == JOptionPane.YES_OPTION) {
                System.exit(0);
            }else
            boardDisplay.displayCancelExitGame();
        }
    }

    //Author : Siow Zhi Jin
    // Listener for mouse clicks on the board
    private class BoardMouseListener extends MouseAdapter {
        @Override
        public void mouseClicked(MouseEvent e) {
            // Calculate the clicked tile
            int col = (e.getX() - boardDisplay.getXOffSet()) / boardDisplay.getTileSize();
            int row = (e.getY() - boardDisplay.getYOffSet()) / boardDisplay.getTileSize();
            Point clickedTile = new Point(row, col);

            // set the clicked piece
            _Piece clickedPiece = model.getBoard().getPiecePositions().get(clickedTile);
            //check the game is end or not
            if(!model.getState().getIsWinner()){
                //call firstclick function if is first click
                if (!isFirstClicked && clickedPiece != null)
                    firstClick(clickedPiece,clickedTile);
                    //call secondclick function if there is a second click
                else if (isFirstClicked){
                    secondClick(clickedPiece,clickedTile);
                }
                else
                    boardDisplay.displaySelectPieceMessage();
            }else
                boardDisplay.displayWinner(model.getState().getWinner(),model.getState().getTurn());
            // Repaint the board to show any updates
            boardDisplay.repaint();
            }
        }

    //Author : Law Li Ting
    //handle the load game 
    private void loadGame(){
        filename = boardDisplay.selectLoadFile();
        if (!filename.equals("null")){
            model.loadGame(filename);
            boardDisplay.displayLoad(filename);
            boardDisplay.repaint(); // Repaint the board to reflect the loaded game
        }else
        boardDisplay.displayLoadError();
    }
    
    //Author : Siow Zhi Jin
    //Clear all the used variable without state
    private void clear(){
        boardDisplay.setPossibleMove(null);
        boardDisplay.setSelected(null);
        model.getBoard().setKill(false);
        model.getBoard().setKillPiece(null);
        firstClickedPiece = null;
        isFirstClicked = false;
        checkStep = false;
    }

    // clear all include the state
    private void clearAll(){
        boardDisplay.setPossibleMove(null);
        boardDisplay.setSelected(null);
        model.getBoard().setKill(false);
        model.getBoard().setKillPiece(null);
        firstClickedPiece = null;
        isFirstClicked = false;
        checkStep = false;
        model.getState().resetState();
    }

    // Checks the current player and flips the board.
    private void setFlip(){
        model.getState().nextPlayer();
        String player = model.getState().getcurrentPlayer();
        if(player.equals("blue"))
            boardDisplay.setFlipBoard(false);
        else
            boardDisplay.setFlipBoard(true);
        model.getBoard().flipBoard();
    }

    //Handle the first click logic
    private void firstClick(_Piece piece, Point tile) {
        //select the correct chess color
        if(model.getState().getcurrentPlayer().equals(piece.getColor())){
            firstClickedPiece = piece;
            move = piece.getPossibleMove();
            boardDisplay.setPossibleMove(move);
            boardDisplay.setSelected(tile);
            isFirstClicked = true;
        }else// incorrect chess color
            boardDisplay.displayInvalidPiece(model.getState().getcurrentPlayer());
    }
    
    //Handle the second click logic
    private void secondClick(_Piece piece,Point tile){
        //check the player select the Valid move or not
        for (Point m : move) {
            if (tile.equals(m)) {
                checkStep = true;
                break;
            }
        }

        //when click on the same chess (unselect the piece and clear the used variable)
        if(firstClickedPiece.equals(piece)){
            clear();
        }

        //player select the Valid move
        else if(checkStep){
            model.getBoard().movePiece(boardDisplay.getSelected(), tile);
            if(model.getBoard().getKill()) boardDisplay.displayKilledPiece(model.getState().getcurrentPlayer(),piece);
            if(model.getBoard().getKilledPiece() instanceof Sau) boardDisplay.displayWinner(model.getState().getWinner(),model.getState().getTurn());
            if (firstClickedPiece instanceof Ram ram) 
                if ((tile.x == 0 || tile.x == 7)&&ram.getReverse()){ 
                    ram.setReverse(false);  
                    ram.setSReverse("NonReverse");
                }   
            setFlip();
            clear();
        }
        //select different chess (clear the last piece's data and load the new piece)
        else if(piece != null){
            clear();
            firstClick(piece, tile);
        }
        //player select the invalid move
        else
            boardDisplay.displayErrorStepMessage();
        }
    }
