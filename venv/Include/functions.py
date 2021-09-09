import speech_recognition as speechrec
import sounddevice as sounddev
import soundfile as soundf
import os
import wavio
import time
import datetime
import webbrowser
from gtts import gTTS
from pygame import mixer
from mutagen.mp3 import MP3
from fuzzywuzzy import fuzz
import pyperclip
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb


lib = {
    "start": ('скажи','расскажи','покажи','сколько', 'назови', 'открой', 'какой', 'открыть', 'найти',
              'say', 'tell', 'show', 'how', 'open', 'what', 'find'),
    "cmds": {
        "time": ('текущее время', 'сейчас времени', 'который час', 'время',
                 'time'),
        "dateweek": ('день недели',
                     'day of week'),
        "date": ('дата', 'какой сегодня день', 'день',
                 'data', 'day', 'today'),
        "selfinput": ('скопировать текст', 'ввод текста', 'текст',
                      'copy', 'text', 'input text'),
        "browser": ('сайт',
                    'site')
    }
}


def recording_1():
    fs = 44100
    seconds = 10
    inputsound = 'input.wav'
    myrecording = sounddev.rec(int(seconds * fs), samplerate=fs, channels=2)
    sounddev.wait()
    wavio.write(inputsound, myrecording, fs, sampwidth=2)
    index = 0
    speech_to_text(inputsound, index)


def recording_2(index):
    def apply():
        try:
            seconds = int(duration.get())
            children.destroy()
            fs = 44100
            inputsound = 'voice.wav'
            myrecording = sounddev.rec(int(seconds * fs), samplerate=fs, channels=2)
            sounddev.wait()
            wavio.write(inputsound, myrecording, fs, sampwidth=2)
            if flag.get() == 0:
                index = 1
            else:
                index = 2
            speech_to_text(inputsound, index)
        except:
            mb.showerror('Ошибка', 'Некорректный ввод!')

    children = Tk()
    children.title("Запись")
    children.geometry('400x400+450+140')
    children.resizable(False, False)
    title = tk.Label(children, text="Введите продолжительность записи:")
    title.grid(row=0, column=0, sticky="w")
    duration = StringVar()
    duration = tk.Entry(children, textvariable=duration)
    duration.grid(row=0, column=1, padx=5, pady=5)
    flag = BooleanVar()
    flag.set(0)
    choose = tk.LabelFrame(children, text='Выбор языка')
    choose.grid(row=1, column=0, pady=5, padx=5)
    f1 = tk.Radiobutton(choose, text='Русский', variable=flag, value=0)
    f1.grid(row=0, column=0, pady=5, padx=5 )
    f2 = tk.Radiobutton(choose, text='Английский', variable=flag, value=1)
    f2.grid(row=1, column=0, pady=5, padx=5)
    apply_b = tk.Button(children, text="Ок", command=apply)
    apply_b.grid(row=4, column=0, padx=5, pady=5)
    children.mainloop()


def recording_3():
    fs = 44100
    seconds = 10
    inputsound = 'input.wav'
    myrecording = sounddev.rec(int(seconds * fs), samplerate=fs, channels=2)
    sounddev.wait()
    wavio.write(inputsound, myrecording, fs, sampwidth=2)
    index = 3
    speech_to_text(inputsound, index)


def deleting(filename):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
    os.remove(path)


def speech_to_text(audio, index):
    r = speechrec.Recognizer()
    with speechrec.AudioFile(audio) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    type(audio)

    try:
        if (index == 2):
            cmd = r.recognize_google(audio).lower()
        else:
            cmd = r.recognize_google(audio, language="ru-RU").lower()
        if (index == 0):
            if cmd.startswith(lib["start"]):
                for x in lib['start']:
                    cmd = cmd.replace(x, "").strip()

            cmd = cmd_recognize(cmd)

            cmd_execute(cmd['cmd'])
        else:
            if (index == 1 or index == 2):
                def close():
                    children.destroy()
                    deleting("input.wav")

                children = Tk()
                children.title("Вы сказали:")
                children.resizable(False, False)
                children.geometry('400x400+450+140')
                output = tk.Label(children, text=cmd, width=200, height=10)
                output.pack()
                pyperclip.copy(cmd)
                pyperclip.paste()
                tk.Button(children, text="Ок", command=close).pack() #.grid(row=1, column=0, padx=5, pady=5)
                children.mainloop()
                deleting(voice.wav)
            else:
                if (index == 3):
                    browser_cmd(cmd)

    except speechrec.UnknownValueError:
        mb.showerror("Ошибка", "Не удалось распознать речь.")
    except speechrec.RequestError as e:
        mb.showerror("Ошибка", "Проверьте соединение с интернетом; {0}".format(e))


def cmd_recognize(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in lib['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


def cmd_execute(cmd):
    if cmd == 'time':
        time_cmd()

    elif cmd == 'date':
        date_cmd()

    elif cmd == 'dateweek':
        dateweek_cmd()

    elif cmd == 'selfinput':
        recording_2(1)

    elif cmd == 'browser':
        text_to_speech('Что вы хотите найти?')
        recording_3()


def text_to_speech(response):
    tts = gTTS(response, lang='ru')
    tts.save("response.mp3")
    responding()


def responding():
    sound = MP3("response.mp3")
    mixer.init()
    mixer.music.load("response.mp3")
    mixer.music.play()
    time.sleep(sound.info.length + 1)
    mixer.music.stop()
    mixer.quit()
    time.sleep(10)
    deleting("response.mp3")
    deleting("input.wav")


def time_cmd():
    now = datetime.datetime.now()
    text_to_speech("Сейчас " + str(now.hour) + ":" + str(now.minute))


def date_cmd():
    today = datetime.datetime.now()
    text_to_speech("Сегодня " + str(today.day) + "." + str(today.month) + "." + str(today.year))


def dateweek_cmd():
    days= ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    today = datetime.date.weekday(datetime.datetime.now())
    text_to_speech("Сегодня " + days[today])


def repeat_cmd():
    filename = 'input.wav'
    if (os.path.exists(filename)):
        data, fs = soundf.read(filename, dtype='float32')
        sounddev.play(data, fs)
        sounddev.wait()
        deleting(filename)
    else:
        mb.showerror("Ошибка", "Вы не выполняли ввод.")


def browser_cmd(find):
    webbrowser.open_new_tab('https://yandex.ru/search/?text=' + str(find))
    deleting("input.wav")