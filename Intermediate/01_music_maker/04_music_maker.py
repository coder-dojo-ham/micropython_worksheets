# Experiments with micro:bit music

from microbit import *
import music

NOTES = ['c3',  'c#3', 'd3',  'd#3', 
         'e3',  'f3',  'f#3', 'g3',
         'g#3', 'a3',  'a#3', 'b3', 
         'c4',  'c#4', 'd4',  'd#4', 
         'e4',  'f4',  'f#4', 'g4',
         'g#4', 'a4',  'a#4', 'b4', 
         'c5',  'c#5', 'd5',  'd#5', 
         'e5',  'f5',  'f#5', 'g5',
         'g#5', 'a5',  'a#5', 'b5']

CHORD_INTERVALS = {'major': [0, 4, 7, 4],
                   'minor': [0, 3, 7, 3]}


def play_arpeggio(root_note_index, chord='major'):
    for interval in CHORD_INTERVALS[chord]:
        music.play(NOTES[root_note_index + interval])


# Main program

display.scroll("Tilt to play music", 75)

root = NOTES.index('c4')
music.set_tempo(bpm=210)

while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    if x < 0:
        if y > 0:
            # "Front left down" plays I chord
            display.show(Image.ARROW_SW)
            play_arpeggio(root, 'major')
        else:
            # "Back left down" plays V chord
            display.show(Image.ARROW_NW)
            play_arpeggio(root + 7, 'major')
    else:
        if y < 0:
            # "Back right down" plays vi chord
            display.show(Image.ARROW_NE)
            play_arpeggio(root + 9, 'minor')
        else:
            # "Front right down" plays IV chord
            display.show(Image.ARROW_SE)
            play_arpeggio(root + 5, 'major')