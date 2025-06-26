import random
import time
import pygame
from Tanks_2025 import models
import sys
import asyncio
import math

def draw_trajectory(screen, tank, angle_deg, power, wind, color=(255, 0, 0)):
    x0, y0 = tank.x, tank.y
    angle = math.radians(angle_deg)
    v = power
    vx = v * math.cos(angle)
    vy = -v * math.sin(angle)

    points = []
    g = 1.5

    for t in range(0, 120):
        time_sec = t * 0.1
        xt = x0 + vx * time_sec + wind * time_sec
        yt = y0 + vy * time_sec + 0.5 * g * (time_sec) ** 2

        if yt > 600 or xt < 0 or xt > 895:
            break
        points.append((int(xt), int(yt)))

    for point in points:
        pygame.draw.circle(screen, color, point, 2)



async def main():
    pygame.init()
    screen = pygame.display.set_mode((895, 600))

    BLUE = (20, 60, 160)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 140, 0)
    GREEN = (0, 255, 0)
    weapon = None
    num_of_players = 2
    num_of_rounds = 1
    buttons = {'new game button' : models.Button(screen, (390, 150), (120, 30), 'NEW GAME', True),
               'text num of players' : models.Button(screen, (380, 120), (140, 20), '     players', False),
               'decrease players button' : models.Button(screen, (370, 170), (20, 20), '-', False),
               'increase players button' : models.Button(screen, (510, 170), (20, 20), '+', False),
               'num of players' : models.Button(screen, (440, 170), (20, 20), '{}'.format(num_of_players), False),
               'text num of rounds': models.Button(screen, (380, 240), (140, 20), '     rounds', False),
               'decrease num of rounds': models.Button(screen, (370, 290), (20, 20), '-', False),
               'increase num of rounds': models.Button(screen, (510, 290), (20, 20), '+', False),
               'num of rounds': models.Button(screen, (440, 290), (20, 20), '{}'.format(num_of_rounds), False),
               'create game button': models.Button(screen, (370, 360), (160, 30), 'CREATE GAME', False),
               }

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        background = pygame.image.load("static/mountains.jpg").convert()
        screen.blit(background, (0, 0))
        title_text_down = pygame.font.Font('freesansbold.ttf', 50).render("TANKS", False, YELLOW)
        title_text_rect_down = title_text_down.get_rect()
        title_text_rect_down.center = (450, 50)
        screen.blit(title_text_down, title_text_rect_down)
        title_text_up = pygame.font.Font('freesansbold.ttf', 50).render("TANKS", False, ORANGE)
        title_text_rect_up = title_text_up.get_rect()
        title_text_rect_up.center = (447, 47)
        screen.blit(title_text_up, title_text_rect_up)


        tank1 = models.Tank(100, 500, RED)
        tank1.gun_direction = 40
        tank2 = models.Tank(800, 500, GREEN)
        tank2.gun_direction = 130
        tank1.draw(screen)
        tank2.draw(screen)
        if not weapon:
            shoting_tank = random.choice([tank1, tank2])
            shoting_tank.shot_power = 50
            weapon = shoting_tank.shot(models.Weapon)
        weapon.draw(screen)
        weapon.x += weapon.velocity_x
        weapon.y += weapon.velocity_y
        weapon.velocity_y += 0.2
        time.sleep(0.01)
        if weapon.y > 500:
            for i in range(30):
                pygame.draw.circle(screen, (200, 130, 0), (weapon.x, weapon.y), i)
                pygame.draw.circle(screen, (255, 130, 0), (weapon.x, weapon.y), 0.5 * i)
                time.sleep(0.001)
            weapon = None

        for button_key in buttons.keys():
            buttons[button_key].draw()
        game = None
        if buttons['new game button'].clicked():
            for button_key in buttons.keys():
                buttons[button_key].active = True
            buttons['new game button'].active = False
        if buttons['increase players button'].clicked():
            pass
            buttons['num of players'].update_text(str(num_of_players))
        if buttons['decrease players button'].clicked():
            pass
            buttons['num of players'].update_text(str(num_of_players))
        if buttons['increase num of rounds'].clicked():
            if num_of_rounds < 10:
                num_of_rounds += 1
            buttons['num of rounds'].update_text(str(num_of_rounds))
        if buttons['decrease num of rounds'].clicked():
            if 1 < num_of_rounds:
                num_of_rounds -= 1
            buttons['num of rounds'].update_text(str(num_of_rounds))
        if buttons['create game button'].clicked():
            game = models.Game(screen, num_of_players, num_of_rounds)

        charging_power = False
        if game:
            exit_game_loop = False
            for round in range(game.num_of_rounds):
                if exit_game_loop:
                    break

                for c, player in enumerate(game.players):
                    if c%2==0:
                        tank_spawn_point = random.randint(450,800)
                    else:
                        tank_spawn_point = random.randint(100, 450)
                    player.tank = models.Tank(tank_spawn_point, game.ground_function(tank_spawn_point), player.color)
                wind = random.randint(-10, 10)
                current_weapon = 0
                weapon = None
                for column in game.board:
                    for pixel in column:
                        if game.ground_function(pixel.x) < pixel.y:
                            pixel.ground = True
                '''power_down_button = models.Button(screen, (20, 100), (30, 25), '-', True)
                power_up_button = models.Button(screen, (60, 100), (30, 25), '+', True)
                gun_down_button = models.Button(screen, (200, 100), (30, 25), '-', True)
                gun_up_button = models.Button(screen, (240, 100), (30, 25), '+', True)
                shot_button = models.Button(screen, (380, 100), (60, 25), 'SHOT', True)'''
                exit_button = models.Button(screen, (30, 30), (60, 25), 'EXIT', True)
                change_weapon_right = models.Button(screen, (400, 45), (15, 15), '->', True)
                change_weapon_left = models.Button(screen, (130, 45), (15, 15), '<-', True)

                screen.blit(background, (0, 0))
                run_round = True
                round_num_text_down = pygame.font.Font('freesansbold.ttf', 50).render(f"ROUND {round+1}", False, YELLOW)
                round_num_text_rect_down = round_num_text_down.get_rect()
                round_num_text_rect_down.center = (450, 50)
                screen.blit(round_num_text_down, round_num_text_rect_down)
                round_num_text_up = pygame.font.Font('freesansbold.ttf', 50).render(f"ROUND {round+1}", False, ORANGE)
                round_num_text_rect_up = round_num_text_up.get_rect()
                round_num_text_rect_up.center = (447, 47)
                screen.blit(round_num_text_up, round_num_text_rect_up)
                ranking = sorted(game.players, key=lambda player: player.score, reverse=True)
                for c, player in enumerate(ranking):
                    player_text = pygame.font.Font('freesansbold.ttf', 30).render(f'{player}    score: {player.score}', False, player.color)
                    player_text_rect = player_text.get_rect()
                    player_text_rect.center = (450, 100 + c*40)
                    screen.blit(player_text, player_text_rect)
                if charging_power:
                    tank = game.players[player_turn].tank
                    if tank.shot_power < tank.max_shot_power:
                        tank.shot_power += 0.5
                pygame.display.update()
                await asyncio.sleep(0)
                time.sleep(3)
                player_turn = 0
                game.dying_order.clear()

                while run_round:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and weapon is None and \
                                game.players[player_turn].weapons[current_weapon][1] > 0:
                             charging_power = True

                    if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and weapon is None and charging_power:
                        charging_power = False
                        weapon = game.players[player_turn].tank.shot(
                            game.players[player_turn].weapons[current_weapon][0])
                        game.players[player_turn].weapons[current_weapon][1] -= 1
                        game.players[player_turn].tank.shot_power = 0

                    screen.blit(background, (0, 0))
                    for column in game.board:
                        for pixel in column:
                            if pixel.ground:
                                pygame.draw.rect(screen, (139, 69, 19), (pixel.x, pixel.y, 3, 3))

                    options_position = (20, 20)
                    options_top_rect = pygame.Rect(options_position[0], options_position[1], 418, 50)
                    options_bottom_rect = pygame.Rect(options_position[0] + 2, options_position[1] + 5, 418, 50)
                    pygame.draw.circle(screen, (205, 102, 0), options_bottom_rect.bottomleft, 10)
                    pygame.draw.circle(screen, (205, 102, 0), options_bottom_rect.bottomright, 10)
                    pygame.draw.circle(screen, (205, 102, 0), options_bottom_rect.topright, 10)
                    pygame.draw.rect(screen, (205, 102, 0), (
                    (options_bottom_rect.topleft[0] - 10, options_bottom_rect.topleft[1]),
                    (options_bottom_rect.size[0] + 20, options_bottom_rect.size[1])))
                    pygame.draw.rect(screen, (205, 102, 0), (
                    (options_bottom_rect.topleft[0], options_bottom_rect.topleft[1] - 10),
                    (options_bottom_rect.size[0], options_bottom_rect.size[1] + 20)))
                    pygame.draw.circle(screen, (180, 150, 0), options_top_rect.bottomleft, 10)
                    pygame.draw.circle(screen, (180, 150, 0), options_top_rect.bottomright, 10)
                    pygame.draw.circle(screen, (180, 150, 0), options_top_rect.topleft, 10)
                    pygame.draw.circle(screen, (180, 150, 0), options_top_rect.topright, 10)
                    pygame.draw.rect(screen, (180, 150, 0), ((options_top_rect.topleft[0] - 10, options_top_rect.topleft[1]),(options_top_rect.size[0] + 20, options_top_rect.size[1])))
                    pygame.draw.rect(screen, (180, 150, 0), ((options_top_rect.topleft[0], options_top_rect.topleft[1] - 10),(options_top_rect.size[0], options_top_rect.size[1] + 20)))
                    '''move_left_text = pygame.font.Font('freesansbold.ttf', 10).render(
                        f"MOVE LEFT - LARROW", False, (0, 0, 0))
                    move_left_text_rect = move_left_text.get_rect()
                    move_left_text_rect.topleft = (20, 155)
                    screen.blit(move_left_text, move_left_text_rect)
                    move_right_text = pygame.font.Font('freesansbold.ttf', 10).render(
                        f"MOVE RIGHT - RARROW", False, (0, 0, 0))
                    move_right_text_rect = move_right_text.get_rect()
                    move_right_text_rect.topleft = (160, 155)
                    screen.blit(move_right_text, move_right_text_rect)'''
                    exit_button.draw()
                    'shot_button.draw()'
                    try:
                        '''power_down_button.draw()
                        power_up_button.draw()
                        gun_down_button.draw()
                        gun_up_button.draw()'''
                        try:
                            tank = game.players[player_turn].tank
                            if tank:
                                bar_x = 20
                                bar_y = 90
                                bar_width = 150
                                bar_height = 15

                                filled_width = int((tank.shot_power / tank.max_shot_power) * bar_width)

                                pygame.draw.rect(screen, (50, 50, 50),
                                                 (bar_x, bar_y, bar_width, bar_height))
                                pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, filled_width, bar_height))

                                pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2)

                                font = pygame.font.SysFont('freesansbold.ttf', 15)
                                label = font.render(f'Power: {int(tank.shot_power)}', True, (0, 0, 0))
                                screen.blit(label, (bar_x + bar_width + 10, bar_y - 2))
                        except AttributeError:
                            pass
                        fuel_left_text = pygame.font.Font('freesansbold.ttf', 15).render(f"FUEL {int(game.players[player_turn].tank.fuel)}            WEAPON", False, (0, 0, 0))
                        fuel_left_text_rect = round_num_text_down.get_rect()
                        fuel_left_text_rect.center = (230, 40)
                        screen.blit(fuel_left_text, fuel_left_text_rect)
                        current_weapon_text = pygame.font.Font('freesansbold.ttf', 15).render(f"{game.players[player_turn].weapons[current_weapon][2]}    {game.players[player_turn].weapons[current_weapon][1]} left", False,(100, 0, 0))
                        current_weapon_text_rect = current_weapon_text.get_rect()
                        current_weapon_text_rect.center = (270, 50)
                        screen.blit(current_weapon_text, current_weapon_text_rect)
                        font = pygame.font.SysFont('freesansbold.ttf', 15)
                        '''screen.blit(font.render("POWER", True, (0, 0, 0)), (20, 80))
                        screen.blit(font.render("GUN", True, (0, 0, 0)), (200, 80))'''
                    except AttributeError:
                        pass
                    pygame.draw.polygon(screen, (30,30,130), ((100, 120), (100, 126), (100+wind*3,126), (100+wind*4,123), (100+wind*3,120)))
                    wind_text = pygame.font.Font('freesansbold.ttf', 10).render(f"WIND", False, (30, 30, 130))
                    wind_text_rect = wind_text.get_rect()
                    wind_text_rect.topleft = (20, 115)
                    screen.blit(wind_text, wind_text_rect)
                    change_weapon_left.draw()
                    change_weapon_right.draw()

                    stats_position = (470, 20)
                    stats_top_rect = pygame.Rect(stats_position[0], stats_position[1], 390, len(game.players)*30)
                    stats_bottom_rect = pygame.Rect(stats_position[0] + 2, stats_position[1] + 5, 390, len(game.players*30))
                    pygame.draw.circle(screen, (205, 102, 0), stats_bottom_rect.bottomleft, 10)
                    pygame.draw.circle(screen, (205, 102, 0), stats_bottom_rect.bottomright, 10)
                    pygame.draw.circle(screen, (205, 102, 0), stats_bottom_rect.topright, 10)
                    pygame.draw.rect(screen, (205, 102, 0), ((stats_bottom_rect.topleft[0] - 10, stats_bottom_rect.topleft[1]),(stats_bottom_rect.size[0] + 20, stats_bottom_rect.size[1])))
                    pygame.draw.rect(screen, (205, 102, 0), ((stats_bottom_rect.topleft[0], stats_bottom_rect.topleft[1] - 10), (stats_bottom_rect.size[0], stats_bottom_rect.size[1] + 20)))
                    pygame.draw.circle(screen, (205, 205, 0), stats_top_rect.bottomleft, 10)
                    pygame.draw.circle(screen, (205, 205, 0), stats_top_rect.bottomright, 10)
                    pygame.draw.circle(screen, (205, 205, 0), stats_top_rect.topleft, 10)
                    pygame.draw.circle(screen, (205, 205, 0), stats_top_rect.topright, 10)
                    pygame.draw.rect(screen, (205, 205, 0), ((stats_top_rect.topleft[0] - 10, stats_top_rect.topleft[1]),(stats_top_rect.size[0] + 20, stats_top_rect.size[1])))
                    pygame.draw.rect(screen, (205, 205, 0), ((stats_top_rect.topleft[0], stats_top_rect.topleft[1] - 10),(stats_top_rect.size[0], stats_top_rect.size[1] + 20)))
                    pygame.draw.polygon(screen, (255, 140, 0), ((465, 22+30*player_turn), (465, 42+30*player_turn), (485, 32+30*player_turn)))
                    stats = []
                    for player in game.players:
                        if player.tank:
                            tank_health = player.tank.health
                        else:
                            tank_health = 0
                        stats.append(pygame.font.Font('freesansbold.ttf', 20).render(
                            f'{player}     score {player.score}     hp {tank_health}', True, player.color))
                    for c, player_data in enumerate(stats):
                        text_rect = player_data.get_rect()
                        text_rect.x += 500
                        text_rect.y += 25 + 30*c
                        screen.blit(player_data, text_rect)

                    for player in game.players:
                        tank = player.tank
                        if tank:
                            tank.draw(screen)
                            try:
                                if game.board[int(tank.y / 3) + 1][int(tank.x / 3)].ground == False:
                                    tank.y += 1
                                if game.board[int(tank.y / 3) - 1][int(tank.x / 3)].ground == True:
                                    tank.y -= 1
                                if game.board[int(tank.y / 3) - 5][int(tank.x / 3 + 3)].ground == True:
                                    tank.x -= 1
                                if game.board[int(tank.y / 3) - 5][int(tank.x / 3 - 3)].ground == True:
                                    tank.x += 1
                            except IndexError:
                                player.tank = None
                                game.explosion(tank.x, tank.y, 30)
                                game.dying_order.append(player)

                    if game.players[player_turn].tank == None:
                        player_turn = game.next_turn(player_turn)

                    if weapon != None:
                        if 0 < weapon.x < 900 and 0 < weapon.y < 600:
                            if game.board[int(weapon.y/3)][int(weapon.x/3)].ground == True:
                                game.explosion(weapon.x, weapon.y, weapon.strength)
                                weapon = None
                                wind = random.randint(-10, 10)
                                player_turn = game.next_turn(player_turn)
                            else:
                                weapon.draw(screen)
                                weapon.move(wind)
                        else:
                            weapon = None
                            wind = random.randint(-10, 10)
                            player_turn = game.next_turn(player_turn)

                    try:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_LEFT] and game.players[player_turn].tank.fuel > 0:
                            game.players[player_turn].tank.move(-1)
                            game.players[player_turn].tank.fuel -= 0.1
                            time.sleep(0.02)
                        if keys[pygame.K_RIGHT] and game.players[player_turn].tank.fuel > 0:
                            game.players[player_turn].tank.move(1)
                            game.players[player_turn].tank.fuel -= 0.1
                            time.sleep(0.02)
                        if keys[pygame.K_UP]:
                            game.players[player_turn].tank.move_gun(1)
                        if keys[pygame.K_DOWN]:
                            game.players[player_turn].tank.move_gun(-1)


                        '''if shot_button.clicked() and weapon == None and game.players[player_turn].weapons[current_weapon][1] > 0:
                            weapon = game.players[player_turn].tank.shot(game.players[player_turn].weapons[current_weapon][0])
                            game.players[player_turn].weapons[current_weapon][1] -= 1'''
                        if exit_button.clicked():
                            exit_game_loop = True
                            break
                        if change_weapon_left.clicked():
                            if current_weapon == 0:
                                current_weapon = 3
                            else:
                                current_weapon -= 1
                            time.sleep(0.05)
                        if change_weapon_right.clicked():
                            if current_weapon == 3:
                                current_weapon = 0
                            else:
                                current_weapon += 1
                            time.sleep(0.05)
                        '''if power_up_button.clicked():
                            game.players[player_turn].tank.edit_shot_power(1)
                        if power_down_button.clicked():
                            game.players[player_turn].tank.edit_shot_power(-1)
                        if gun_up_button.clicked():
                            game.players[player_turn].tank.move_gun(1)
                        if gun_down_button.clicked():
                            game.players[player_turn].tank.move_gun(-1)'''
                    except AttributeError:
                        pass
                    if charging_power:
                        tank = game.players[player_turn].tank
                        if tank.shot_power < tank.max_shot_power:
                            tank.shot_power += 0.1
                    if charging_power:
                        tank = game.players[player_turn].tank
                        draw_trajectory(screen, tank, tank.gun_direction, tank.shot_power, wind)
                    pygame.display.update()
                    await asyncio.sleep(0)

                    players_alive = sum((1 if player.tank != None else 0 for player in game.players))
                    if players_alive == 1:
                        for c, player in enumerate(game.dying_order):
                            player.score += 500*c
                        [player for player in game.players if player not in game.dying_order][0].score += 800 * len(game.players)
                        break

                    await asyncio.sleep(0)
                await asyncio.sleep(0)

            ranking = sorted(game.players, key=lambda player : player.score, reverse=True)
            screen.blit(background, (0, 0))
            winner_text_down = pygame.font.Font('freesansbold.ttf', 30).render("WINNER", False, YELLOW)
            winner_text_rect_down = winner_text_down.get_rect()
            winner_text_rect_down.center = (450, 100)
            screen.blit(winner_text_down, winner_text_rect_down)
            winner_text_down = pygame.font.Font('freesansbold.ttf', 30).render("WINNER", False, ORANGE)
            winner_text_rect_down = winner_text_down.get_rect()
            winner_text_rect_down.center = (447, 97)
            screen.blit(winner_text_down, winner_text_rect_down)
            winner_text = pygame.font.Font('freesansbold.ttf', 30).render(f"{ranking[0]}", False, ranking[0].color)
            winner_text_rect = winner_text.get_rect()
            winner_text_rect.center = (450, 140)
            screen.blit(winner_text, winner_text_rect)
            second_text = pygame.font.Font('freesansbold.ttf', 15).render(f"2nd {ranking[1]}", False, ranking[1].color)
            second_text_rect = second_text.get_rect()
            second_text_rect.center = (450, 250)
            screen.blit(second_text, second_text_rect)
            if len(game.players) > 2:
                third_text = pygame.font.Font('freesansbold.ttf', 15).render(f"3rd {ranking[2]}", False, ranking[2].color)
                third_text_rect = third_text.get_rect()
                third_text_rect.center = (450, 280)
                screen.blit(third_text, third_text_rect)
            if charging_power:
                tank = game.players[player_turn].tank
                if tank.shot_power < tank.max_shot_power:
                    tank.shot_power += 0.1
            pygame.display.update()
            await asyncio.sleep(0)
            time.sleep(5)

            for button_k in buttons:
                buttons[button_k].active = False
            buttons['new game button'].active = True
        if charging_power:
            tank = game.players[player_turn].tank
            if tank.shot_power < tank.max_shot_power:
                tank.shot_power += 0.1
        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())