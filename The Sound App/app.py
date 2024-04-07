#------------------------------------------------------
#   File: app.py
#
#   Description: example showing mp3 file and timer
#
#   Author: Masrur Ahmed Sami
#
#   Date: 4-06-2024
#
#   Notes: expects mp3 files in /assets dir 
#
#------------------------------------------------------

import toga
from toga.style.pack import LEFT, RIGHT, COLUMN, ROW, CENTER, TOP, BOTTOM, Pack
from kivy.core.audio import SoundLoader
import threading


# Define styles for the UI elements
displayStyle = Pack(padding=(0, 0), direction=COLUMN, alignment=CENTER, flex=1, background_color='#666666')
commandStyle = Pack(height=50, padding=(5, 5), font_size=14, font_family='sans-serif', color='#ffffff', background_color='#333333')
nameStyle = Pack(padding=(5, 5), font_size=14, color='#ffffff', background_color='#444444')

class AudioPlayerApp(toga.App):
    def startup(self):
        self.available_sounds = ['guitar', 'piano', 'violin']
        self.instrument_options = ['Guitar', 'Violin', 'Piano', 'Cello', 'Trumpet', 'Drums']
        self.current_sound_index = 0
        self.correct_guesses = 0
        self.currently_playing_sound = None  # Reference to currently playing sound object
        self.timer = None

        main_box = toga.Box(style=displayStyle)
        self.instruction_label = toga.Label('Listen to the sound and guess the instrument:', style=nameStyle)
        main_box.add(self.instruction_label)
        
        self.instrument_selector = toga.Selection(items=self.instrument_options, style=commandStyle)
        main_box.add(self.instrument_selector)
        
        self.submit_button = toga.Button('Submit Guess', on_press=self.submit_guess, style=commandStyle)
        main_box.add(self.submit_button)
        
        self.result_label = toga.Label('', style=nameStyle)
        main_box.add(self.result_label)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        self.play_sound()

    def play_sound(self):
        if self.currently_playing_sound:
            self.currently_playing_sound.stop()  # Stop the current sound if it's playing
        sound_path = f'assets/{self.available_sounds[self.current_sound_index]}.mp3'
        self.currently_playing_sound = SoundLoader.load(sound_path)
        if self.currently_playing_sound:
            self.currently_playing_sound.play()
        self.timer = threading.Timer(10, self.time_up)
        self.timer.start()

    def submit_guess(self, widget):
        if self.timer:
            self.timer.cancel()
        if self.currently_playing_sound:
            self.currently_playing_sound.stop()  # Stop the sound when the user makes a guess

        guess = self.instrument_selector.value
        correct_instrument = self.available_sounds[self.current_sound_index]

        if guess.lower() == correct_instrument.lower():
            self.correct_guesses += 1
            self.result_label.text = "Correct!"
        else:
            self.result_label.text = f"Incorrect! It was a {correct_instrument.capitalize()}."

        self.current_sound_index += 1
        if self.current_sound_index < len(self.available_sounds):
            self.play_sound()
        else:
            self.end_game()

    def time_up(self):
        if self.currently_playing_sound:
            self.currently_playing_sound.stop()  # Stop the sound when time is up
        self.submit_button.label = "Time's up! Next sound..."
        self.submit_guess(None)

    def end_game(self):
        final_message = f"Game Over! You guessed {self.correct_guesses} out of {len(self.available_sounds)} correctly."
        self.result_label.text = final_message

def main():
    return AudioPlayerApp('AudioPlayer', 'org.beeware.audioplayer')

if __name__ == '__main__':
    main().main_loop()