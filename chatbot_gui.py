import api_bot
import tkinter.scrolledtext as tks #creates a scrollable text window

from datetime import datetime
from tkinter import *
import string
import nltk
import requests

from googlesearch import search
from lxml import html
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

# helper function to generate text corpus from html elements
def generate_corpus(all_p_elements):
    corpus = ""
    for p_element in all_p_elements:
        corpus += '\n' + ''.join(p_element.findAll(text = True))
    return corpus


def get_bot_response1(user_input):
    # default bot response
    bot_response = "I'm sorry, I don't think I can help you with that :("
    try:
        # use the google search api to fetch top 3 search results
        google_search_results = list(search(user_input, stop=3, pause=1))
        
        # use the requests api to fetch the top result webpage
        webpage = requests.get(google_search_results[0])
        webpage_tree = html.fromstring(webpage.content)
        webpage_soup = BeautifulSoup(webpage.content, "lxml")
        
        # extract all <p> elements from webpage soup object
        all_p_list = webpage_soup.findAll('p')
        
        # generate corpus from all <p> elements
        google_search_corpus = generate_corpus(all_p_list)

    except:
      # return the default response if corpus is empty
      if len(google_search_corpus) == 0:
        return bot_response
        
def create_and_insert_user_frame(user_input):
  userFrame = Frame(chatWindow, bg="#d0ffff")
  Label(
      userFrame,
      text=user_input,
      font=("Arial", 11),
      bg="#d0ffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
  Label(
      userFrame,
      text=datetime.now().strftime("%H:%M"),
      font=("Arial", 7),
      bg="#d0ffff"
  ).grid(row=1, column=0, sticky="w")

  chatWindow.insert('end', '\n ', 'tag-right')
  chatWindow.window_create('end', window=userFrame)


def create_and_insert_bot_frame(bot_response):
  botFrame = Frame(chatWindow, bg="#ffffd0")
  Label(
      botFrame,
      text=bot_response,
      font=("Arial", 11),
      bg="#ffffd0",
      wraplength=400,
      justify='left'
  ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
  Label(
      botFrame,
      text=datetime.now().strftime("%H:%M"),
      font=("Arial", 7),
      bg="#ffffd0"
  ).grid(row=1, column=0, sticky="w")

  chatWindow.insert('end', '\n ', 'tag-left')
  chatWindow.window_create('end', window=botFrame)
  chatWindow.insert(END, "\n\n" + "")


def send(event):
    chatWindow.config(state=NORMAL)

    user_input = userEntryBox.get("1.0",'end-2c')
    create_and_insert_user_frame(user_input)

    bot_response = api_bot.get_bot_response(user_input)
    create_and_insert_bot_frame(bot_response)

    chatWindow.config(state=DISABLED)
    userEntryBox.delete("1.0","end")
    chatWindow.see('end')


baseWindow = Tk()
baseWindow.title("The Google Search Bot")
baseWindow.geometry("500x250")

chatWindow = tks.ScrolledText(baseWindow, font="Arial")
chatWindow.tag_configure('tag-left', justify='left')
chatWindow.tag_configure('tag-right', justify='right')
chatWindow.config(state=DISABLED)

sendButton = Button(
    baseWindow,
    font=("Verdana", 12, 'bold'),
    text="Send",
    bg="#fd94b4",
    activebackground="#ff467e",
    fg='#ffffff',
    command=send)
sendButton.bind("<Button-1>", send)
baseWindow.bind('<Return>', send)

#text box for user entry
userEntryBox = Text(baseWindow, bd=1, bg="white", width=38, font="Arial")

chatWindow.place(x=1, y=1, height=200, width=500)
userEntryBox.place(x=3, y=202, height=27)
sendButton.place(x=430, y=200)

baseWindow.mainloop()    
