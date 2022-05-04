# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 12:11:33 2022

@author: henri
"""

import streamlit as st
import random as rd
import pandas as pd


def load_colors():
    with open('colors.css') as fh:
        st.write(f"<style>{fh.read()}</style>", unsafe_allow_html=True)

@st.cache
def get_words():
    words = pd.read_csv('unigram_freq.csv')
    common_words = list(words.loc[(words['count']>=1000000)].astype(str).word.values)

    # return a Set so that searching for a specific word is faster
    # more here: https://python-reference.readthedocs.io/en/latest/docs/sets/
    english_5chars_words = {i.upper() for i in common_words if len(i) == 5}

    
    return english_5chars_words


def validate_guess(guess, answer):

    color_map = {
        'Correct': " <span class='green'>",
        'Good': " <span class='yellow'>",
        'Wrong': " <span class='grey'>"
    }

    word = "<div><h4><bold>"

    for i, char in enumerate(guess):
        if answer[i] == guess[i]:
            word += color_map['Correct'] + char

        elif char in answer:
            word += color_map['Good'] + char

        else:
            word += color_map['Wrong'] + char


    word += "</span></bold></h4></div>"

    st.write(word, unsafe_allow_html=True)

    return guess == answer



if 'solution' not in st.session_state:
    st.session_state['solution'] = rd.choice(list(get_words()))


st.title("Wordle")
load_colors()

        
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button("Give me a hint."):
    hint=list(st.session_state['solution'])

    # hint[rd.randint(0,len(st.session_state['solution'])-1)]
    # ^ why make it harder when it can be so simple?   
    st.text("Why don't you try a word with a '" + rd.choice(hint) + "' on it?")
    st.session_state.count -=1
    
if st.button("Check solution."):
    st.text("The solution is: " + st.session_state['solution'])
    st.session_state.count -=1

if st.button("New Game"):
    st.session_state['solution'] = rd.choice(list(get_words()))
    st.session_state.count = 0
    st.experimental_rerun()

if st.session_state.count<=6:
    remaining_attempts=6-st.session_state.count
    
    guess = st.text_input("Try your word", max_chars=5).upper()
    
    # Only allow 5 letter words
    if guess not in get_words() and st.session_state.count > 0:
         st.write("Not a valid word! Try again.")

    elif validate_guess(guess, st.session_state['solution']):
        st.write("<h3><bold>That is correct!</bold></h3>", unsafe_allow_html=True)
    elif remaining_attempts>0:
        st.write("You ony have "+str(remaining_attempts)+" attempts left.")
        st.session_state.count +=1
    else:
        st.write("<h3><bold>You ran out of tries!</bold></h3>", unsafe_allow_html=True)

st.text(st.session_state['solution'])
