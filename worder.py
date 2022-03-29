#!/usr/bin/env python3

# Copyright (c) 2022 Jean-Rémy Falleri

import curses
import random
import time
import argparse

parser = argparse.ArgumentParser(description='options of worder.')
parser.add_argument('--lang', help = 'language used for the word database', choices=['en', 'fr'], default = 'en')
args = parser.parse_args()

database = 'words-' + args.lang
words = open(database).read().splitlines()
word = list(random.choice(words))
words = set(words)
size = len(word)
history = []
candidate = []

def main(screen):
    curses.use_default_colors()
    curses.curs_set(0)
    screen.clear()
    curses.init_pair(1, -1, 7)
    curses.init_pair(2, -1, curses.COLOR_RED)
    curses.init_pair(3, -1,  curses.COLOR_YELLOW)
    draw_grid(screen)
    ask(screen)

def current_round_line():
    return round_line(len(history) + 1)

def round_line(round):
    return round * 2

def draw_grid(screen):
    for round in range(1, 7):
        screen.addstr(round_line(round) - 1, 1, '+-' * size + '+', curses.A_BOLD)
        screen.addstr(round_line(round), 1, '| ' * size + '|', curses.A_BOLD)
        if round == 6:
            screen.addstr(round_line(round) + 1, 1, '+-' * size + '+', curses.A_BOLD)
    screen.refresh()

def clear_status(screen):
    for i in range(1, 30):
        screen.delch(15, 1)
    screen.refresh()
    
def ask(screen):
    while True:
        letter = screen.getch()
        clear_status(screen)
        if letter == 10:
            if len(candidate) == len(word):
                if ''.join(candidate) in words:
                    validate_round(screen)
                else:
                    screen.addstr(15, 1, "Word not in dictionnary.")
        elif letter == 127:
            if len(candidate) > 0:
                candidate.pop()
                screen.addstr(current_round_line(), (len(candidate) + 1) * 2, ' ')
        elif len(candidate) < size:
            candidate.append(chr(letter))
            screen.addstr(current_round_line(), len(candidate) * 2, chr(letter), curses.A_BOLD)
        screen.refresh()

def validate_round(screen):
    for i in range(0, len(candidate)):
        time.sleep(0.3)
        color = 1
        if candidate[i] == word[i]:
            color = 2
        elif candidate[0:i + 1].count(candidate[i]) + well_placed(candidate[i]) <= word.count(candidate[i]):
            color = 3
        screen.addstr(current_round_line(), (i + 1) * 2, candidate[i], curses.color_pair(color) | curses.A_BOLD)
        screen.refresh()
    history.append(candidate)
    if same():
        end_game(screen, True)
    elif len(history) == 6:
        end_game(screen, False)
    candidate.clear()
    ask(screen)

def same():
    for i in range(0, size):
        if candidate[i] != word[i]:
            return False
    
    return True

def well_placed(letter):
    total = 0
    for i in range(0, size):
        if candidate[i] == letter and candidate[i] == word[i]:
            total += 1
    
    return total

def end_game(screen, won):
    if won:
        screen.addstr(15, 1, 'Congratulation, you won!')
    else:
        screen.addstr(15, 1, 'Sorry, you lost. The solution was:')
        screen.addstr(16, 1, ''.join(word), curses.A_BOLD)
    letter = screen.getch()
    exit()

curses.wrapper(main)