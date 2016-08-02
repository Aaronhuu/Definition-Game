'''
Created on Dec 3, 2015

@author: aaronhu
'''
import subprocess
import sys
import random
import ReadExcel


class Game:
    _player='Nobody'
    _score = 0
    _last_round_score = 0
    _total_score = 0
    _round = 0
    WORDS_IN_ROUND = 12
    _words = {}
    _definition = u''
    _word = u''
    _message = u''
    _pass = True
    
    def new_game(self):
        """Starts a new game, resetting scores and sets round to 1."""
        self._total_score = 0
        self._last_round_score = 0
        self._score = 0
        self._round = 1
        self._words = self.load_words_for_round(self._round)
        self._word, self._definition = self.choose_random_definition()

    def get_definition(self):
        """Returns the current definition."""
        return self._definition

    def get_word(self):
        """Returns the current definition's word. (what the player is trying to guess)"""
        return self._word

    def get_words(self,forcedRound = None, roundNum = None):
        """Returns the current words available."""
        if(forcedRound == True):
            self.words = self.load_words_for_round(-1, forced_round = True, roundNum = roundNum)
        return self._words

    def get_round(self):
        """Returns the current round number."""
        return self._round

    def get_round_count(self):
        """Returns number of rounds from database."""
        return ReadExcel.getMaxRound()

    def get_score(self):
        """Returns players current score."""
        return self._score

    def get_last_round_score(self):
        """Returns players score from last round."""
        return self._last_round_score

    def get_total_score(self):
        """Returns players total score."""
        return self._total_score

    def get_max_total_score(self):
        """Returns total score possible from all words."""
        return ReadExcel.getTotalScore()

    def next_round(self):
        """Progresses game to next round by tallying scores and loading new words."""
        self._total_score += self._score
        self._last_round_score = self._score
        self._score = 0

        if self._round < self.get_round_count():
            self._round += 1
            self._words = self.load_words_for_round(self._round)
            self._word, self._definition = self.choose_random_definition()
            return True
        else:
            return False

    def load_words_for_round(self, rnd, forced_round = None,roundNum = None):
        """Query databsae for words in round"""
        if forced_round == True:
            words = ReadExcel.getWordsFromRound(roundNum)
        else:
            words = ReadExcel.getWordsFromRound(rnd)
            
        #rarray=[0,1,2,3,4,5,6,7,8,9,10,11]
        #random.shuffle(rarray)
        #wordsrom={}
        #for i in range(0,12):
        #wordsrom+=words[self._words.keys()]
        return words
            
    def has_words(self):
        """Returns true if game has words left to be guessed."""
        return len(list(self._words.keys())) > 0

    def choose_random_definition(self):
        """Chooses a random definition for the player to guess."""
        if len(list(self._words.keys())) > 0:
            random_word = random.choice(list(self._words.keys()))
            self._definition = self._words[random_word]
            self._word = random_word
            return random_word, self._definition

    def check_word(self, word):
        """Checks if word given is equal to the current definition's word."""
        word = word.lower()
        if word in list(self._words.keys()):
            if (self._definition == self._words[word]) == True:
                self._message = 'Correct!'
                return True
            else:
                self._message = 'Incorrect! :('
                return False
        else:
            self._message = 'Word not a choice! Try again.'
            return False

    def display_words(self):
        """Displays list of words that player can choose from."""
        words = ''
        for word in list(self._words.keys()):
            words += word + ', '
        print('Word Choices: ' + words)

    def display_definition(self):
        """Prints the current definition which the player is to guess."""
        print('Definition: ' + self._definition)

    def display_message(self):
        """Displays a message"""
        print(self._message)
        self._message = ''

    def display_divider(self):
        """Prints a divider line."""
        print('='*64)

    def display_line_break(self):
        """Prints an empty line."""
        print('')

    def clear_screen(self):
        """Clears terminal screen"""
        if(sys.platform == 'windows'):
            subprocess.call('cls',shell=True)
        else:
            subprocess.call('clear',shell=True)

    def play(self):
        """The main game loop.  The game runs here."""
        self.choose_random_definition()    # Choose first definition.
        while len(list(self._words.keys())) > 0:    # Continue playing until there are no words left to guess.
            self.clear_screen()
            self.display_message()
            self.display_divider()
            self.display_definition()
            self.display_line_break()
            self.display_words()
            self.display_divider()
            guess = input('What is the word this definition describes? ') # Get input from player for word guess
            if self.check_word(guess): # Check if the players guess is valid and respond accordingly    
                self.choose_random_definition()
                self._words.pop(word, None)
        # When the program reaches this point there are no words to choose from so the round is complete.
        self.clear_screen()
        self.display_divider()
        print("Round complete! Score: "+str(self._score))
        self.display_divider()

if __name__ == '__main__':
    rarray=[0,1,2,3,4,5,6,7,8,9,10,11]
    random.shuffle(rarray)
    wordsrom=[]
    for i in range(0,11):
        wordsrom.append(rarray[i])
    print(wordsrom)
    g = Game()
    g.play()