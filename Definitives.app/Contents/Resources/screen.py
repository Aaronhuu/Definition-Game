'''
Created on Dec 3, 2015

@author: aaronhu
'''
import pygame, sys, time, os
from pygame.locals import *
import pygame.gfxdraw
import random, math

import ui, game, utilities, ReadExcel
from ReadExcel import savename

WORD_TIME = 10 # seconds
SETTING_FULLSCREEN = False
SONG_END = pygame.USEREVENT + 1
SONG_MUTED = False
pause=False
display_width=1280
display_height=700
white=(255,255,255)
clock = pygame.time.Clock()
blurbg= pygame.image.load('data/blurbg.jpg')
bg1 = pygame.image.load('data/bg1.jpg')
bg2 = pygame.image.load('data/space.jpg')
bg3 = pygame.image.load('data/bg3.jpg')
icon= pygame.image.load('data/icon.png')
leftwing = pygame.image.load('data/leftwing.png')
rightwing = pygame.image.load('data/rightwing.png')
pythonlogo = pygame.image.load('data/Python.png')
pygamelogo = pygame.image.load('data/pygame_logo.png')

pygame.display.set_icon(icon)
personIndex = 0



class Screen(object):
    prev_time = 0
    delta_time = 0
    def display(self, screen):
        """Main draw method called every frame"""
        # Calculate delta time in milliseconds.  This is used for animations.
        if self.prev_time == 0:
            self.delta_time = 0
        else:
            self.delta_time = pygame.time.get_ticks() - self.prev_time
        self.prev_time = pygame.time.get_ticks()

    def show_music_controls(self, screen):
        """Draw music controls"""
        CLICK_STATUS = ui.show_mute_button(screen,15,screen.get_height() - 16 - 60)
        NEXT_SONG_STATUS = ui.show_next_button(screen,80,screen.get_height()- 16 - 60)
        #PAUSE = ui.show_pause_button(screen, 145, screen.get_height()-16-60)
        # Code for muting the in game_music
        global SONG_MUTED

        if CLICK_STATUS:
            if SONG_MUTED:
                ui.COLOR_BUTTON_A = ui.COLOR_BUTTON
                pygame.mixer.music.set_volume(0.3)
                ui.option_number = 0
                ui.show_mute_button(screen,15,screen.get_height() - 16 - 64)
                SONG_MUTED = False
            
            else:
                ui.COLOR_BUTTON_A = ui.COLOR_BLACK
                pygame.mixer.music.set_volume(0)
                ui.option_number = -1
                ui.show_mute_button(screen,15,screen.get_height() - 16 - 64)
                SONG_MUTED = True
            

        new_song = None
        if NEXT_SONG_STATUS:
            new_song = ui.play_songs()
            pygame.mixer.music.load(new_song)
            pygame.mixer.music.play()
            if SONG_MUTED == True:
                pygame.mixer.music.set_volume(0)
    
    def show_pause_control(self,screen):
        PAUSE = ui.show_pause_button(screen, 145, screen.get_height()-16-60)
        if PAUSE:  
                
                global pause
                pause=True
                paused()

class GameScreen(Screen):
    def __init__(self):
        self.words = dict(g.get_words())
        self.reset()
        self.keyset= list(self.words.keys())
        random.shuffle(self.keyset)

    disabled_words, correct_words = ([], [])
    time_in_round = WORD_TIME # seconds
    timer = time_in_round

    def reset_timer(self):
        """Resets the timer"""
        self.timer = self.time_in_round

    def reset(self):
        """Resets the screen"""
        self.reset_timer()
        self.disabled_words, self.correct_words = ([], [])

    def show_definition(self, screen):
        """Draws definition panel with definition."""
        light_green = (56,214,255,150)
        pygame.gfxdraw.box(screen, pygame.Rect(0, screen.get_height()*0.07, screen.get_width(), screen.get_height()*0.20), light_green)
        f = ui.FONT_UI_BOLD

        lines = utilities.word_wrap(g.get_definition())
        line_height = f.get_linesize()
        text_size = f.size(lines[0])
        text_margin = ((screen.get_width() - text_size[0]) / 2 , (screen.get_height()*0.20 - line_height*len(lines)) / 2)
        for i, line in enumerate(lines):
            text_surface = f.render(line, 1, ui.COLOR_DEFINITION)
            shadow_surface = f.render(line, 1, ui.COLOR_TEXT_SHADOW)
            screen.blit(shadow_surface, (0 + text_margin[0] + 1, screen.get_height() * 0.05 + i * line_height + text_margin[1] + 1))
            screen.blit(text_surface, (0 + text_margin[0], screen.get_height() * 0.05 + i * line_height + text_margin[1]))

    def show_score_and_round(self, screen):
        """Draws top panel which displays the score and round."""
        score_text = 'Score: ' + str(g._score)
        round_text = 'Round: ' + str('{0:2.0f}'.format(g._round))
        f = ui.FONT_UI_BOLD
        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.07))
        ui.centered_text(score_text, f, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*0.5, screen.get_height()*0.07), True)
        ui.centered_text(round_text, f, ui.COLOR_DEFINITION, Rect(screen.get_width()*0.5, 0, screen.get_width()*0.5, screen.get_height()*0.07), True)

    def show_bottom_panel(self, screen):
        """Draws bottom panel used for grouping quit and settings options."""
        COLOR_LIGHT_TURQUOISE = (133, 230, 255,150)
        pygame.gfxdraw.box(screen, pygame.Rect(0, screen.get_height()*0.85, screen.get_width(), screen.get_height()*0.15), COLOR_LIGHT_TURQUOISE)
        
        #pygame.draw.rect(screen, ui.COLOR_LIGHT_TURQUOISE, (0, screen.get_height()*0.85, screen.get_width(), screen.get_height()*0.15))
        ui.centered_text(str('{0:2.1f}'.format(self.timer)) + " s",ui.FONT_INSTRUCTION,ui.COLOR_DEFINITION,Rect(screen.get_width()*0.17,screen.get_height()-94,screen.get_width()*0.65,screen.get_height()*0.1), False)
               
    def show_typed_words(self, screen):
        """Draws text that player is typing"""
        ui.centered_text(input_handler.key_buffer, ui.FONT_UI_BOLD, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.27, screen.get_width(), screen.get_height()), True)

    def show_words(self, screen):
        """Draws word buttons"""
        button_offset_y = screen.get_height() * 0.35 + 64
        button_offset_x = (screen.get_width() - ui.BUTTON_WIDTH * 4) / 2
        button_row = 0
        button_col = 0
        # big mess for organizing buttons in grid
        for w in self.keyset:
            if button_col == 4:
                button_row += 1
                button_col = 0
            if w in self.disabled_words:
                ui.disabled_button(screen, w, button_offset_x + ui.BUTTON_WIDTH * button_col, button_offset_y + 64 * button_row)
            elif w in self.correct_words:
                ui.correct_button(screen, w, button_offset_x + ui.BUTTON_WIDTH*button_col, button_offset_y + 64 * button_row)
            elif ui.button(screen, w, button_offset_x + ui.BUTTON_WIDTH * button_col, button_offset_y + 64 * button_row):
                if g.check_word(w): # game logic stuff like this shouldn't be here
                    self.correct(w)
                else: # and this
                    self.incorrect(w)
                pass
            button_col += 1

        return w

    def choose_new_def(self):
        """Chooses a new random definition"""
        if g.has_words():
            self.reset_timer()
            word, defn = g.choose_random_definition()
        else:
            if g.next_round():
                change_screen(RoundEndScreen())
            else:
                change_screen(GameOverScreen())

    def correct(self, word):
        """Called when correct word is guessed"""
        row_num = ReadExcel.getRowNumber(word)
        self.correct_words += [word]
        g._score += ReadExcel.getScore(row_num)
        g._words.pop(word, None)
        self.choose_new_def()

    def incorrect(self, word):
        """Does stuff when incorrect word is guessed"""
        self.disabled_words += [word]
        g._words.pop(word, None)

    def show_timer(self, screen):
        """Draws and updates the timer"""
        self.timer -= self.delta_time * (0.001)
        
        if self.timer < 0:
            self.timer = 0
            self.incorrect(g.get_word())
            self.choose_new_def()
        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, screen.get_height()*0.27, screen.get_width() * (self.timer / self.time_in_round), screen.get_height()*0.01))
          
        
    def display(self, screen):
        """Main method for screen which draws everything"""
        super(GameScreen, self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        #bg9=bg2.convert_alpha().set_alpha(200)
        screen.blit(bg2,(0,0))
        self.show_definition(screen)
        self.show_words(screen)
        self.show_score_and_round(screen)
        self.show_bottom_panel(screen)
        self.show_timer(screen)
        self.show_typed_words(screen)
        self.show_pause_control(screen)
        self.show_music_controls(screen)
        if ui.show_profile_button(screen, -5, -15, personIndex,g._total_score+g._score,g._pass) and g._pass:
            self.correct(g.get_word())
            g._pass = False
        # Quit button
        if ui.button(screen, 'Quit', screen.get_width() - ui.BUTTON_WIDTH - 16, screen.get_height() - 16 - 64, ui.COLOR_PURPLE, font=ui.FONT_UI_BOLD):
            change_screen(GameOverScreen())

class SplashScreen(Screen):
    ticker = 0
    def __init__(self):
        g.new_game()
        input_handler.reset_key_buffer()

    def display(self, screen):
        super(SplashScreen, self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        screen.blit(bg1,(0,0))
        self.show_music_controls(screen)

        self.ticker += self.delta_time * 0.001
        if self.ticker > 2 * math.pi: self.ticker = 0

        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.1))
        ui.centered_text('Definition Game',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0 + math.sin(self.ticker) * 10, screen.get_width(), screen.get_height()*0.1), True)
        if ui.button(screen,'New Game',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5-ui.BUTTON_HEIGHT-10,(255,215,0)) or pygame.key.get_pressed()[pygame.K_RETURN]:
            change_screen(choosePersonScreen())
        if ui.button(screen,'Load Game',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5-10,(255,127,80,230)):
            change_screen(choseRoundScreen())
        if ui.button(screen,'How to play',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5+ui.BUTTON_HEIGHT-10,(255,99,71,230)):
            change_screen(howToPlayScreen())
        if ui.button(screen,'Quit',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5+ui.BUTTON_HEIGHT*2-10,(255,0,0)):
            quit()

class choseRoundScreen(Screen):
    def __init__(self):
        self.words = None
        
    def display(self, screen):
        super(choseRoundScreen,self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        screen.blit(bg3,(0,0))
        self.show_music_controls(screen)
        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.1))
        ui.centered_text('LoadGame',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width(), screen.get_height()*0.1), True)
        ui.centered_text('Name: ' + str(ReadExcel.loadname(1))+' Score: '+str('{0:2.0f}'.format(ReadExcel.loadscore(1)))+' Round: '+str('{0:2.0f}'.format(ReadExcel.loadround(1))),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.2, screen.get_width(), screen.get_height()*0.2), True)
        ui.centered_text('Name: ' + str(ReadExcel.loadname(2))+' Score: '+str('{0:2.0f}'.format(ReadExcel.loadscore(2)))+' Round: '+str('{0:2.0f}'.format(ReadExcel.loadround(2))),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.3, screen.get_width(), screen.get_height()*0.3), True)
        ui.centered_text('Name: ' + str(ReadExcel.loadname(3))+' Score: '+str('{0:2.0f}'.format(ReadExcel.loadscore(3)))+' Round: '+str('{0:2.0f}'.format(ReadExcel.loadround(3))),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.4, screen.get_width(), screen.get_height()*0.4), True)
        ui.centered_text('Name: ' + str(ReadExcel.loadname(4))+' Score: '+str('{0:2.0f}'.format(ReadExcel.loadscore(4)))+' Round: '+str('{0:2.0f}'.format(ReadExcel.loadround(4))),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.5, screen.get_width(), screen.get_height()*0.5), True)
        if ui.show_choose_button(screen, screen.get_width()*0.1, screen.get_height()*0.25):
            g._total_score = ReadExcel.loadscore(1)
            g._last_round_score = ReadExcel.loadscore(1)
            g._round = ReadExcel.loadround(1) 
            g._words = g.load_words_for_round(-1,True,g._round)
            g._player = ReadExcel.loadname(1)
            ui.played_round = True
            g_word, g._definition = g.choose_random_definition()
            checkPerson(ReadExcel.loadname(1))
            change_screen(RoundEndScreen())
        if ui.show_choose_button(screen, screen.get_width()*0.1, screen.get_height()*0.4):
            g._total_score = ReadExcel.loadscore(2)
            g._last_round_score = ReadExcel.loadscore(2)
            g._round = ReadExcel.loadround(2) 
            ui.played_round = True
            g._words = g.load_words_for_round(-1,True,g._round)
            g._player = ReadExcel.loadname(2)
            g_word, g._definition = g.choose_random_definition()
            checkPerson(ReadExcel.loadname(2))
            change_screen(RoundEndScreen())
        if ui.show_choose_button(screen, screen.get_width()*0.1, screen.get_height()*0.55):
            g._total_score = ReadExcel.loadscore(3)
            g._last_round_score = ReadExcel.loadscore(3)
            g._round = ReadExcel.loadround(3)
            ui.played_round = True
            g._words = g.load_words_for_round(-1,True,g._round)
            g._player = ReadExcel.loadname(3)
            g_word, g._definition = g.choose_random_definition()
            checkPerson(ReadExcel.loadname(3))
            change_screen(RoundEndScreen())
        if ui.show_choose_button(screen, screen.get_width()*0.1, screen.get_height()*0.70):
            g._total_score = ReadExcel.loadscore(4)
            g._last_round_score = ReadExcel.loadscore(4)
            g._round = ReadExcel.loadround(4)
            ui.played_round = True
            g._player = ReadExcel.loadname(4)
            g._words = g.load_words_for_round(-1,True,g._round+1)
            g_word, g._definition = g.choose_random_definition()
            checkPerson(ReadExcel.loadname(4))
            change_screen(RoundEndScreen())
        if ui.button(screen,'Back',screen.get_width()*0.3-ui.BUTTON_WIDTH/2,screen.get_height()*0.75+ui.BUTTON_HEIGHT,(238,232,170,240)):
            change_screen(SplashScreen())
        if ui.button(screen,'Quit',screen.get_width()*0.7-ui.BUTTON_WIDTH/2,screen.get_height()*0.75+ui.BUTTON_HEIGHT,(255,0,0)):
            pygame.quit()
            quit()
        if ui.show_home_button(screen, 0, -2):
            change_screen(SplashScreen())

class saveGameScreen(Screen):
    def display(self, screen):
        super(saveGameScreen,self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        screen.blit(bg3,(0,0))
        self.show_music_controls(screen)
        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.1))
        ui.centered_text('SaveGame',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width(), screen.get_height()*0.1), True)
        ui.centered_text('Name: ' + str(ReadExcel.loadname(1))+' Score: '+str('{0:2.0f}'.format(ReadExcel.loadscore(1)))+' Round: '+str('{0:2.0f}'.format(ReadExcel.loadround(1))),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.2, screen.get_width(), screen.get_height()*0.2), True)
        ui.centered_text('Name: ' + str(ReadExcel.loadname(2))+' Score: '+str('{0:2.0f}'.format(ReadExcel.loadscore(2)))+' Round: '+str('{0:2.0f}'.format(ReadExcel.loadround(2))),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.3, screen.get_width(), screen.get_height()*0.3), True)
        ui.centered_text('Name: ' + str(ReadExcel.loadname(3))+' Score: '+str('{0:2.0f}'.format(ReadExcel.loadscore(3)))+' Round: '+str('{0:2.0f}'.format(ReadExcel.loadround(3))),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.4, screen.get_width(), screen.get_height()*0.4), True)
        ui.centered_text('Name: ' + str(ReadExcel.loadname(4))+' Score: '+str('{0:2.0f}'.format(ReadExcel.loadscore(4)))+' Round: '+str('{0:2.0f}'.format(ReadExcel.loadround(4))),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.5, screen.get_width(), screen.get_height()*0.5), True)
        if ui.show_save_button(screen, screen.get_width()*0.1, screen.get_height()*0.25):
            ReadExcel.savename(1,g._player)
            ReadExcel.savescore(1,g._total_score)
            ReadExcel.saveround(1,g._round)
        if ui.show_save_button(screen, screen.get_width()*0.1, screen.get_height()*0.4):
            ReadExcel.savename(2,g._player)
            ReadExcel.savescore(2,g._total_score)
            ReadExcel.saveround(2,g._round)
        if ui.show_save_button(screen, screen.get_width()*0.1, screen.get_height()*0.55):
            ReadExcel.savename(3,g._player)
            ReadExcel.savescore(3,g._total_score)
            ReadExcel.saveround(3,g._round)
        if ui.show_save_button(screen, screen.get_width()*0.1, screen.get_height()*0.70):
            ReadExcel.savename(4,g._player)
            ReadExcel.savescore(4,g._total_score)
            ReadExcel.saveround(4,g._round)
        if ui.button(screen,'Back',screen.get_width()*0.3-ui.BUTTON_WIDTH/2,screen.get_height()*0.75+ui.BUTTON_HEIGHT,(238,232,170,240)):
            change_screen(RoundEndScreen())
        if ui.button(screen,'Quit',screen.get_width()*0.7-ui.BUTTON_WIDTH/2,screen.get_height()*0.75+ui.BUTTON_HEIGHT,(255,0,0)):
            pygame.quit()
            quit()
        if ui.show_home_button(screen, 0, -2):
            change_screen(SplashScreen())

class howToPlayScreen(Screen):
    def display(self, screen):
        super(howToPlayScreen,self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        screen.blit(bg1,(0,0))
        self.show_music_controls(screen)
        #screen.blit(pythonlogo,(900,30))
        
        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.1))
        screen.blit(pygamelogo,(1050,3))
        ui.centered_text('How to play.',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width(), screen.get_height()*0.1), True)
        ui.show_mute_button(screen, 150, 130)
        ui.centered_text('Mute the sound',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*0.65, screen.get_height()*0.46), True)
        ui.show_next_button(screen, 150, 210)
        ui.centered_text('Next song',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*0.56, screen.get_height()*0.7), True)
        ui.show_pause_button(screen, 150, 290)
        ui.centered_text('Pause',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*0.49, screen.get_height()*0.93), True)
        ui.show_choose_button(screen, 150, 370)
        ui.centered_text('Load Game',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*0.58, screen.get_height()*1.15), True)
        ui.show_save_button(screen, 142, 450)
        ui.centered_text('Save Game',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*0.58, screen.get_height()*1.39), True)
        ui.show_home_button(screen, 700, 130)
        ui.centered_text('Home',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*1.35, screen.get_height()*0.46), True)
        ui.show_profile_button(screen, 700, 210,0,0,True)
        ui.centered_text('Amy',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*1.35, screen.get_height()*0.7), True)
        ui.show_profile_button(screen, 700, 290,1,0,True)
        ui.centered_text('Aaron',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*1.35, screen.get_height()*0.93), True)
        ui.show_profile_button(screen, 700, 370,2,0,True)
        ui.centered_text('James',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*1.35, screen.get_height()*1.15), True)
        ui.show_profile_button(screen, 700, 450,3,0,True)
        ui.centered_text('Lina',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width()*1.35, screen.get_height()*1.39), True)

        if ui.button(screen,'Back',screen.get_width()*0.3-ui.BUTTON_WIDTH/2,screen.get_height()*0.75+ui.BUTTON_HEIGHT,(238,232,170,240)):
            change_screen(SplashScreen())
        if ui.button(screen,'Next',screen.get_width()*0.7-ui.BUTTON_WIDTH/2,screen.get_height()*0.75+ui.BUTTON_HEIGHT,(0,206,209,240)):
            change_screen(HowToPlayScreen2())
        if ui.show_home_button(screen, 0, -2):
            change_screen(SplashScreen())

class HowToPlayScreen2(Screen):
    def display(self, screen):
        super(HowToPlayScreen2, self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        screen.blit(bg1,(0,0))
        self.show_music_controls(screen)

        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.1))
        ui.centered_text('Game Rules',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width(), screen.get_height()*0.1), True)
        ui.centered_text('1. Before a round starts you have to choose a person as your player.',  ui.FONT_INSTRUCTION, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.16, screen.get_width()*0.75+75, screen.get_height()*0.1),True)
        ui.centered_text('2. You would be given a definition and a set of 12 words each round to choose from.',  ui.FONT_INSTRUCTION, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.24, screen.get_width()*0.91+100, screen.get_height()*0.1),True)
        ui.centered_text('3. If a word you choose is wrong it is disabled and you score no marks. ',  ui.FONT_INSTRUCTION, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.32, screen.get_width()*0.785+80, screen.get_height()*0.1),True)
        ui.centered_text('4. If you score a word right, you are awarded marks.',  ui.FONT_INSTRUCTION, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.40, screen.get_width()*0.6+50, screen.get_height()*0.1),True)
        ui.centered_text('5. You can save a game  when you finish the round. QUIT with no mark.',  ui.FONT_INSTRUCTION, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.48, screen.get_width()*0.84+13, screen.get_height()*0.1),True)
        ui.centered_text('6. For now, when you past 4 rounds, the game is over.',  ui.FONT_INSTRUCTION, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.56, screen.get_width()*0.62+55, screen.get_height()*0.1),True)
        ui.centered_text('7. You would see your total score when finish the game.',  ui.FONT_INSTRUCTION, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.64, screen.get_width()*0.64+57, screen.get_height()*0.1),True)
        ui.centered_text('8. You can click the profile of your player to get one free help for each round.',  ui.FONT_INSTRUCTION, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.72, screen.get_width()*0.84+93, screen.get_height()*0.1),True)

        if ui.show_home_button(screen, 0, -2):
            change_screen(SplashScreen())
        if ui.button(screen,'Back',screen.get_width()*0.3-ui.BUTTON_WIDTH/2,screen.get_height()*0.75+ui.BUTTON_HEIGHT,(238,232,170,240)):
            change_screen(howToPlayScreen())
        if ui.button(screen,'New Game',screen.get_width()*0.7-ui.BUTTON_WIDTH/2,screen.get_height()*0.75+ui.BUTTON_HEIGHT,(255,215,0)):
            change_screen(choosePersonScreen())

class RoundEndScreen(Screen):
    def display(self, screen):
        super(RoundEndScreen, self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        screen.blit(bg1,(0,0))
        self.show_music_controls(screen)
        g._pass = True
        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.1))
        ui.centered_text('The round is finished.',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width(), screen.get_height()*0.1), True)
        ui.centered_text('Your score was ' + str(g.get_last_round_score()),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.1, screen.get_width(), screen.get_height()*0.1), True)
        if ui.button(screen,'Next Round',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5-ui.BUTTON_HEIGHT,(0,191,255,250)) or pygame.key.get_pressed()[pygame.K_RETURN]:
            if ui.played_round:
                g._round+=1
                ui.played_round = False
            change_screen(GameScreen())
        if ui.button(screen,'Save Game',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5,(100,149,237,240)) or pygame.key.get_pressed()[pygame.K_RETURN]:
            change_screen(saveGameScreen())
        if ui.button(screen,'Quit',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5+ui.BUTTON_HEIGHT,(255,0,0)):
            quit()
        if ui.show_home_button(screen, 0, -2):
            change_screen(SplashScreen())

class choosePersonScreen(Screen):
    def display(self, screen):
        global personIndex
        super(choosePersonScreen,self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        screen.blit(bg1,(0,0))

        self.show_music_controls(screen)
        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.1))
        ui.centered_text('Choose a person as your player.',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width(), screen.get_height()*0.1), True)
        if ui.show_people_button(screen, screen.get_width()*0.2,screen.get_height()*0.1, 0):
            g._player='Amy'
            personIndex = 0
            g._pass = True
            change_screen(GameScreen())
        if ui.show_people_button(screen, screen.get_width()*0.55,screen.get_height()*0.1, 1):
            g._player='Aaron'
            personIndex = 1
            g._pass = True
            change_screen(GameScreen())
        if ui.show_people_button(screen, screen.get_width()*0.2,screen.get_height()*0.55, 2):
            g._player='James'
            personIndex = 2
            g._pass = True
            change_screen(GameScreen())
        if ui.show_people_button(screen, screen.get_width()*0.55,screen.get_height()*0.55, 3):
            g._player='Lina'
            personIndex = 3
            g._pass = True
            change_screen(GameScreen())
        if ui.show_home_button(screen, 0, -2):
            change_screen(SplashScreen())
        ui.centered_text('Amy',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.22, screen.get_width()*0.25, screen.get_height()*0.22), True)
        ui.centered_text('Aaron',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.22, screen.get_width()*1.70, screen.get_height()*0.22), True)
        ui.centered_text('James',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.42, screen.get_width()*0.25, screen.get_height()*0.62), True)
        ui.centered_text('Lina',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.42, screen.get_width()*1.7, screen.get_height()*0.62), True)

class GameOverScreen(Screen):
    def display(self, screen):
        super(GameOverScreen, self).display(screen)
        screen.fill(ui.COLOR_BACKGROUND)
        screen.blit(bg1,(0,0))
        self.show_music_controls(screen)

        pygame.draw.rect(screen, ui.COLOR_PURPLE, (0, 0, screen.get_width(), screen.get_height()*0.1))
        ui.centered_text('Game Over!',  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, 0, screen.get_width(), screen.get_height()*0.1), True)
        pygame.draw.rect(screen, ui.COLOR_PURPLE, (254, screen.get_height()*0.2, screen.get_width()*0.6, screen.get_height()*0.25))
        ui.centered_text('Your score was ' + str(g.get_total_score()) + '/' + str(g.get_max_total_score()),  ui.FONT_TITLE, ui.COLOR_DEFINITION, Rect(0, screen.get_height()*0.2, screen.get_width(), screen.get_height()*0.25), True)
        
        if ui.button(screen,'Play Again',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5,(255,215,0)) or pygame.key.get_pressed()[pygame.K_RETURN]:
            change_screen(SplashScreen())

        if ui.button(screen,'Quit',screen.get_width()*0.5-ui.BUTTON_WIDTH/2,screen.get_height()*0.5+ui.BUTTON_HEIGHT,(255,0,0)):
            quit()
        if ui.show_home_button(screen, 0, -2):
            change_screen(SplashScreen())


######################award here##########
def change_screen(screen):
    """Sets the current screen being shown"""
    global current_screen
    current_screen = screen

def text_objects(text,font,color):
    textSurface = font.render(text,True, color)
    return textSurface, textSurface.get_rect()

def unpause():
    global pause
    pause = False

def paused():
    screen.blit(blurbg,(0,-1))
    
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects("Paused",largeText,white)
    TextRect.center = ((display_width/2),(display_height/2-65))
    screen.blit(TextSurf,TextRect)
    largeText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf, TextRect = text_objects("Press any key to continue",largeText,white)
    TextRect.center = ((display_width/2),(display_height/2+85))
    screen.blit(TextSurf,TextRect)
    while pause:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 quit()
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_SPACE or pygame.K_RETURN:
                     unpause() 
        pygame.display.update()
        clock.tick(15)

def quit():
    """Quits game"""
    pygame.quit()
    sys.exit()

def checkPerson(name):
    global personIndex
    if name == 'Amy':
        personIndex = 0
    elif name == 'Aaron':
        personIndex = 1
    elif name == 'James':
        personIndex = 2
    elif name == 'Lina':
        personIndex = 3

def checkPersonIndex(index):
    if index == 0:
        return 'Amy'
    elif index == 1:
        return  'Aaron'
    elif index == 2:
        return  'James'
    elif index == 3:
        return  'Lina'

class InputHandler(object):
    """InputHandler takes pygame events and handles inputs to do things like word typing"""
    key_buffer = u''

    def __init__(self):
        pass

    def handle_event(self, event):
        """Handles pygame events"""

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONUP:
            ui.mouse_down = False
            ui.mouse_up = True
        if event.type == MOUSEBUTTONDOWN:
            ui.mouse_down = True
        if event.type == MOUSEMOTION:
            ui.mouse_pos = event.pos
        if event.type == KEYDOWN:
            if len(event.unicode) > 0 and ord(event.unicode) < 128:
                self.key_buffer += event.unicode
            tmp = dict(g._words)
            for w in tmp:
                if w in self.key_buffer and isinstance(current_screen, GameScreen):
                    if g.check_word(w):
                        current_screen.correct(w)
                        self.reset_key_buffer()
                    else:
                        current_screen.incorrect(w)
                        self.reset_key_buffer()
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_RETURN:
                self.reset_key_buffer()
            if event.key == K_BACKSPACE:
                self.key_buffer = self.key_buffer[:len(self.key_buffer)-2]
            if event.key == K_RIGHT and g._pass: # cheat
                self.key_buffer = g.get_word()
                g._pass=False
        if event.type == KEYUP:
            pass
        if event.type == SONG_END:
            ui.play_songs()
            if SONG_MUTED == True:
                pygame.mixer.music.set_volume(0)

    def reset_key_buffer(self):
        """Clears key buffer"""
        self.key_buffer = ''

if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(200,50)

    # Screen initialization
    modes = pygame.display.list_modes()
    pygame.display.set_caption("Definition Game")
    if SETTING_FULLSCREEN:
        screen = pygame.display.set_mode(modes[0], pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)
    else:
        screen = pygame.display.set_mode((1280,700), pygame.DOUBLEBUF | pygame.HWSURFACE)

    ui.set_screen(screen)

    # Game initialization
    input_handler = InputHandler()
    g = game.Game()
    g.new_game()

    # Set screen to splash screen to start
    change_screen(SplashScreen())
    ui.play_songs()

    # Main loop
    while True:
        ui.mouse_up = False
        # Event loop
        for event in pygame.event.get():
            input_handler.handle_event(event)
           
                    
        current_screen.display(screen)
        pygame.display.update()
        time.sleep(0.01)
    pass