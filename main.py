from math import floor

import simpleaudio
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from kivymd.app import MDApp



PALE = get_color_from_hex('ebd8b7')
BLUE = get_color_from_hex('99bbad')
MAUVE = get_color_from_hex('c6a9a3')
LILAC = get_color_from_hex('9a8194')


# globals

session_length = 0
phases = 0
ticks = 0
total_phases = 0
text_string = '00:00'
event = None
count = 0



Builder.load_file('meditation.kv')

class MeditationScreen(Widget):


    def reset_timer(self):

        global session_length
        global phases
        global ticks
        global total_phases
        global event

        session_length = 0
        phases = 0
        ticks = 0
        total_phases = 0
        Clock.unschedule(event)
        play_sound(end_bell)


    # Selection
    def get_selection(self, instance, value, time):
        global session_length
        global phases
        global ticks
        global total_phases

        session_length = int(time)
        print(f"Session length {session_length}")

        if session_length < 30:
            phases = int(session_length / 5)
            ticks = 300
        else:
            phases = int(session_length / 10)
            ticks = 600
        phases += 1
        total_phases = phases

    def start_timer(self):

        global phases
        global total_phases
        global ticks
        global session_length
        global count
        global event
        if session_length == 0:
            return
        if event:
            event.cancel() # Stop any ongoing event
        if phases == total_phases:
            if event:
                event.cancel()  # Stop any ongoing event
            count = 10
            event = Clock.schedule_interval(self.count_down, 1)
        elif phases == total_phases - 1:
            if event:
                event.cancel()  # Stop any ongoing event
            play_sound(beginning_bell)
            count = ticks
            event = Clock.schedule_interval(self.count_down, 1)
        elif phases == 0:
            play_sound(end_bell)
            if event:
                event.cancel()  # Stop any ongoing event
        else:
            play_sound(phase_bell)
            if event:
                event.cancel()  # Stop any ongoing event
            count = ticks
            event = Clock.schedule_interval(self.count_down, 1)



    def print_time(self):
        global text_string
        global count
        minutes = floor(count / 60)
        seconds = count % 60

        if seconds < 10:
            seconds = f"0{seconds}"
        count_text = f"{minutes}:{seconds}"

        print(count_text)
        self.ids.timer_label.text = count_text


    def count_down(self, dt):

        global phases
        global count
        self.print_time()
        if count > 0:
            count -= 1
        else:       # When count gets to zero, decrement phases and restart timer
            phases -= 1
            self.start_timer()





class MeditationApp(MDApp):
    # Pass colours to .kv file
    pale = ObjectProperty(PALE)
    blue = ObjectProperty(BLUE)
    mauve = ObjectProperty(MAUVE)
    lilac = ObjectProperty(LILAC)
    global text_string

    def change_label_text(self):
        global text_string
        return text_string


    def build(self):
        # Window.clearcolor = PALE
        return MeditationScreen()



# Sounds
def play_sound(sound):
    sound.play()


beginning_bell = simpleaudio.WaveObject.from_wave_file("beginning_meditation_bell.wav")
phase_bell = simpleaudio.WaveObject.from_wave_file("phase_meditation_bell.wav")
end_bell = simpleaudio.WaveObject.from_wave_file("end_meditation_bell.wav")



if __name__ == '__main__':
    MeditationApp().run()
