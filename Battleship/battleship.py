import tkinter as tk
from tkinter import messagebox
import random


class Battleship:
    def __init__(self, root):
        self.root = root
        self.root.title("Battleship Game")
        self.board_size = 6
        self.enemy_board_size = self.board_size
        self.turn = 1
        self.ship_position_enemy = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
        self.ship_position_player = (random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1))
        self.create_board()
        
    
    def create_board(self):
        self.buttons = [[tk.Button(self.root, width=4, height=2, bg='blue', command=lambda x=i, y=j: self.button_click(x, y))
                        for j in range(self.board_size)]
                        for i in range(self.board_size)]
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].grid(row=i, column=j)
                
        self.buttons[self.ship_position_player[0]][self.ship_position_player[1]].config(bg='green', state=tk.DISABLED)
    
                
    def button_click(self, x, y):
        if self.turn == 1:
            if(x, y) == self.ship_position_enemy:
                self.buttons[x][y].config(bg='red', state=tk.DISABLED)
                messagebox.showinfo("Battleship Game", "You won!")
                self.root.destroy()
                
            elif(x, y) == self.ship_position_player:
                messagebox.showinfo("Battleship Game", "It's your ship!")
    
            else:
                self.buttons[x][y].config(bg='white', state=tk.DISABLED)
                messagebox.showinfo("Battleship Game", "Miss!")
                self.turn = -1
                
                self.enemy_move()

    def enemy_move(self):
        if self.turn == -1:
            x, y = (random.randint(0, self.enemy_board_size - 1), random.randint(0, self.enemy_board_size - 1))
            self.enemy_button_click(x, y)
    
    def enemy_button_click(self, x, y):
        if(x, y) == self.ship_position_player:
            self.buttons[x][y].config(bg='red', state=tk.DISABLED)
            messagebox.showinfo("Battleship Game", "You lost!")
            self.root.destroy()
            
        elif(x, y) == self.ship_position_enemy:
            messagebox.showinfo("Battleship Game", "Enemy missed!")
            self.turn = 1
        
        else:
            self.buttons[x][y].config(bg='white', state=tk.DISABLED)
            messagebox.showinfo("Battleship Game", "Enemy missed!")
            self.turn = 1
            
            
def main():
    root = tk.Tk()
    game = Battleship(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()