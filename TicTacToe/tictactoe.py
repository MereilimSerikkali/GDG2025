import pygame

class TicTacToe():
    
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.WINDOW_SIZE = (450, 500)
        self.CELL_SIZE = 150

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Tic Tac Toe")
            
        self.table_size = self.WINDOW_SIZE[0]
        self.cell_size = self.WINDOW_SIZE[0] // 3
        self.table_space = 20
        self.table = [["-" for _ in range(3)] for _ in range(3)]
                
        self.player = "X"
        self.winner = None
        self.taking_move = True
        self.running = True
        
        self.background_color = (255, 175, 65)
        self.table_color = (50, 50, 50)
        self.line_color = (190, 0, 10)
        self.instructions_color = (15, 55, 165)
        self.game_over_bg_color = (45, 100, 165)
        self.game_over_color = (255, 180, 1)
        
        self.font = pygame.font.SysFont("Courier New", 35)
        self.fps = pygame.time.Clock()
        
    def _draw_table(self):
        tb_space_point = (self.table_space, self.table_size - self.table_space)
        cell_space_point = (self.cell_size, self.cell_size * 2)
        pygame.draw.line(self.screen, self.table_color, [tb_space_point[0], cell_space_point[0]], [tb_space_point[1], cell_space_point[0]], 8)
        pygame.draw.line(self.screen, self.table_color, [cell_space_point[0], tb_space_point[0]], [cell_space_point[0], tb_space_point[1]], 8)
        pygame.draw.line(self.screen, self.table_color, [tb_space_point[0], cell_space_point[1]], [tb_space_point[1], cell_space_point[1]], 8)
        pygame.draw.line(self.screen, self.table_color, [cell_space_point[1], tb_space_point[0]], [cell_space_point[1], tb_space_point[1]], 8)

    def _change_player(self):
        self.player = "O" if self.player == "X" else "X"
    
    def _draw_char(self, x, y, player):
        if player == "O":
            img = pygame.image.load("images/image_o.png")
        elif player == "X":
            img = pygame.image.load("images/image_x.png")

        img = pygame.transform.scale(img, (self.cell_size, self.cell_size))    
        self.screen.blit(img, (x * self.cell_size, y * self.cell_size))

    def _pattern_strike(self, start_point, end_point, line_type):
        mid_val = self.cell_size // 2

        if line_type == "ver":
            start_x, start_y = start_point[0] * self.cell_size + mid_val, self.table_space
            end_x, end_y = end_point[0] * self.cell_size + mid_val, self.table_size - self.table_space
        elif line_type == "hor":
            start_x, start_y = self.table_space, start_point[-1] * self.cell_size + mid_val
            end_x, end_y = self.table_size - self.table_space, end_point[-1] * self.cell_size + mid_val
        elif line_type == "left-diag":
            start_x, start_y = self.table_space, self.table_space
            end_x, end_y = self.table_size - self.table_space, self.table_size - self.table_space
        elif line_type == "right-diag":
            start_x, start_y = self.table_size - self.table_space, self.table_space
            end_x, end_y = self.table_space, self.table_size - self.table_space

        pygame.draw.line(self.screen, self.line_color, [start_x, start_y], [end_x, end_y], 8)

    def _message(self):
        if self.winner is not None:
            self.screen.fill(self.game_over_bg_color, (130, 455, 195, 35))
            msg = self.font.render(f'{self.winner} Wins!', True, self.game_over_color)
            self.screen.blit(msg, (145, 445))
        elif not self.taking_move:
            self.screen.fill(self.game_over_bg_color, (130, 445, 195, 35))
            msg = self.font.render('Draw', True, self.background_color)
            self.screen.blit(msg, (165, 445))
        else: 
            self.screen.fill(self.background_color, (135, 445, 190, 35))
            instructions = self.font.render(f'{self.player} moves', True, self.instructions_color)
            self.screen.blit(instructions,(135,445))
    
    def _game_check(self):
        # vertical check
        for x_index, col in enumerate(self.table):
            if all(cell == self.player for cell in col):
                self._pattern_strike((x_index, 0), (x_index, 2), "ver")
                self.winner = self.player
                self.taking_move = False
                self._message()
                return
            
        # horizontal check
        for row in range(3):
            if all(self.table[col][row] == self.player for col in range(3)):
                self._pattern_strike((0, row), (2, row), "hor")
                self.winner = self.player
                self.taking_move = False
                self._message()
                return
            
        # left diagonal check
        if all(self.table[i][i] == self.player for i in range(3)):
            self._pattern_strike((0, 0), (2, 2), "left-diag")
            self.winner = self.player
            self.taking_move = False
            self._message()
            return

        # right diagonal check
        if all(self.table[i][2 - i] == self.player for i in range(3)):
            self._pattern_strike((2, 0), (0, 2), "right-diag")
            self.winner = self.player
            self.taking_move = False
            self._message()
            return

        # blank table cells check
        if all(cell != "-" for row in self.table for cell in row):
            self.taking_move = False
            self._message()

    def _move(self, pos):
        try:
            x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
            if self.table[x][y] == "-":
                self.table[x][y] = self.player
                self._draw_char(x, y, self.player)
                self._game_check()
                self._change_player()
        except IndexError:
            print("Click inside the table only")

    def main(self):
        self.screen.fill(self.background_color)
        self._draw_table()
        
        while self.running:
            self._message()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.taking_move:
                    self._move(event.pos)
                
            pygame.display.flip()
            self.fps.tick(60)

# Run the game
if __name__ == "__main__":
    TicTacToe().main()
