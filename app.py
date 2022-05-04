from random import choice
import random
from termcolor import colored
import pandas as pd
import streamlit as st
import sys
from streamlit import caching
import time

st.title('Wordle')

new_game = st.button('START A NEW GAME')
if new_game:
    st.success('REFRESH THE PAGE TO START THE NEW GAME')
    st.legacy_caching.caching.clear_cache()
    st.stop()

@st.cache()
def find_target():
    words = pd.read_csv('unigram_freq.csv')
    common_words = list(words.loc[(words['count'] >= 1000000)].astype(str).word.values)
    english_5chars_words = [i.upper() for i in common_words if len(i) == 5]
    return english_5chars_words, choice(english_5chars_words)

TILES = {
    'correct_place': '🟩',
    'correct_letter': '🟨',
    'incorrect': '⬛'
}


def validate_guess(guess, answer):
    guessed = []
    tile_pattern = []
    # Loop through every letter of the guess
    for i, letter in enumerate(guess):
        # If the letter is in the correct spot, color it in green and add the green tile
        if answer[i] == guess[i]:
            # guessed += colored(letter, 'green')
            guessed += letter
            tile_pattern.append(TILES['correct_place'])
            # Replace the existing letter in the answer with -
            answer = answer.replace(letter, '-', 1)
        # whereas if the letter is in the correct spot, color it in yellow and add the yellow tile
        elif letter in answer:
            # guessed += colored(letter, 'yellow')
            guessed += letter
            tile_pattern.append(TILES['correct_letter'])
            # Replace the existing letter in the answer with -
            answer = answer.replace(letter, '-', 1)
        # Otherwise, the letter doens't exist, just add the grey tile
        else:
            guessed += letter
            tile_pattern.append(TILES['incorrect'])
    
    # Return the joined colored letters and tiles pattern
    return ''.join(guessed), ''.join(tile_pattern)


ALLOWED_GUESSES = 6


def wordle_game(target, words):

    GAME_ENDED = False

    # Init Session State to store the results as streamlit keep executing the script from top to bottom
    if 'history_guesses' not in st.session_state:
        st.session_state.history_guesses = []
    if 'tiles_patterns' not in st.session_state:
        st.session_state.tiles_patterns = []
    if 'colored_guessed' not in st.session_state:
        st.session_state.colored_guessed = []

    # Keep playing until the user runs out of tries or finds the word
    i = 1
    guess = st.text_input('Type your guess!', placeholder='type here', max_chars=5).upper()
    while not GAME_ENDED:
        # Check the user's guess
        if len(guess) != 5:
            st.warning("Please enter a 5-letter word")
            st.stop()
        elif guess in st.session_state.history_guesses:
            st.warning("You've already guessed this word!!")
            st.stop()
        elif guess not in words:
            st.warning('This word does not exist!')
            st.stop()
        
        # Append the valid guess
        st.session_state.history_guesses.append(guess)
        # Validate the guess
        guessed, pattern = validate_guess(guess, target)
        # Append the results
        st.session_state.colored_guessed.append(guessed)
        st.session_state.tiles_patterns.append(pattern)

        lcol, rcol = st.columns(2)
        # For each result (also the previous ones), it'll print the colored guesses and the tile pattern
        for g, p in zip(st.session_state.colored_guessed, st.session_state.tiles_patterns):
            lcol.write(f"Attempt: {g}")
            rcol.write(f"Result: {p}")
            # st.write(g, end=' ')
            # st.write(p)
        st.write()
        
        # If the guess is the target or if the user ran out of tries, end the game
        if guess == target or len(st.session_state.history_guesses) == ALLOWED_GUESSES:
            GAME_ENDED = True
        i += 1

    
    # st.write the results
    if len(st.session_state.history_guesses) == ALLOWED_GUESSES and guess != target:
        st.snow()
        st.write("\nDANG IT! YOU RAN OUT OF TRIES. THE CORRECT WORD WAS --> {}".format(target))
    else:
        st.balloons()
        st.write("\nGOOD JOB, YOU NAILED IT IN {}/{} TRIES\n".format(len(st.session_state.history_guesses),
                                                                  ALLOWED_GUESSES))

words, target_word = find_target()
st.write('WELCOME TO WORDLE...TIME TO GUESS, YOU HAVE {} TRIES\n!'.format(ALLOWED_GUESSES))
wordle_game(target_word, words)
