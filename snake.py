#!/usr/bin/env python3
"""
Simple Snake Game
Use WASD or arrow keys to control the snake
Press 'q' to quit
"""

import curses
import random
import time

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        self.width -= 1  # Account for border
        self.height -= 1  # Account for border
        
        # Initialize snake
        self.snake = [(self.height // 2, self.width // 2)]
        self.direction = (0, 1)  # Moving right initially
        
        # Initialize food
        self.food = self.generate_food()
        
        # Game state
        self.score = 0
        self.game_over = False
        
        # Set up curses
        curses.curs_set(0)  # Hide cursor
        stdscr.nodelay(1)  # Non-blocking input
        stdscr.timeout(100)  # Refresh rate
        
    def generate_food(self):
        """Generate food at a random location not occupied by snake"""
        while True:
            food = (random.randint(1, self.height - 2), 
                   random.randint(1, self.width - 2))
            if food not in self.snake:
                return food
    
    def move_snake(self):
        """Move snake in current direction"""
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check wall collision
        if (new_head[0] <= 0 or new_head[0] >= self.height - 1 or
            new_head[1] <= 0 or new_head[1] >= self.width - 1):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 1
            self.food = self.generate_food()
        else:
            self.snake.pop()  # Remove tail if no food eaten
    
    def handle_input(self):
        """Handle user input"""
        key = self.stdscr.getch()
        
        # Quit game
        if key == ord('q') or key == ord('Q'):
            self.game_over = True
            return
        
        # Direction controls (prevent reversing into self)
        if key == curses.KEY_UP or key == ord('w') or key == ord('W'):
            if self.direction != (1, 0):  # Not moving down
                self.direction = (-1, 0)
        elif key == curses.KEY_DOWN or key == ord('s') or key == ord('S'):
            if self.direction != (-1, 0):  # Not moving up
                self.direction = (1, 0)
        elif key == curses.KEY_LEFT or key == ord('a') or key == ord('A'):
            if self.direction != (0, 1):  # Not moving right
                self.direction = (0, -1)
        elif key == curses.KEY_RIGHT or key == ord('d') or key == ord('D'):
            if self.direction != (0, -1):  # Not moving left
                self.direction = (0, 1)
    
    def draw(self):
        """Draw the game state"""
        self.stdscr.clear()
        
        # Draw border
        for i in range(self.height):
            self.stdscr.addch(i, 0, '#')
            self.stdscr.addch(i, self.width - 1, '#')
        for j in range(self.width):
            self.stdscr.addch(0, j, '#')
            self.stdscr.addch(self.height - 1, j, '#')
        
        # Draw snake
        for i, (y, x) in enumerate(self.snake):
            if i == 0:  # Head
                self.stdscr.addch(y, x, '@')
            else:  # Body
                self.stdscr.addch(y, x, 'o')
        
        # Draw food
        self.stdscr.addch(self.food[0], self.food[1], '*')
        
        # Draw score
        score_text = f"Score: {self.score}"
        self.stdscr.addstr(0, 2, score_text)
        
        # Draw controls
        controls = "WASD/Arrows: Move | Q: Quit"
        if len(controls) < self.width - 2:
            self.stdscr.addstr(self.height - 1, 2, controls)
        
        self.stdscr.refresh()
    
    def run(self):
        """Main game loop"""
        while not self.game_over:
            self.handle_input()
            self.move_snake()
            self.draw()
            time.sleep(0.1)
        
        # Game over screen
        self.stdscr.clear()
        game_over_text = "GAME OVER!"
        score_text = f"Final Score: {self.score}"
        restart_text = "Press any key to exit..."
        
        # Center the text
        y_center = self.height // 2
        x_center = self.width // 2
        
        self.stdscr.addstr(y_center - 1, x_center - len(game_over_text) // 2, game_over_text)
        self.stdscr.addstr(y_center, x_center - len(score_text) // 2, score_text)
        self.stdscr.addstr(y_center + 1, x_center - len(restart_text) // 2, restart_text)
        
        self.stdscr.refresh()
        self.stdscr.nodelay(0)  # Blocking input
        self.stdscr.getch()  # Wait for any key

def main(stdscr):
    """Main function to be called by curses.wrapper"""
    game = SnakeGame(stdscr)
    game.run()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Make sure your terminal supports curses and is large enough for the game.")
