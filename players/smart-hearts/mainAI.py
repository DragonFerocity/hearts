from performance_timer import Perf
import sys
import random
from traceback import format_exc

from brain import Brain
from grapher import Grapher
Perf('Imports')

try:
    in_string = str(sys.argv[1])
    mode = 'command'
except Exception as e:
    in_string = "1/2/3/110,214,303,207,109,414/211,202/12,0,1,4/102,105,111,103|208,203,212,103|210,209,402,207|306,305,309,302"
    mode = 'debug'

in_list = in_string.split('/')
round_num = int(in_list[0])
player = int(in_list[1])
lead_player = int(in_list[2])
hand = [int(s) for s in in_list[3].split(',')]
trick = [int(s) for s in in_list[4].split(',')]
points = {n+1:int(s) for n, s in enumerate(in_list[5].split(','))}
tricks_taken = {n+1:[int(t) for t in s.split(',')] for n, s in enumerate(in_list[6].split('|'))}

choice = random.choice(hand)

if mode == 'debug':
    import PySimpleGUI as sg
    new_theme = {"BACKGROUND": '#333333', "TEXT": '#cccccc', "INPUT": '#888888',
             "TEXT_INPUT": '#888888', "SCROLL": '#888888',
             "BUTTON": '#888888', "PROGRESS": '#888888', "BORDER": 1,
             "SLIDER_DEPTH": 1, "PROGRESS_DEPTH": 0
             }
    sg.theme_add_new('MyTheme', new_theme)
    sg.theme('MyTheme')
    layout = [
        [sg.Text(f'Round {round_num}.')],
        [sg.Text(f'Player 1: {points[1]} {tricks_taken[1]}, Player 2: {points[2]} {tricks_taken[2]}, Player 3: {points[3]} {tricks_taken[3]}, Player 4: {points[4]} {tricks_taken[4]}.')],
        [sg.Text(f'You are player {player}.')],
        [sg.Text(f'Player {lead_player} led.')],
        [sg.Text(f'The cards {trick} have been played.')],
        [sg.Text(f'You hand is {hand}.')],
        [sg.Graph((800,200), (0,0), (100,100), key='graph')]
    ]
    window = sg.Window('Smart Heart', layout=layout, grab_anywhere=True, finalize=True)
    Grapher.brain(window['graph'], Brain.load(693))
    while True:
        event, values = window.read(timeout=1)
        if event == sg.WIN_CLOSED:
            break
    window.close()

print(choice)
Perf('End')