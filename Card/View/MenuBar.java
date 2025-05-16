package View;
import java.awt.*;
import javax.swing.*;

// Author : Law Li Ting

//View of the Kawazam Chess game
//HelpDisplay focus on display the GUI of the menu bar at the top of the game board

public class MenuBar extends JFrame{
    private final JMenuBar MENU_BAR;
    private final JMenuItem SAVE_ITEM;
    private final JMenuItem LOAD_ITEM;
    private final JMenuItem EXIT_ITEM;
    private final JMenuItem HELP_ITEM;
    private final JMenuItem NEW_ITEM;

    // Constructor
    public MenuBar() {
        MENU_BAR = new JMenuBar();

        // File menu
        JMenu fileMenu = new JMenu("File");
        NEW_ITEM = new JMenuItem("New Game");
        SAVE_ITEM = new JMenuItem("Save Game");
        LOAD_ITEM = new JMenuItem("Load Game");
        EXIT_ITEM = new JMenuItem("Exit");

        fileMenu.add(NEW_ITEM);
        fileMenu.add(SAVE_ITEM);
        fileMenu.add(LOAD_ITEM);
        fileMenu.addSeparator();
        fileMenu.add(EXIT_ITEM);

        // Add File menu to menu bar
        MENU_BAR.add(fileMenu);

        // Help menu
        JMenu helpMenu = new JMenu("Help");
        HELP_ITEM = new JMenuItem("Rules");
        helpMenu.add(HELP_ITEM);

        // Add Help menu to menu bar
        MENU_BAR.add(helpMenu);

        setLayout(new BorderLayout());
        JTextField hi= new JTextField("hinoa");
        add(hi);
    }

    // Getter for menu bar
    public JMenuBar getMenu() {
        return MENU_BAR;
    }

    public JMenuItem getNewGame(){
        return NEW_ITEM;
    }

    public JMenuItem getSaveItem(){
        return SAVE_ITEM;
    }
    public JMenuItem getLoadItem(){
        return LOAD_ITEM;
    }
    public JMenuItem getExitItem(){
        return EXIT_ITEM;
    }
    public JMenuItem getHelpItem(){
        return HELP_ITEM;
    }

}
