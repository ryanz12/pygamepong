import pygame
import random

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
paddleWidth, paddleHeight = 15, 100
ballSize = 15

score = aiScore = 0
font = pygame.font.SysFont('arial', 50)
text = font.render(f'{score}  :  {aiScore}', False, (211, 211, 211))
text_rect = text.get_rect(center=(WIDTH/2, 100))

wn = pygame.display.set_mode((WIDTH, HEIGHT))

class Ball:
    def __init__(self):
        self.x = (WIDTH-ballSize)/2
        self.y = (HEIGHT-ballSize)/2

        self.speedX = random.choice([-1, 1]) * 5
        self.speedY = random.choice([-1, 1]) * 5
        self.velocity = 1.002

    def draw(self):
        pygame.draw.rect(wn, (211, 211, 211), (self.x, self.y, ballSize, ballSize))
        self.move()

    def move(self):
        self.checkCollision()
        self.x += self.speedX
        self.y += self.speedY
        self.speedX*=self.velocity

    def checkCollision(self):
        if self.y < 0 or self.y+ballSize > HEIGHT:
            self.speedY = -self.speedY
        
        if self.x < 0 or self.x+ballSize > WIDTH:
            global score, aiScore, text

            if self.x < 0:
                aiScore+=1
            else:
                score+=1

            self.x = (WIDTH-ballSize)/2
            self.y = (HEIGHT-ballSize)/2
            self.speedX = random.choice([-1, 1]) * 5

            text = font.render(f'{score}  :  {aiScore}', False, (211, 211, 211))

    def paddleCollision(self, paddle):
        if self.x + ballSize >= paddle.x and self.x <= paddle.x + paddleWidth:
            if self.y + ballSize >= paddle.y and self.y <= paddle.y + paddleHeight:
                self.speedX = -self.speedX


ball = Ball()

class Paddle:
    def __init__(self, x):
        self.x = x
        self.y = (HEIGHT-paddleHeight)/2    
        self.speed = 12

    def draw(self):
        pygame.draw.rect(wn, (211, 211, 211), (self.x, self.y, paddleWidth, paddleHeight))

    def move(self, direction):
        self.checkCollision()

        if direction == 'up':
            self.y -= self.speed
        elif direction == 'down':
            self.y += self.speed

    def checkCollision(self):
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT-paddleHeight:
            self.y = HEIGHT-paddleHeight

    def returnPaddleY(self):
        return self.y

paddle1 = Paddle(5)
paddle2 = Paddle(WIDTH-5-paddleWidth)

def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        wn.fill((0,0,0))
        wn.blit(text, text_rect)
        paddle1.draw()
        paddle2.draw()
        paddle2.y = ball.y
        paddle2.checkCollision()

        ball.draw()
        ball.paddleCollision(paddle1)
        ball.paddleCollision(paddle2)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            paddle1.move('up')
        if keys[pygame.K_s]:
            paddle1.move('down')
        
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()