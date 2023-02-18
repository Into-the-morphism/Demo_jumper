import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(70, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Audio/audio_jump.mp3')
        self.jump_sound.set_volume(0.1)
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    def animate_player(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump

        else:
            self.player_index += 0.1
            self.image = self.player_walk[int(self.player_index) % 2]
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate_player()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'Snail':
            snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300
        else:
            fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 200


        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100),y_pos))
    def animation_obstacle(self):
        self.animation_index += 0.1
        self.image = self.frames[int(self.animation_index) % 2]
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
    def update(self):
        self.animation_obstacle()
        self.destroy()
        self.rect.x -= 6


def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = text_font.render(f' score : {current_time}', False, 'Black')
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf,score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

'''def play_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        player_surf = player_walk[int(player_index) % 2]'''
pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('DEMO')
Clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)
game_active = False
start_time = 0
bg_music = pygame.mixer.Sound('Audio/music.wav')
bg_music.set_volume(0.08)
bg_music.play(loops= -1)
#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

ground_surf = pygame.image.load('graphics/ground.png').convert()
sky_surf = pygame.image.load('graphics/sky.png').convert()


#score_surf = text_font.render("DEMO GAME", False, 'Black')
#score_rect = score_surf.get_rect(center=(400, 50))

#Snail
#snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
#snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
#snail_frames = [snail_frame_1, snail_frame_2]
#snail_index = 0
#snail_surf = snail_frames[snail_index]

#Fly
#fly_frame_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
#fly_frame_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
#fly_frames = [fly_frame_1, fly_frame_2]
#fly_index = 0
#fly_surf = fly_frames[fly_index]


#obstacle_rect_list = []

#player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
#player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
#player_walk = [player_walk_1, player_walk_2]
#player_index = 0
#player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

#player_surf = player_walk[player_index]
#player_rect = player_surf.get_rect(midbottom=(80, 300))
#player_gravity = 0
score = 0
highest_score = 0

#Intro Screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center= (400, 200))

Game_name =text_font.render('Demo Jumper', False, (11, 120, 169))
Game_rect = Game_name.get_rect(center=(400, 40))

Game_messege = text_font.render('Press space to start game ...', False, (11, 120, 169))
Game_messege_rect = Game_messege.get_rect(center = (400, 340))
#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

#snail_animation_timer = pygame.USEREVENT + 2
#pygame.time.set_timer(snail_animation_timer, 1600)

#fly_animation_timer = pygame.USEREVENT + 3
#pygame.time.set_timer(fly_animation_timer, 40)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['Snail', 'Fly', 'Snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)


                #if randint(0, 2):
                 # obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                #else:
                 # obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 200)))




    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))

        #pygame.draw.rect(screen, 'Green', score_rect, 10)
        #pygame.draw.rect(screen, 'Green', score_rect)
        #screen.blit(score_surf, score_rect)
        score = display_score()
        highest_score = max(score, highest_score)
        # snail
        #snail_rect.x -= 5
       # if snail_rect.right <= 0:
       #     snail_rect.left = 800
        #screen.blit(snail_surf, snail_rect)
        # Player
        #player_gravity += 1
        #player_rect.y += player_gravity
        #if player_rect.bottom >= 300:
         #   player_rect.bottom = 300
        #play_animation()
        #screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #obstacle
        #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision_sprite()
        #game_active = collision(player_rect, obstacle_rect_list)


    else:
        screen.fill('turquoise')
        screen.blit(player_stand, player_stand_rect)
        screen.blit(Game_name, Game_rect)
        #obstacle_rect_list.clear()

        score_messge =text_font.render(f'Your score : {score} . Highest : {highest_score}', False, (11, 120, 169))
        score_messge_rect = score_messge.get_rect(center= (400, 320))
        if score == 0:
          screen.blit(Game_messege, Game_messege_rect)
        else:
            screen.blit(score_messge, score_messge_rect)



    pygame.display.update()
    Clock.tick(60)
