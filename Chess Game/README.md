# Kwazam Chess Game

### CCP6224 Object-Oriented Analysis and Design — Trimester 2410

A Java GUI-based implementation of **Kwazam Chess**, a strategic two-player game with unique transformation mechanics. This project was developed using robust object-oriented design principles and follows the **Model-View-Controller (MVC)** pattern. The application includes a graphical interface, save/load features, and dynamic piece transformation to offer an engaging, custom chess experience.

---

##  Game Description

Kwazam Chess is played on a **5×8 board** with the following custom pieces:

- **Ram**: Moves 1 step forward. Turns around upon reaching the end of the board.
- **Biz**: Moves in an L-shape (3×2) like a knight. Can jump over pieces.
- **Tor**: Moves any number of spaces horizontally/vertically. Transforms into Xor after 2 turns.
- **Xor**: Moves diagonally. Transforms into Tor after 2 turns.
- **Sau**: Moves 1 step in any direction. Capturing it ends the game.

> Only the Biz piece may skip over others. All others cannot pass through pieces.

After every 2 full turns (1 red + 1 blue move), all **Tor ↔ Xor** pieces transform.

---

##  Key Features

- Java GUI with user-friendly interface
- Fully functioning 2-player Kwazam Chess gameplay
- Piece transformation mechanic (Tor ↔ Xor)
- Turn indicator with **screen flipping**
- Save and load game to/from **human-readable `.txt` files**
- Responsive GUI with **window resizing support**
- Follows **MVC pattern** and includes **additional design patterns** 

---

##  Design Patterns Used

- **MVC Pattern**: Separation of Model (game logic), View (GUI), and Controller (input handling)
- **Factory Pattern**: For centralized state or configuration management

---

##  Compile & Run Instructions
- ** run with CHessMain.Java
