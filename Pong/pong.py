import pygame



class Pong():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        
        self.WINDOW_SIZE = (900, 600)   
        self.WIDTH = self.WINDOW_SIZE[0]
        self.HEIGHT = self.WINDOW_SIZE[1]
             
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("Pong")
        
        self.font = pygame.font.SysFont("Courier New", 20)
        self.fps = pygame.time.Clock()
        self.fps_value = 60
    
    def main(self):
        running = True
        player1 = Striker(20, 0, 10, 100, 10, self.GREEN)
        player2 = Striker(self.WIDTH -30, 0, 10, 100, 10, self.GREEN)
        ball = Ball(self.WIDTH // 2, self.HEIGHT // 2, 7, 7, self.WHITE)
        
        list_players = [player1, player2]
        
        player1_score, player2_score = 0, 0
        player1_yDir, player2_yDir = 0, 0
        
        while running:
            self.screen.fill(self.BLACK)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        player1_yDir = -1
                    if event.key == pygame.K_s:
                        player1_yDir = 1
                    if event.key == pygame.K_UP:
                        player2_yDir = -1
                    if event.key == pygame.K_DOWN:
                        player2_yDir = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s:
                        player1_yDir = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        player2_yDir = 0
            for player in list_players:
                if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
                    ball.hit()
            
            player1.update(player1_yDir)
            player2.update(player2_yDir)
            point = ball.update()
            
            if point == -1:
                player1_score += 1
            elif point == 1:
                player2_score += 1
                
            if point:
                ball.reset()
            
            player1.display()
            player2.display()
            ball.display()
            
            player1.display_score(100, 20, "Player 1: ", player1_score,  self.WHITE)
            player2.display_score(self.WIDTH - 100, 20, "Player 2: ", player2_score,  self.WHITE)
            
            pygame.display.update()
            pygame.display.flip()
            self.fps.tick(self.fps_value)

class Striker:
    def __init__(self, x, y, width, height, speed, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
    
        self.screen = Pong().screen
        self.HEIGHT = Pong().WINDOW_SIZE[1]
        self.font = Pong().font
                
        self.objRect = pygame.Rect(x, y, width, height)
        self.obj = pygame.draw.rect(self.screen, self.color, self.objRect)
        
    def display(self):
        self.obj = pygame.draw.rect(self.screen, self.color, self.objRect)
    
    def update(self, yDir):
        self.y = self.y + self.speed * yDir
        
        if self.y <= 0:
            self.y = 0
            
        elif self.y + self.height >= self.HEIGHT:
            self.y = self.HEIGHT - self.height
            
        self.objRect = (self.x, self.y, self.width, self.height)
        
    def display_score(self, x, y, text, score, color):
        text = self.font.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        self.screen.blit(text, textRect)
        
    def getRect(self):
        return self.objRect
    
class Ball:
    def __init__(self, x, y, radius, speed, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xDir = 1
        self.yDir = -1

        self.screen = Pong().screen
        self.HEIGHT = Pong().WINDOW_SIZE[1]
        self.WIDTH = Pong().WINDOW_SIZE[0]
        
        self.ball = pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
        self.score_restraint = 1
        
    def display(self):
        self.ball = pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
    
    def update(self):
        self.x += self.speed * self.xDir
        self.y += self.speed * self.yDir
        
        if self.y <= 0 or self.y >= self.HEIGHT:
            self.yDir *= -1
        
        if self.x <= 0 and self.score_restraint:
            self.score_restraint = 0
            return 1
        elif self.x >= self.WIDTH and self.score_restraint:
            self.score_restraint = 0
            return -1
        else:
            return 0
        
    def reset(self):
        self.x = self.WIDTH // 2
        self.y = self.HEIGHT // 2
        self.xDir *= -1
        self.score_restraint = 1
        
    def hit(self):
        self.xDir *= -1
        
    def getRect(self):
        return self.ball


if __name__ == '__main__':
    Pong().main()