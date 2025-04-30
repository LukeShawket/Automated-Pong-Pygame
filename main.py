import random
import pygame
import ball
import player
import ui_handle

#variables
is_lunched = True
is_right_hit = False
is_left_hit = False
is_touched = False
turn_ended = False
white_wins = False
black_wins = False
fund_update = False

random_dir = random.choice((-1, 1))
ball_start_speed = 1500

total_fund = 10000
bet = 0
betted_player = ''

# pygame setup
pygame.init()
text = ui_handle.Text(20, 'white')
title = ui_handle.Text(60, 'white')
debug_text = ui_handle.Text(20, 'yellow')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


bet_white = ui_handle.Button(x=50, y=160, wid=100, hei=40)
bet_black = ui_handle.Button(x=50, y=210, wid=100, hei=40)
start_button = ui_handle.Button(x=50, y=260, wid=100, hei=40)
return_button = ui_handle.Button(x=600, y=500, wid=100, hei=40)

small_bet = ui_handle.Button(x=50, y=180, wid=100, hei=40)
mid_bet = ui_handle.Button(x=200, y=180, wid=100, hei=40)
big_bet = ui_handle.Button(x=350, y=180, wid=100, hei=40)
small_bet.visible = False
mid_bet.visible = False
big_bet.visible = False

ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
r_player_pos = pygame.Vector2(screen.get_width()-100, screen.get_height() / 2.5)
l_player_pos = pygame.Vector2(100, screen.get_height() / 2.5)
ball_late_x = ball_pos.x
while running:


    right_player_rect = pygame.Rect(r_player_pos.x, r_player_pos.y , 30, 200)
    left_player_rect = pygame.Rect(l_player_pos.x, l_player_pos.y, 30, 200)
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    if not turn_ended:
        is_start_pressed = start_button.button_state_update(events)
    is_bet_white_pressed = bet_white.button_state_update(events)
    is_bet_black_pressed = bet_black.button_state_update(events)
    is_smal_bet_pressed = small_bet.button_state_update(events)
    is_mid_bet_pressed = mid_bet.button_state_update(events)
    is_big_bet_presed = big_bet.button_state_update(events)


    if is_bet_white_pressed:
        bet_white.visible = False
        bet_black.visible = False
        small_bet.visible = True
        mid_bet.visible = True
        big_bet.visible = True
        small_bet.draw(screen=screen)
        mid_bet.draw(screen=screen)
        big_bet.draw(screen=screen)
        betted_player = 'white'
    if is_bet_black_pressed:
        bet_white.visible = False
        bet_black.visible = False
        small_bet.visible = True
        mid_bet.visible = True
        big_bet.visible = True
        small_bet.draw(screen=screen)
        mid_bet.draw(screen=screen)
        big_bet.draw(screen=screen)
        betted_player = 'black'

    if is_smal_bet_pressed:
        bet = total_fund/3
        small_bet.pressed = False
    if is_mid_bet_pressed:
        bet = total_fund/2
        mid_bet.pressed = False
    if is_big_bet_presed:
        bet = total_fund/1
        big_bet.pressed = False

    if is_start_pressed:

        start_button.visible = False
        bet_white.visible = False
        bet_black.visible = False
        bet_white.pressed = False
        bet_black.pressed = False
        turn_ended = False

        _ball = ball.Ball(screen, ball_pos)
        right_player = player.Player(screen, r_player_pos.x, r_player_pos.y, (0, 0, 0), 200, 500)
        left_player = player.Player(screen, l_player_pos.x, l_player_pos.y, (255, 255, 255), 200, 500)

        # ball move to random direction
        if is_lunched:
            ball_pos.x += random_dir * dt *  ball_start_speed
        if is_right_hit:
            is_lunched = False
            ball_pos.x += -dt * ball_start_speed
            ball_pos.y += random_y
        if is_left_hit:
            is_lunched = False
            ball_pos.x += dt * ball_start_speed
            ball_pos.y += random_y

        # collision detection
        hit =  _ball.collision(ball_pos, right_player_rect, left_player_rect)
        if hit == "right_hit":
            random_y = random.uniform(-5, 5)
            is_left_hit = False
            is_right_hit = True
        if hit == "left_hit":
            random_y = random.uniform(-5, 5)
            is_right_hit = False
            is_left_hit = True
        
        # bounce direction when hit boundary
        if ball_pos.y <= 15:
            random_y *= -1
        if ball_pos.y >= 705:
            random_y *= -1

        # player y update according to ball y in limited area
        if is_left_hit:
            if r_player_pos.y <= 520:
                if right_player.predict() >= 5:
                    if r_player_pos.y < ball_pos.y-100:
                        r_player_pos.y += dt * 300
                else:
                    r_player_pos.y += dt * 300
            if r_player_pos.y >= 0:
                if right_player.predict() >= 5:
                    if r_player_pos.y > ball_pos.y-100:
                        r_player_pos.y -= dt * 300
                else:
                    r_player_pos.y -= dt * 300

        if is_right_hit: 
            if l_player_pos.y <= 520:
                if left_player.predict() >= 5:
                    if l_player_pos.y < ball_pos.y-100:
                        l_player_pos.y += dt * 300
                else:
                    l_player_pos.y += dt * 300
            if l_player_pos.y >= 0:
                if left_player.predict() >= 5:
                    if l_player_pos.y > ball_pos.y-100:
                        l_player_pos.y -= dt * 300
                else:
                    l_player_pos.y -= dt * 300

        ball_late_x = ball_pos.x

        if ball_pos.x < l_player_pos.x-200:
            turn_ended =  True
            is_start_pressed = False
            black_wins = True
        if ball_pos.x > r_player_pos.x+200:
            turn_ended = True
            is_start_pressed = False
            white_wins = True

        # display all variables
        screen.blit(debug_text.get_text(f'is_lunched: {is_lunched}'), (700, 20))
        screen.blit(debug_text.get_text(f'is_right_hit: {is_right_hit}'), (700, 40))
        screen.blit(debug_text.get_text(f'is_left_hit: {is_left_hit}'), (700, 60))
        screen.blit(debug_text.get_text(f'is_touched: {is_touched}'), (700, 80))
        screen.blit(debug_text.get_text(f'turn_ended: {turn_ended}'), (700, 100))
        screen.blit(debug_text.get_text(f'white_wins: {white_wins}'), (700, 120))
        screen.blit(debug_text.get_text(f'black_wins: {black_wins}'), (700, 140))
        screen.blit(debug_text.get_text(f'fund_update: {fund_update}'), (700, 160))
        screen.blit(debug_text.get_text(f'small_bet_visible: {small_bet.visible}'), (700, 180))
        screen.blit(debug_text.get_text(f'mid_bet_visible: {mid_bet.visible}'), (700, 200))
        screen.blit(debug_text.get_text(f'big_bet_visible: {big_bet.visible}'), (700, 220))
        screen.blit(debug_text.get_text(f'small_bet_pressed: {small_bet.pressed}'), (700, 240))
        screen.blit(debug_text.get_text(f'mid_bet_pressed: {mid_bet.pressed}'), (700, 260))
        screen.blit(debug_text.get_text(f'big_bet_pressed: {big_bet.pressed}'), (700, 280))
        screen.blit(debug_text.get_text(f'bet_white_pressed: {bet_white.pressed}'), (700, 300))
        screen.blit(debug_text.get_text(f'bet_black_pressed: {bet_black.pressed}'), (700, 320))
        screen.blit(debug_text.get_text(f'start_pressed: {start_button.pressed}'), (700, 340))
        screen.blit(debug_text.get_text(f'bet_white_visible: {bet_white.visible}'), (700, 360))
        screen.blit(debug_text.get_text(f'bet_black_visible: {bet_black.visible}'), (700, 380))
        screen.blit(debug_text.get_text(f'start_visibile: {start_button.visible}'), (700, 400))
        screen.blit(debug_text.get_text(f'ball.hit: {_ball.hit}'), (700, 420))
        screen.blit(debug_text.get_text(f'ball.position: {ball_pos}'), (700, 440))
        screen.blit(debug_text.get_text(f'white.position: {r_player_pos}'), (700, 460))
        screen.blit(debug_text.get_text(f'black.position: {l_player_pos}'), (700, 480))
        screen.blit(debug_text.get_text(f'bet_amount: {round(bet)}'), (700, 500))
        screen.blit(debug_text.get_text(f'total_fund: {round(total_fund)}'), (700, 520))

    else:
        if not turn_ended:
            start_button.draw(screen=screen)
            bet_white.draw(screen=screen)
            bet_black.draw(screen=screen)
            screen.blit(text.get_text(f'Your fund: {round(total_fund)} dollars'), (50, 100))
            screen.blit(text.get_text('Start'), (start_button.x+30, start_button.y+10))
            if is_bet_white_pressed or is_bet_black_pressed:
                screen.blit(text.get_text('Choose the amount you would like to bet'), (50, 130))
                screen.blit(text.get_text(f'{round(total_fund/3)}'), (small_bet.x+10, small_bet.y+10))
                screen.blit(text.get_text(f'{round(total_fund/2)}'), (mid_bet.x+10, mid_bet.y+10))
                screen.blit(text.get_text(f'{round(total_fund/1)}'), (big_bet.x+10, big_bet.y+10))
            else:
                screen.blit(text.get_text('Choose a team'), (50, 130))
                screen.blit(text.get_text('White'), (bet_white.x+30, bet_white.y+10))
                screen.blit(text.get_text('Black'), (bet_black.x+30, bet_black.y+10))
        else:
            if white_wins:
                screen.blit(title.get_text('White Player Wins!'), (400, 200))
                if betted_player == 'white':
                    if not fund_update:
                        total_fund += bet
                        fund_update = True
                    screen.blit(title.get_text(f'You earned: {round(bet)} dollars'), (400, 300))
                    screen.blit(title.get_text(f'Your total fund: {round(total_fund)} dollars'), (400, 400))
                else:
                    if not fund_update:
                        total_fund -= bet
                        fund_update = True
                    screen.blit(title.get_text(f'You lost: {round(bet)} dollars'), (400, 300))
                    screen.blit(title.get_text(f'Your total fund: {round(total_fund)} dollars'), (400, 400))
            if black_wins:
                screen.blit(title.get_text('Black Player Wins!'), (400, 200))
                if betted_player == 'black':
                    if not fund_update:
                        total_fund += bet
                        fund_update = True
                    screen.blit(title.get_text(f'You earned: {round(bet)} dollars'), (400, 300))
                    screen.blit(title.get_text(f'Your total fund: {round(total_fund)} dollars'), (400, 400))
                else:
                    if not fund_update:
                        total_fund -= bet
                        fund_update = True
                    screen.blit(title.get_text(f'You lost: {round(bet)} dollars'), (400, 300))
                    screen.blit(title.get_text(f'Your total fund: {round(total_fund)} dollars'), (400, 400))
            return_button.draw(screen=screen)
            screen.blit(text.get_text('Return'), (return_button.x+30, return_button.y+10))
            is_return_pressed = return_button.button_state_update(events)
            if is_return_pressed:
                is_lunched = True
                turn_ended = False
                white_wins = False
                black_wins = False
                fund_update = False
                small_bet.visible = False
                mid_bet.visible = False
                big_bet.visible = False
                small_bet.pressed = False
                mid_bet.pressed = False
                big_bet.pressed = False
                bet_white.pressed = False
                bet_black.pressed = False
                start_button.pressed = False
                start_button.visible = True
                bet_white.visible = True
                bet_black.visible = True
                is_right_hit = False
                is_left_hit = False
                _ball.hit = ''
                ball_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
                r_player_pos = pygame.Vector2(screen.get_width()-100, screen.get_height() / 2.5)
                l_player_pos = pygame.Vector2(100, screen.get_height() / 2.5)
                return_button.pressed = False

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()