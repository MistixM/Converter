import tkinter, customtkinter
import os
import time
import threading
import random

from tkinter import filedialog as fd
from tkinterdnd2 import DND_ALL, TkinterDnD

class Tk(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

def root():
    app_v = 1.0

    print("Application started well! Current version:", app_v)

    app = Tk()
    app.geometry("600x500")
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    app.resizable(False, False)
    app.title("Converter")
    
    normalised_path = None
    choose_file_format_box = None
    combobox_in = None

    audio_format = ['MP3', 'WAV', 'AAC', 'FLAC', 'OGG', 'WMA', 'AIFF']
    video_format = ['MP4', 'AVI', 'MKV', 'MOV', 'FLV', 'WebM', 'MPEG', 'WMV']
    format = ["Video", "Audio"]
    random_info_phrases = ["Loading..", "Process..", "In process", "Converting..", "Stand by.."]
    '''
        Main program functions
    '''
    def convert_audio():
        global normalised_path

        util_path = "C:/ffmpeg/bin/ffmpeg.exe"
        
        if os.path.isfile(util_path):
            if normalised_path and combobox_in.get() != combobox_from.get() and normalised_path != '.':
                output_dir = os.path.dirname(normalised_path)
                final_output = os.path.join(output_dir, os.path.basename(normalised_path).replace(" ", "_").rsplit('.', 1)[0] + '.' + combobox_in.get().lower())
                try:
                    button_convert.configure(state="disabled")
                    choose_file.configure(state="disabled")

                    os.system(util_path + ' -i "' + normalised_path + '" "' + final_output + '"')
                    information_text.configure(text="Conversion successful!")

                    button_convert.configure(state="normal")
                    choose_file.configure(state="normal")
                except:
                    information_text.configure(text="Conversion error!")
            else:
                information_text.configure(text="Operation failed! Please, check your file and file path.")
        else:
            information_text.configure(text="Current library not found. Please, install library")
    '''
        Buttons actions
    '''
    def OnConvertClicked():
        global normalised_path
        try:
            if normalised_path and combobox_in.get() != combobox_from.get() and normalised_path != '.' and os.path.splitext(os.path.basename(normalised_path))[1].replace(".", "").upper() == combobox_from.get():
                information_text.configure(text=random.choice(random_info_phrases))
                threading.Thread(target=convert_audio).start()
            else:
                information_text.configure(text="Unknown error! Please, re-check your file and file path!")
        except NameError:
            information_text.configure(text="Operation failed! Please, check your file and file path.")
    def OnChoose():
        global normalised_path
        normalised_path = os.path.normpath(fd.askopenfilename())
        
        if normalised_path != '.':
            information_text.configure(text=f"The {os.path.basename(normalised_path)} has been imported.")
        else:
            information_text.configure(text="The file has not been selected. Please, select the file!")

    def check_format_state(*args):
        selected_format = choose_file = choose_file_format_box.get()
        if selected_format == "Video":
            combobox_from.configure(values=video_format)
            combobox_in.configure(values=video_format)
            combobox_from.set(video_format[0])
            combobox_in.set(video_format[3])
        elif selected_format == "Audio":
            combobox_from.configure(values=audio_format)
            combobox_in.configure(values=audio_format)
            combobox_from.set(audio_format[0])
            combobox_in.set(audio_format[1])
    '''
        GUI code
    '''
    font_title = customtkinter.CTkFont(family='Gilroy-Semibold', size=20)
    font_text = customtkinter.CTkFont(family='Gilroy-Semibold', size=15)

    combobox_from = customtkinter.CTkComboBox(app, width=70, height=20, values=audio_format, state="readonly", font=font_text)
    combobox_from.place(relx=.4, rely=.4, anchor=customtkinter.N)
    combobox_from.set("MP3")

    title_label = customtkinter.CTkLabel(app, text="Converter", font=font_title)
    title_label.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

    from_label = customtkinter.CTkLabel(app, text="From", font=font_text)
    from_label.place(relx=.39, rely=.35, anchor=customtkinter.CENTER)

    in_label = customtkinter.CTkLabel(app, text="In", font=font_text)
    in_label.place(relx=.59, rely=.35, anchor=customtkinter.CENTER)

    combobox_in = customtkinter.CTkComboBox(app, width=70, height=20, values=audio_format, state="readonly", font=font_text)
    combobox_in.place(relx=.6, rely=.426, anchor=customtkinter.CENTER)
    combobox_in.set("WAV")


    choose_file_format_box = customtkinter.CTkComboBox(app, width=190, height=20, values=format, state="readonly", command=check_format_state, font=font_text)
    choose_file_format_box.place(relx=.5, rely=.49, anchor=customtkinter.CENTER)
    choose_file_format_box.set("Audio")

    choose_file = customtkinter.CTkButton(app, width=190, text="Choose file", command=OnChoose, font=font_text)
    choose_file.place(relx=.5, rely=.56, anchor=customtkinter.CENTER)

    button_convert = customtkinter.CTkButton(app, width=190, text="Convert", command=OnConvertClicked, font=font_text)
    button_convert.place(relx=.5, rely=.63,anchor=customtkinter.CENTER)

    information_text = customtkinter.CTkLabel(app, text=None, font=font_text)
    information_text.place(relx=.5, rely=.9, anchor=customtkinter.CENTER)

    version_info = customtkinter.CTkLabel(app, text=app_v, font=font_text, text_color="grey")
    version_info.place(relx=.98, rely= .93, anchor=customtkinter.NE)
    '''
        Start GUI Window
    '''
    app.mainloop()

if __name__ == "__main__":
    root()
