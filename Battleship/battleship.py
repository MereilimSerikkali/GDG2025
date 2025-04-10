import tkinter as tk
from tkinter import messagebox
import random


class Battleship:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")
        self.board_size = 6
        self.ship_position = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
        self.create_board()
    
    def create_board(self):
        self.buttons = [[tk.Button(self.root, width=4, height=2, bg='blue', command=lambda x=i, y=j: self.button_click(x, y))
                        for j in range(self.board_size)]
                        for i in range(self.board_size)]
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].grid(row=i, column=j)
                
    def button_click(self, x, y):
        if(x, y) == self.ship_position:
            self.buttons[x][y].config(bg='red', state=tk.DISABLED)
            messagebox.showinfo("Battleship Game", "You won!")
            self.root.destroy()
        else:
            self.buttons[x][y].config(bg='white', state=tk.DISABLED)
            messagebox.showinfo("Battleship Game", "Miss!")
            
def main():
    root = tk.Tk()
    game = Battleship(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()