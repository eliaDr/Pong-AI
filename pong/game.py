import pygame
import sys
pygame.init()

from .ball import Ball
from .paddle import Paddle
    
class Game():
    def __init__(self):
        # initializing variables
        self.FPS = 60
        self.WINDOW_SIZE = [1100, 700]
        self.SCORE_FONT = pygame.font.SysFont("comicsans", 50)

        self.window = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption('Pong AI')
        self.clock = pygame.time.Clock()

        self.ball = Ball(self.WINDOW_SIZE[0] / 2, self.WINDOW_SIZE[1] / 2)
        self.paddle_left = Paddle(30, (self.WINDOW_SIZE[1] / 2) - 50)
        self.paddle_right = Paddle(self.WINDOW_SIZE[0] - 30 - 20, (self.WINDOW_SIZE[1] / 2) - 50)
        
        self.left_score = 0
        self.right_score = 0
        
    def collision(self):
        if self.ball.y <= 0:
            self.ball.y_speed *= -1
        if self.ball.y >= self.WINDOW_SIZE[1]:
            self.ball.y_speed *= -1
            
        if self.ball.x <= 0:
            self.right_score += 1
            self.ball.reset(self.WINDOW_SIZE[0] / 2, self.WINDOW_SIZE[1] / 2, self.ball.x_speed * -1, self.ball.y_speed * 1)
        if self.ball.x >= self.WINDOW_SIZE[0]:
            self.left_score += 1
            self.ball.reset(self.WINDOW_SIZE[0] / 2, self.WINDOW_SIZE[1] / 2, self.ball.x_speed * -1, self.ball.y_speed * 1)
        
        collide = pygame.Rect.colliderect(self.paddle_left.rect, self.ball.rect)
        if collide:
            self.ball.x_speed *= -1
        
        collide = pygame.Rect.colliderect(self.paddle_right.rect, self.ball.rect)
        if collide:
            self.ball.x_speed *= -1    
    
    def draw_dashed_line(self, start, end):
        origin = start
        target = end
        displacement = target[1] - origin[1]
        length = displacement
        slope = displacement/length

        for index in range(0, int(length / 10), 2):
            start_continue = origin[1] + (slope * index * 12)
            end_continue   = origin[1] + (slope * (index + 1) * 12)
            pygame.draw.line(self.window, (255, 255, 255), (self.WINDOW_SIZE[0] / 2, start_continue), (self.WINDOW_SIZE[0] / 2, end_continue), 2)     
        
    def draw_score(self):
        left_score_text = self.SCORE_FONT.render(f"{self.left_score}", 1, (255, 255, 255))
        right_score_text = self.SCORE_FONT.render(f"{self.right_score}", 1, (255, 255, 255))
        
        self.window.blit(left_score_text, (self.WINDOW_SIZE[0] // 4 - left_score_text.get_width() // 2, 20))
        self.window.blit(right_score_text, (self.WINDOW_SIZE[0] * (3/4) - right_score_text.get_width() // 2, 20))
    
    def draw(self):
        self.draw_score()
        self.draw_dashed_line((self.WINDOW_SIZE[0] / 2, 0), (self.WINDOW_SIZE[0] / 2, self.WINDOW_SIZE[1]))
        self.ball.draw(self.window)
        self.paddle_left.draw(self.window)
        self.paddle_right.draw(self.window)
        pygame.display.update()
        self.window.fill((0, 0, 0))
    
    def move(self):
        self.ball.move()
        self.paddle_left.move(self.WINDOW_SIZE, 'left')
        self.paddle_right.move(self.WINDOW_SIZE, 'right')
    
    def loop(self):
        self.clock.tick(self.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        
        self.collision()          
        self.move()
        self.draw()
        