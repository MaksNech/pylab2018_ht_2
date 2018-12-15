import sys

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import nltk
import string
from nltk.corpus import stopwords
import collections



def tokenize(text):
    """tokenize is main tokenization function that remove punctuation
       symbols of punctuation and stop words:
    """
    tokens = nltk.word_tokenize(text)
    tokens = [i for i in tokens if (i not in string.punctuation)]
    stop_words = stopwords.words('english')
    tokens = [i for i in tokens if (i not in stop_words)]
    return tokens


def parseNouns(tokenList):
    """parseNouns is a parsing function that outputs nouns from tokens:
    """
    pos_sentences = nltk.pos_tag(tokenList)
    nouns = [word for word, pos in pos_sentences
             if (pos == 'NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS')]
    downcased = [x.lower() for x in nouns]
    return downcased


def frequencyOfRepetitions(tokenList, frequency):
    """frequencyOfRepetitions is a parsing function that outputs tokens with preset frequency:
    """
    resultList = dict(collections.Counter(tokenList))
    resultListKeys = [i for i in resultList if resultList[i] >= frequency]
    resultListValues = [resultList[i] for i in resultList if resultList[i] >= frequency]
    data = [resultListKeys, resultListValues]
    return data


def new_winBar():
    """new_winBar is a new window definition function for Bar graph:
    """
    newwinBar = tk.Toplevel(root)

    words = update_analys()[0]
    frequency = update_analys()[1]

    figure_bar = plt.Figure(figsize=(10, 5), dpi=180)
    plot_bar = figure_bar.add_subplot(111)
    plot_bar.barh(words, frequency, color='#2baf41')
    bar1 = FigureCanvasTkAgg(figure_bar, newwinBar)
    bar1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
    plot_bar.tick_params(direction='out', length=6, width=2, colors='k',
                         grid_color='g', grid_alpha=0.5, labelsize=5)
    plot_bar.set_facecolor('#f2f2f2')
    plot_bar.set_title('Bar graph "Noun repetition rate"', color='k', fontsize=9)
    plot_bar.set_xlabel('frequency', color='#f9a43b')
    plot_bar.set_ylabel('noun', color='#f9a43b')

    toolbar = NavigationToolbar2Tk(bar1, newwinBar)
    toolbar.update()
    bar1.get_tk_widget().pack()


def new_winPie():
    """new_winPie is a new window definition function for Pie graph:
    """

    newwinPie = tk.Toplevel(root)

    words = update_analys()[0]
    frequency = update_analys()[1]

    mpl.rcParams['font.size'] = 5.0

    figure_pie = plt.Figure(figsize=(10, 5), dpi=180)
    plot_pie = figure_pie.add_subplot(111)
    plot_pie.pie(frequency, labels=words, autopct='%1.1f%%', shadow=False, startangle=90)
    plot_pie.axis('equal')
    pie2 = FigureCanvasTkAgg(figure_pie, newwinPie)
    pie2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
    plot_pie.set_title('Pie graph "Noun repetition rate"', color='k', fontsize=9)

    toolbar = NavigationToolbar2Tk(pie2, newwinPie)
    toolbar.update()
    pie2.get_tk_widget().pack()


def get_input_txt():
    """get_input_txt is a function for get txt value:
    """
    input_value = text_field.get(1.0, tk.END)
    print(input_value)
    return str(input_value)


def get_input_spin():
    """get_input_spin is a function for get spin value:
        """
    input_value = spin.get()
    return int(input_value)


def update_analys():
    """update_analys is a function for updating current data for graphs generation:
       return: [[keys],[values]]
        """
    nounsList = parseNouns(tokenize(get_input_txt()))
    data = frequencyOfRepetitions(nounsList, get_input_spin())
    return data

#####################################################################
"""GUI with Tkinter 
    """
root = tk.Tk()
root.geometry('800x600')
root.resizable(width=False, height=False)
root.title('Noun frequency app')
frame_main = tk.Frame(root, bg='#303030', width=800, height=600)
frame_main.grid(row=0, column=0)
frame_txt_input = tk.Frame(frame_main, bg='#303030', width=600, height=400)
frame_txt_input.pack()

label = tk.Label(frame_txt_input, text="Enter here text for nouns analysis:", fg="White", bg="#303030")
label.pack(side=tk.TOP, anchor=tk.W, padx=10)

text_field = tk.Text(frame_txt_input, height=30, width=105)
text_field.pack(side=tk.LEFT, fill=tk.BOTH, pady=10, padx=10)
scroll = tk.Scrollbar(frame_txt_input, command=text_field.yview, orient=tk.VERTICAL)
scroll.config(command=text_field.yview)
text_field.configure(yscrollcommand=scroll.set)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

label = tk.Label(frame_main, text="Set the minimal frequency value:", fg="White", bg="#303030")
label.pack(side=tk.TOP, anchor=tk.W, padx=10)

spin = tk.Spinbox(frame_main, from_=2, to=100)
spin.pack(expand=True, side=tk.LEFT, fill="both", padx=10, pady=10)

button_bar = tk.Button(frame_main, text="Generate bar graph", width=10, height=3, bg="#9b9b9b", bd=2, fg="black",
                       command=lambda: new_winBar(),
                       font=('arial', 12))
button_bar.pack(expand=True, side=tk.LEFT, fill="both", padx=10, pady=10)
button_pie = tk.Button(frame_main, text="Generate pie graph", width=10, height=3, bg="#9b9b9b", bd=2, fg="black",
                       command=lambda: new_winPie(),
                       font=('arial', 12))
button_pie.pack(expand=True, side=tk.LEFT, fill="both", padx=10, pady=10)
#####################################################################

root.mainloop()
