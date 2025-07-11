import time
import pygame
import math

class Game:
    def __init__(self, screen, players, num_of_rounds):
        assert players == 2
        self.board = [[Pixel(3*x, 3*y) for x in range(300)] for y in range(200)]
        self.players_colors = [(255, 0, 0), (0, 255, 0)]
        self.players = [Player(i, self.players_colors.pop()) for i in range(players)]
        self.next_turn = lambda player : player + 1 if player < len(self.players)-1 else 0
        self.ground_function = lambda x: 300 + 30 * math.sin(x * 0.01) + 20 * math.sin(x * 0.05)
        self.num_of_rounds = num_of_rounds
        self.screen = screen
        self.dying_order = []

    def explosion(self, x, y, strength):
        for i in range(strength):
            pygame.draw.circle(self.screen, (200, 130, 0), (x, y), i)
            pygame.draw.circle(self.screen, (255, 130, 0), (x, y), 0.5 * i)
            pygame.display.update()
            time.sleep(0.001)
        for column in self.board:
            for pixel in column:
                if (pixel.x - x) ** 2 + (pixel.y - y) ** 2 < strength ** 2:
                    pixel.ground = False
        for player in self.players:
            tank = player.tank
            if tank:
                if x-strength < tank.x < x+strength and y-strength < tank.y < y+strength:
                    tank.health -= strength
                    tank.max_shot_power -= 0.5*strength
                if tank.health <= 0:
                    player.tank = None
                    self.explosion(tank.x, tank.y, 20)
                    self.dying_order.append(player)
                    return
class Player:
    def __init__(self, id, color):
        self.player_id = id
        self.score = 0
        self.color = color
        self.tank = None
        self.weapons = ([Weapon, 1000, 'MISSLE'], [SevereMissle, 10, 'SEVERE MISSLE'], [SmallAtomBomb, 2, 'SMALL ATOM BOMB'], [AtomBomb, 1, 'ATOM BOMB'])
    def __repr__(self):
        return f'player {self.player_id+1}'

class Pixel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ground = False

class Weapon:
    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.strength = 25
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), (self.x, self.y), 2)

    def move(self, wind):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.2
        self.velocity_x += wind * 0.005
        time.sleep(0.01)


class SevereMissle(Weapon):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__(x, y, velocity_x, velocity_y)
        self.strength = 40

class AtomBomb(Weapon):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__(x, y, velocity_x, velocity_y)
        self.strength = 150

class SmallAtomBomb(Weapon):
    def __init__(self, x, y, velocity_x, velocity_y):
        super().__init__(x, y, velocity_x, velocity_y)
        self.strength = 80

class Tank:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.gun_direction = 90
        self.health = 100
        self.shot_power = 0
        self.max_shot_power = 100
        self.fuel = 100

    def move(self, change):
        if 0 <= self.x <= 900:
            self.x += change

    def move_gun(self, change):
        if 0 < self.gun_direction < 180:
            self.gun_direction += change
        elif self.gun_direction <= 0:
            self.gun_direction = 1
        elif self.gun_direction >= 180:
            self.gun_direction = 179
    def edit_shot_power(self, change):
        if 0 < self.shot_power < self.max_shot_power:
            self.shot_power += change

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y - 7, 13, 10))
        pygame.draw.rect(screen, self.color, (self.x - 6.5, self.y - 2, 26, 10))
        pygame.draw.rect(screen, (0,0,0), (self.x - 6, self.y + 5, 24, 4))
        pygame.draw.line(screen, (0,0,0), (self.x + 5, self.y - 7), (self.x + (20 * math.cos((self.gun_direction / 360) * 2 * math.pi)), self.y - 7 - (20 * math.sin((self.gun_direction / 360) * 2 * math.pi))), 5)

    def shot(self, weapon_type):
        return weapon_type(self.x+(20*math.cos((self.gun_direction/360)*2*math.pi)), self.y-(20*math.sin((self.gun_direction/360)*2*math.pi)),
                      self.shot_power*0.2*math.cos((self.gun_direction/360)*2*math.pi), -self.shot_power*0.2*math.sin((self.gun_direction/360)*2*math.pi))

class Button:
    def __init__(self, screen, pos, size, text, active):
        #main vars
        self.screen = screen
        self.position = pos
        self.size = size
        self.top_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.bottom_rect = pygame.Rect(self.position[0] + 2, self.position[1] + 5, self.size[0], self.size[1])
        self.pressed = False
        self.active = active

        #colors
        self.__top_rect_normal_color = (205,205,0)
        self.__top_rect_hovered_color = (250,250,150)
        self.__bottom_rect_normal_color = (205,102,0)
        self.__bottom_rect_hovered_color = (205,142,40)
        self.__not_active_color = (131,139,139)

        self.__top_rect_color = self.__top_rect_normal_color
        self.__bottom_rect_color = self.__bottom_rect_normal_color

        #text
        self.__text_font = pygame.font.SysFont(str(text) + "font", 30)
        self.__text = self.__text_font.render(text, False, (0, 0, 0))

    def draw(self):
        if self.active:
            pygame.draw.circle(self.screen, self.__bottom_rect_color, self.bottom_rect.bottomleft, 10)
            pygame.draw.circle(self.screen, self.__bottom_rect_color, self.bottom_rect.bottomright, 10)
            pygame.draw.circle(self.screen, self.__bottom_rect_color, self.bottom_rect.topright, 10)
            pygame.draw.rect(self.screen, self.__bottom_rect_color, ((self.bottom_rect.topleft[0] - 10, self.bottom_rect.topleft[1]), (self.bottom_rect.size[0] + 20, self.bottom_rect.size[1])))
            pygame.draw.rect(self.screen, self.__bottom_rect_color, ((self.bottom_rect.topleft[0], self.bottom_rect.topleft[1] - 10), (self.bottom_rect.size[0], self.bottom_rect.size[1] + 20)))
            pygame.draw.circle(self.screen, self.__top_rect_color, self.top_rect.bottomleft, 10)
            pygame.draw.circle(self.screen, self.__top_rect_color, self.top_rect.bottomright, 10)
            pygame.draw.circle(self.screen, self.__top_rect_color, self.top_rect.topleft, 10)
            pygame.draw.circle(self.screen, self.__top_rect_color, self.top_rect.topright, 10)
            pygame.draw.rect(self.screen, self.__top_rect_color, ((self.top_rect.topleft[0] - 10, self.top_rect.topleft[1]), (self.top_rect.size[0] + 20, self.top_rect.size[1])))
            pygame.draw.rect(self.screen, self.__top_rect_color, ((self.top_rect.topleft[0], self.top_rect.topleft[1] - 10), (self.top_rect.size[0], self.top_rect.size[1] + 20)))
            self.screen.blit(self.__text, (self.position[0]+2, self.position[1]+5))

    def clicked(self):
        if self.active:
            pos = pygame.mouse.get_pos()
            if self.top_rect.collidepoint(pos) or self.bottom_rect.collidepoint(pos):
                self.__top_rect_color = self.__top_rect_hovered_color
                self.__bottom_rect_color = self.__bottom_rect_hovered_color
                if pygame.mouse.get_pressed()[0] and self.pressed == False:
                    self.top_rect.center = self.bottom_rect.center
                    self.draw()
                    pygame.display.update()
                    time.sleep(0.05)
                    return True
                self.top_rect.x = self.position[0]
                self.top_rect.y = self.position[1]
            else:
                self.__top_rect_color = self.__top_rect_normal_color
                self.__bottom_rect_color = self.__bottom_rect_normal_color
            return False

    def update_text(self, text):
        self.__text_font = pygame.font.SysFont(str(text) + "font", 30)
        self.__text = self.__text_font.render(text, False, (0, 0, 0))

class Slider:
    def __init__(self, screen, pos, text):
        self.screen = screen
        self.position = pos
        self.size = (150, 25)
        self.top_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.bottom_rect = pygame.Rect(self.position[0] + 2, self.position[1] + 5, self.size[0], self.size[1])
        self.slider_pos = 50
        self.text = text

    def draw(self, max_shot_power):
        self.max_shot_power = max_shot_power
        pygame.draw.circle(self.screen, (205, 102, 0), self.bottom_rect.bottomleft, 10)
        pygame.draw.circle(self.screen, (205, 102, 0), self.bottom_rect.bottomright, 10)
        pygame.draw.circle(self.screen, (205, 102, 0), self.bottom_rect.topright, 10)
        pygame.draw.rect(self.screen, (205, 102, 0), ((self.bottom_rect.topleft[0] - 10, self.bottom_rect.topleft[1]),(self.bottom_rect.size[0] + 20, self.bottom_rect.size[1])))
        pygame.draw.rect(self.screen, (205, 102, 0), ((self.bottom_rect.topleft[0], self.bottom_rect.topleft[1] - 10),(self.bottom_rect.size[0], self.bottom_rect.size[1] + 20)))
        pygame.draw.circle(self.screen, (205,205,0), self.top_rect.bottomleft, 10)
        pygame.draw.circle(self.screen, (205,205,0), self.top_rect.bottomright, 10)
        pygame.draw.circle(self.screen, (205,205,0), self.top_rect.topleft, 10)
        pygame.draw.circle(self.screen, (205,205,0), self.top_rect.topright, 10)
        pygame.draw.rect(self.screen, (205,205,0), ((self.top_rect.topleft[0] - 10, self.top_rect.topleft[1]), (self.top_rect.size[0] + 20, self.top_rect.size[1])))
        pygame.draw.rect(self.screen, (205,205,0), ((self.top_rect.topleft[0], self.top_rect.topleft[1] - 10), (self.top_rect.size[0], self.top_rect.size[1] + 20)))
        self.screen.blit(pygame.font.SysFont('shot power' + "font", 20).render(self.text, False, (0, 0, 0)), (self.position[0]+30, self.position[1]))
        pygame.draw.rect(self.screen, (10,10,10), ((self.position[0]+10, self.position[1]+20), (130, 5)))
        pygame.draw.rect(self.screen, (255, 0, 0), ((self.position[0]+10+(self.max_shot_power*1.3),self.position[1]+20),((100-self.max_shot_power)*1.3,5)))
        pygame.draw.circle(self.screen, (255,100,0), (self.position[0]+10+(self.slider_pos*1.3), self.position[1]+22), 8)

    def clicked(self):
        pos = pygame.mouse.get_pos()
        if self.position[0]+10+(self.slider_pos*1.3)-30 < pos[0] < self.position[0]+30+(self.slider_pos*1.3) + 4 and self.position[1] + 10 < pos[1] < self.position[1] + 34:
            if pygame.mouse.get_pressed()[0]:
                new_slider_pos = ((pos[0]-self.position[0]-10)/130)*100
                if new_slider_pos < 0:
                    self.slider_pos = 0
                elif new_slider_pos > self.max_shot_power:
                    self.slider_pos = self.max_shot_power
                else:
                    self.slider_pos = new_slider_pos
        return self.slider_pos
