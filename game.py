import sys
import pygame
from Player import *
from floor import *
from enemy import *
from random import randint
import RPi.GPIO as GPIO
import time

class Game:

    @property
    def width(self):
        return self.screen.get_size()[0]

    @property
    def height(self):
        return self.screen.get_size()[1]

#    @property
#    def gravity(self):
#        return -500

    def __init__(self, screen_width: int = 800, screen_height: int = 600,
                 background_color: pygame.Color = pygame.Color(135, 206, 235, 255),
                 player: Player = Player(30, 30)):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.background_color = background_color
        self.player = player
        self.floor = Floor()
        self.obstacles = [Enemy(50, 50, 800, 350)]
        self.obstacle_speed = 50
        self.lost = False
        self.message = None
        self.message_rect = None
        self.respawn_time = 2.0
        self.current_respawn_timer = 0.0
        self.velocity_range = [150, 180]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN)
        self.gravity = 0
        self.level = 1
        self.time_per_level = 5
        self.game_time = 0
        pygame.init()
        self.timer_font = pygame.font.Font('freesansbold.ttf', 20)

    def start(self):
        
        while True:
            for event in pygame.event.get():
                self.handle_event(event)

            delta_time = pygame.time.Clock().tick(60) / 1000.0
            self.game_time += delta_time
            if self.game_time // self.time_per_level >= self.level:
                self.next_level()

            if GPIO.input(4):
                self.gravity = 2000
            else:
                self.gravity = -2000
            self.lost = self.test_collision()
            self.draw()

            if not self.lost:
                
                self.update_positions(delta_time)
                self.generates_enemy(delta_time)
            else:
                self.display_lost_message()



            pygame.display.update()

    def display_lost_message(self):
        if self.message is None or self.message_rect is None:
            font = pygame.font.Font('freesansbold.ttf', 32)
            self.message = font.render("YOU LOST!", True, pygame.Color('green'), pygame.Color('red'))
            self.message_rect = self.message.get_rect()
            self.message_rect.center = (self.width // 2, self.height // 2)

        self.screen.blit(self.message, self.message_rect)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                self.player.jump(self.height - self.player.position_y - self.player.height <= self.floor.floor_level)

    def draw(self):
        self.draw_background()
        pygame.draw.rect(self.screen, pygame.Color(145, 198, 56, 255), pygame.Rect(60, 50, 50, 50))
        self.draw_obstacles()
        self.player.draw(self.screen)
        self.draw_timer()

    def draw_background(self):
        self.screen.fill(self.background_color)
        self.floor.draw(self.screen)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

    def draw_timer(self):
        message = self.timer_font.render("Time: {:.2f} - Level: ".format(self.game_time) + str(self.level), True, pygame.Color('green'), pygame.Color('red'))
        message_rect = message.get_rect()
        message_rect.center = (self.width // 2, 20)
        self.screen.blit(message, message_rect)

    def update_positions(self, delta_time):
        self.update_player_position(delta_time)
        self.update_obstacles(delta_time)

    def update_player_position(self, delta_time):
        self.player.y_velocity = self.gravity * delta_time + self.player.y_velocity
        self.player.position_y -= self.player.y_velocity * delta_time

        if self.height - self.player.position_y - self.player.height <= self.floor.floor_level:
            self.player.position_y = self.height - self.floor.floor_level - self.player.height
            self.player.y_velocity = 0

    def update_obstacles(self, delta_time):
        for obstacle in self.obstacles:
            obstacle.update_position(delta_time)

    def test_collision(self):
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.rect):
                return True
        if self.player.position_y < 0:
            return True
        return False

    def generates_enemy(self, delta_time):
        self.current_respawn_timer += delta_time
        if self.current_respawn_timer >= self.respawn_time:
            height = 50
            width = 50
            position_x = self.width + width
            position_y = randint(0, self.height-self.floor.floor_level-height)
            velocity = randint(self.velocity_range[0], self.velocity_range[1])
            print(velocity)
            self.obstacles.append(Enemy(width, height, position_x, position_y, velocity))
            self.current_respawn_timer = 0

    def next_level(self):
        self.level += 1
        self.respawn_time -= 0.15
        self.velocity_range[0] += 50
        self.velocity_range[1] += 50
        print(self.velocity_range)


game = Game()
game.start()
