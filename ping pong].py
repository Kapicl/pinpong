import pygame
import random

WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 15
PADDLE_SPEED = 10
BALL_SPEED_X = 7
BALL_SPEED_Y = 7
MAX_BALL_SPEED = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 60)

bounce_sound = pygame.mixer.Sound("udar.mp3")

left_paddle = pygame.Rect(50, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 70, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

score_left = 0
score_right = 0

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    speed_text = font.render(f"Speed: {abs(ball_speed_x)}", True, WHITE)
    screen.blit(speed_text, (WIDTH//2 - 100, 20))
    score_text = font.render(f"{score_left} : {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - 50, 60))
    pygame.display.flip()

def move_ball():
    global ball_speed_x, ball_speed_y, score_left, score_right

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        bounce_sound.play()

    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1.1
        ball_speed_x = max(min(ball_speed_x, MAX_BALL_SPEED), -MAX_BALL_SPEED)
        bounce_sound.play()

    if ball.left <= 0:
        score_right += 1
        reset_ball()
    elif ball.right >= WIDTH:
        score_left += 1
        reset_ball()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x = BALL_SPEED_X * random.choice((1, -1))
    ball_speed_y = BALL_SPEED_Y * random.choice((1, -1))

def main():
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += PADDLE_SPEED

        move_ball()
        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
