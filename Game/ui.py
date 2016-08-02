'''
Created on Dec 3, 2015

@author: aaronhu
'''
import pygame, sys, time, os
from pygame.locals import *

import game, utilities

import random
from screen import checkPersonIndex
g = game.Game()
pygame.init()

# Settings and constants
BUTTON_WIDTH, BUTTON_HEIGHT = (300, 64)
MUTE_BUTTON_WIDTH, MUTE_BUTTON_HEIGHT = (65, 64)
IS_QUIT_BUTTON = False
played_round = False
COLOR_TURQUOISE = (56, 255, 197)
COLOR_LIGHT_TURQUOISE = (133, 230, 255,240)
COLOR_MID_GREEN = (121, 189, 143)
COLOR_PURPLE = (255, 56, 115, 240)
COLOR_BLACK = (10, 10, 10)

COLOR_BUTTON_DOWN = (230, 230, 230)
COLOR_BUTTON_UP = (250, 250, 250)
COLOR_BUTTON_HOVER = COLOR_PURPLE
COLOR_BUTTON = (0,186,235,220)
COLOR_BUTTON_A = COLOR_BUTTON
COLOR_BUTTON_DISABLED = COLOR_PURPLE
COLOR_BACKGROUND = (56,214,255)
COLOR_DEFINITION = (250, 250, 250)
COLOR_MUTE_DOWN = (97, 56, 255)
COLOR_TEXT_SHADOW = (0, 130, 109)


def getAbsoluteResourcePath(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        try:
            basePath = os.path.dirname(sys.modules['difinitives'].__file__)
        except Exception:
            basePath = ''
            
        if not os.path.exists(os.path.join(basePath,relativePath)):
            basePath = 'difinitives'
    
    path= os.path.join(basePath, relativePath)
    
    if not os.path.exists(path):
        return None
    
    return path
                

FONT_INSTRUCTION = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data', 'f1.ttf')),28)
FONT_ICON = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data', 'flaticon.ttf')), 32)
FONT_UI = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data', 'Roboto-Light.ttf')), 32)
FONT_UI_BOLD = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data', 'Roboto-Bold.ttf')), 25)
FONT_TITLE = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data', 'Roboto-Bold.ttf')), 48)
FONT_MUTE = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data', 'flaticon2.ttf')), 32)
FONT_NEXT = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data', 'flaticon3.ttf')), 32)
FONT_PAUSE = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data','pause.ttf')),32)
FONT_CHOOSE = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data','choose.ttf')),35)
FONT_PEOPLE = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data','people.ttf')),250)
FONT_PERSON = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data','people.ttf')),45)
FONT_SAVE = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data','load.ttf')),45)
FONT_BACK = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data','back.ttf')),45)
FONT_HOME = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data','home.ttf')),45)
FONT_PROFILE = pygame.font.Font(getAbsoluteResourcePath(os.path.join('data', 'Roboto-Light.ttf')), 20)
SOUND_BUTTON = pygame.mixer.Sound(getAbsoluteResourcePath(os.path.join('data', 'click.wav')))

pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag

# song list for the game
_songs = ['game_music/1.wav', 'game_music/2.wav', 'game_music/3.wav', 'game_music/4.wav', 'game_music/5.wav']

_options = [''u'\ue000',''u'\ue001']

option_number = 0
# event for when the song ends
SONG_END = pygame.USEREVENT + 1

# default setting
_currently_playing_song = None

def set_screen(s):
    global screen
    screen = s

def play_songs():
    global _currently_playing_song, _songs
    pygame.mixer.music.set_volume(0.3)
    next_song = random.choice(_songs)
    while next_song == _currently_playing_song:
        next_song = random.choice(_songs)
    _currently_playing_song = next_song 
    pygame.mixer.music.set_endevent(SONG_END)
    pygame.mixer.music.load(next_song)
    pygame.mixer.music.play()
    return next_song

# UI stuff
mouse_pos = (0,0)
mouse_down = False
mouse_up = False

def button(screen,word,x,y,button_color=COLOR_BUTTON,font=FONT_UI):
    ''' A general purpose button. Returns true if clicked. '''
    width, height = (BUTTON_WIDTH, BUTTON_HEIGHT)

    clicked = False

    if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
        button_state = 'hover'
        if mouse_down:
            button_state = 'down'
            y += 2
        if mouse_up:
            clicked = True
    else:
        button_state = 'normal'

    if button_state == 'hover':
        text_color = COLOR_BUTTON_HOVER
    elif button_state == 'down':
        text_color = COLOR_BUTTON_DOWN
    else:
        text_color = COLOR_BUTTON_UP

    pygame.gfxdraw.box(screen, pygame.Rect(x + 2, y + 2, width - 4, height - 4), button_color)

    #pygame.draw.rect(screen,button_color,(x + 2, y + 2, width - 4, height - 4))
    centered_text(word, font, text_color, Rect(x, y, width, height), True)

    return clicked

def disabled_button(screen,word,x,y):
    ''' A disabled button used to display an incorrect guess. '''
    width, height = (BUTTON_WIDTH, BUTTON_HEIGHT)
    f = FONT_UI
    pygame.gfxdraw.box(screen, pygame.Rect(x + 2, y + 2, width - 4, height - 4), COLOR_BUTTON_DISABLED)
    centered_text(word, f, COLOR_MID_GREEN, Rect(x, y, width, height), False)

    icon = FONT_ICON
    s = icon.render(u'\ue006', 1, COLOR_MID_GREEN)
    screen.blit(s, (x+16, y+16))

def correct_button(screen, word, x, y):
    ''' A disabled button used to display a correct guess. '''
    width, height = (BUTTON_WIDTH, BUTTON_HEIGHT)
    f = FONT_UI
    pygame.gfxdraw.box(screen, pygame.Rect(x + 2, y + 2, width - 4, height - 4), COLOR_LIGHT_TURQUOISE)
    #pygame.draw.rect(screen, COLOR_LIGHT_TURQUOISE, (x + 2, y + 2, width - 4, height - 4))
    centered_text(word, f, COLOR_MID_GREEN, Rect(x, y, width, height), False)

    icon = FONT_ICON
    s = icon.render(u'\ue001', 1, COLOR_MID_GREEN)
    screen.blit(s, (x+16, y+16))

def centered_text(text, font, color, rect, shadow=False):
    ''' Draws center aligned text in a given rect. '''
    text_size = font.size(text)

    text_surface = font.render(text, 1, color)
    shadow_surface = font.render(text, 1, COLOR_TEXT_SHADOW)

    text_margin = ((rect.width - text_size[0]) / 2 , (rect.height - text_size[1]) / 2)
    if shadow: screen.blit(shadow_surface, (rect.x + text_margin[0] + 1, rect.y + text_margin[1] + 1))
    screen.blit(text_surface, (rect.x + text_margin[0], rect.y + text_margin[1]))

def timer_initial_state(screen):
    '''Creates an thin line representing the timer'''
    pygame.draw.line(screen,COLOR_PURPLE,(0,screen.get_height()*0.27), (screen.get_width(),screen.get_height()*0.27),5)

def show_mute_button(screen,x,y):
        width, height = (MUTE_BUTTON_WIDTH, MUTE_BUTTON_HEIGHT)
        clicked = False
        icon = FONT_MUTE

        if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
            button_state = 'hover'
            if mouse_down:
                button_state = 'down'
                y += 2
            if mouse_up:
                clicked = True
        else:
            button_state = 'normal'

        if button_state == 'hover':
            icon_color = COLOR_PURPLE
        elif button_state == 'down':
            icon_color = COLOR_MUTE_DOWN
        else:
            icon_color = COLOR_BUTTON_UP
        pygame.gfxdraw.box(screen, pygame.Rect(x + 2, y + 2, width - 4, height - 4), COLOR_BUTTON)

        #pygame.draw.rect(screen, COLOR_BUTTON_A,(x + 2, y + 2, width - 4, height - 4))

        s = icon.render(_options[option_number], 1, icon_color)
        screen.blit(s, (x+17, y+17)) 
        return clicked

def show_next_button(screen,x,y):
        width, height = (MUTE_BUTTON_WIDTH, MUTE_BUTTON_HEIGHT)
        clicked = False
        icon = FONT_NEXT

        if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
            button_state = 'hover'
            if mouse_down:
                button_state = 'down'
                y += 2
            if mouse_up:
                clicked = True
        else:
            button_state = 'normal'

        if button_state == 'hover':
            icon_color = COLOR_PURPLE
        elif button_state == 'down':
            icon_color = COLOR_MUTE_DOWN
        else:
            icon_color = COLOR_BUTTON_UP
        pygame.gfxdraw.box(screen, pygame.Rect(x + 2, y + 2, width - 4, height - 4), COLOR_BUTTON)

        s = icon.render(u'\ue000', 1, icon_color)
        screen.blit(s, (x+17, y+17)) 
        return clicked

def show_pause_button(screen,x,y):
        width,height = (MUTE_BUTTON_WIDTH,MUTE_BUTTON_HEIGHT)
        clicked = False
        icon = FONT_PAUSE
        if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
            button_state = 'hover'
            if mouse_down:
                button_state = 'down'
                y += 2
            if mouse_up:
                clicked = True
        else:
            button_state = 'normal'

        if button_state == 'hover':
            icon_color = COLOR_PURPLE
        elif button_state == 'down':
            icon_color = COLOR_MUTE_DOWN
        else:
            icon_color = COLOR_BUTTON_UP
        pygame.gfxdraw.box(screen, pygame.Rect(x + 2, y + 2, width - 4, height - 4), COLOR_BUTTON)

        s = icon.render(u'\ue000', 1, icon_color)
        screen.blit(s, (x+17, y+17)) 
        return clicked

def show_choose_button(screen,x,y):
        width,height = (MUTE_BUTTON_WIDTH,MUTE_BUTTON_HEIGHT)
        clicked = False
        icon = FONT_CHOOSE
        if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
            button_state = 'hover'
            if mouse_down:
                button_state = 'down'
                y += 2
            if mouse_up:
                clicked = True
        else:
            button_state = 'normal'

        if button_state == 'hover':
            icon_color = COLOR_PURPLE
        elif button_state == 'down':
            icon_color = COLOR_MUTE_DOWN
        else:
            icon_color = COLOR_BUTTON_UP
        
        pygame.gfxdraw.box(screen, pygame.Rect(x + 2, y + 2, width - 4, height - 4), (138,43,226,210))

        #pygame.draw.rect(screen, (138,43,226),(x + 2, y + 2, width - 4, height - 4))

        s = icon.render(u'\ue000', 1, icon_color)
        screen.blit(s, (x+17, y+17)) 
        return clicked

def show_people_button(screen,x,y,index):
        width,height = (250,250)
        clicked = False
        icon = FONT_PEOPLE
        if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
            button_state = 'hover'
            if mouse_down:
                button_state = 'down'
                y += 2
            if mouse_up:
                clicked = True
        else:
            button_state = 'normal'

        if button_state == 'hover':
            icon_color = COLOR_PURPLE
        elif button_state == 'down':
            icon_color = COLOR_MUTE_DOWN
        else:
            icon_color = COLOR_BUTTON_UP
            
        list=[u'\ue000',u'\ue001',u'\ue002',u'\ue003']
        #pygame.draw.rect(screen, COLOR_BUTTON,(x + 2, y + 2,150,150))
        
        s = icon.render(list[index], 1, icon_color)
        screen.blit(s, (x+17, y+17)) 
        return clicked

def show_save_button(screen,x,y):
        width,height = (MUTE_BUTTON_WIDTH,MUTE_BUTTON_HEIGHT)
        clicked = False
        icon = FONT_SAVE
        if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
            button_state = 'hover'
            if mouse_down:
                button_state = 'down'
                y += 2
            if mouse_up:
                clicked = True
        else:
            button_state = 'normal'

        if button_state == 'hover':
            icon_color = COLOR_PURPLE
        elif button_state == 'down':
            icon_color = COLOR_MUTE_DOWN
        else:
            icon_color = COLOR_BUTTON_UP
        pygame.gfxdraw.box(screen, pygame.Rect(x + 10, y + 10, width - 4, height - 4), (72,61,139,210))

        #pygame.draw.rect(screen, (72,61,139),(x + 10, y + 10, width - 4, height - 4))

        s = icon.render(u'\ue000', 1, icon_color)
        screen.blit(s, (x+17, y+17)) 
        return clicked

def show_home_button(screen,x,y):
        width,height = (MUTE_BUTTON_WIDTH,MUTE_BUTTON_HEIGHT)
        clicked = False
        icon = FONT_HOME
        if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
            button_state = 'hover'
            if mouse_down:
                button_state = 'down'
                y += 2
            if mouse_up:
                clicked = True
        else:
            button_state = 'normal'

        if button_state == 'hover':
            icon_color =(0,191,255)
        elif button_state == 'down':
            icon_color = COLOR_MUTE_DOWN
        else:
            icon_color = COLOR_BUTTON_UP

        #pygame.draw.rect(screen, COLOR_BUTTON,(x + 10, y + 10, width - 4, height - 4))

        s = icon.render(u'\ue000', 1, icon_color)
        screen.blit(s, (x+17, y+17)) 
        return clicked

def show_profile_button(screen,x,y,index,score,ps):
        width,height = (40,75)
        clicked = False
        icon = FONT_PERSON
        if ((mouse_pos[0] > x) and (mouse_pos[0] < x+width) and (mouse_pos[1] > y) and (mouse_pos[1] < y+height)):
            button_state = 'hover'
            if mouse_down:
                button_state = 'down'
                y += 2
            pygame.gfxdraw.box(screen, pygame.Rect(x+50, y+70, width+150, height+35), (30,144,255,150))
            name = checkPersonIndex(index)
            scorestr = 'Score: '+str(score)
            passstr = 'used'
            if ps:
                passstr = 'not used'
            centered_text(name, FONT_PROFILE, COLOR_PURPLE, Rect(x+120,y+53,width,height), True)
            centered_text(scorestr, FONT_PROFILE, COLOR_DEFINITION, Rect(x+120,y+85,width,height), False)
            centered_text('Help: '+passstr, FONT_PROFILE, COLOR_DEFINITION, Rect(x+120,y+115,width,height), False)
            if mouse_up:
                clicked = True
        else:
            button_state = 'normal'
        if button_state == 'hover':
            icon_color = COLOR_LIGHT_TURQUOISE
            pygame.gfxdraw.box(screen, pygame.Rect(x+50, y+70, width+150, height+35), (30,144,255,150))
            name = checkPersonIndex(index)
            scorestr = 'Score: '+str(score)
            passstr = 'used'
            if ps:
                passstr = 'not used'
            centered_text(name, FONT_PROFILE, COLOR_PURPLE, Rect(x+120,y+53,width,height), True)
            centered_text(scorestr, FONT_PROFILE, COLOR_DEFINITION, Rect(x+120,y+85,width,height), False)
            centered_text('Help: '+passstr, FONT_PROFILE, COLOR_DEFINITION, Rect(x+120,y+115,width,height), False)
            
        elif button_state == 'down':
            icon_color = COLOR_MUTE_DOWN
        else:
            icon_color = COLOR_BUTTON_UP
            
        list=[u'\ue000',u'\ue001',u'\ue002',u'\ue003']
        #pygame.draw.rect(screen, COLOR_BUTTON,(x + 2, y + 2,150,150))
        
        s = icon.render(list[index], 1, icon_color)
        screen.blit(s, (x+17, y+17)) 
        return clicked