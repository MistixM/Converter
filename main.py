import customtkinter # Import ui library
import os, threading, random # Multithreading and other important variables

from tkinter import filedialog as fd # Special dialog window that should ask user file

def main():
    app_v = 1.0 # Current software version

    print("Application started well! Current version:", app_v)

    # Set properties ui and start ui loop
    app = customtkinter.CTk()   
    app.geometry("400x500")
    app.minsize(400, 500)
    app.maxsize(629, 550)

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")
    app.resizable(True, True)
    app.title("Converter")

    # None values. Will used in future
    normalised_path = None
    choose_file_format_box = None
    combobox_in = None

    # Converter available formats
    audio_format = ['MP3', 'WAV', 'AAC', 'FLAC', 'OGG', 'WMA', 'AIFF']
    video_format = ['MP4', 'AVI', 'MKV', 'MOV', 'FLV', 'WebM', 'MPEG', 'WMV']
    format = ["Video", "Audio"]

    # Random phrases used when converting files
    random_info_phrases = ["Loading..", "Process..", "In process", "Converting..", "Stand by.."]
    
    # Function convert audio. Using ffmpeg.exe file to start convert to the requested format
    def convert_audio():
        # Set global path to manipulate with him in future
        global normalised_path

        # Locate ffmpeg.exe file
        util_path = f"{os.getcwd()}/ffmpeg/bin/ffmpeg.exe"
        
        # Check if ffmpeg.exe exists
        if os.path.isfile(util_path):
            ''' 
                Then, we check that normalised_path exists, combobox_in value is not equal to 
                combobox_from, and normalised_path is not None 
            '''
            if normalised_path and combobox_in.get() != combobox_from.get() and normalised_path != '.':
                '''
                    If the condition above is true, we save the specified directory 
                    to addition value using 'os' library.
                ''' 
                output_dir = os.path.dirname(normalised_path)
                final_output = os.path.join(output_dir, os.path.basename(normalised_path).replace(" ", "_").rsplit('.', 1)[0] + '.' + combobox_in.get().lower())
                # With try start the conversion and disable any buttons that may break the script
                try:
                    button_convert.configure(state="disabled")
                    choose_file.configure(state="disabled")

                    os.system(util_path + ' -i "' + normalised_path + '" "' + final_output + '"')
                    information_text.configure(text="Conversion successful!")

                    # After successful conversion set buttons to normal state
                    button_convert.configure(state="normal")
                    choose_file.configure(state="normal")

                # Catch any errors and send error message
                except:
                    information_text.configure(text="Conversion error!")
            # Catch user issue if inputs are incorrect
            else:
                information_text.configure(text="Operation failed! Please, check your file and inputs!")
        # Catch and send error message if ffmpeg file does not exist
        else:
            information_text.configure(text="Current library not found. Please, install library")
    
    # Function that's responsible for convert button action
    def on_convert_clicked():
        # Set global path to manipulate with him as before
        global normalised_path

        # Check again that the inputs are correct
        try:
            if normalised_path and combobox_in.get() != combobox_from.get() and normalised_path != '.' and os.path.splitext(os.path.basename(normalised_path))[1].replace(".", "").upper() == combobox_from.get():
                # If all correct, start multithreading (conversion) and send information to user with random phrases
                information_text.configure(text=random.choice(random_info_phrases))
                threading.Thread(target=convert_audio).start()
            # If inputs are incorrect, send error message to user
            else:
                information_text.configure(text="Unknown error! Please, re-check your file and file path!")
        # Catch NameError error and send error message to user
        except NameError:
            information_text.configure(text="Operation failed! Please, check your file and file path.")
    
    # Function that's responsible for choose button action
    def on_choose():
        # Set global path to manipulate with him as before
        global normalised_path

        # Ask user file path that should be converted
        normalised_path = os.path.normpath(fd.askopenfilename())
        
        # Check if normalised_path is correct and if it is send success message to user
        if normalised_path != '.':
            information_text.configure(text=f"The {os.path.basename(normalised_path)} has been imported.")
        # If the user has not selected the file, send the error message 
        else:
            information_text.configure(text="The file has not been selected. Please, select the file!")

    # Function that's responsible for checking format state. In other words, just check what the user wants to convert
    def check_format_state(*args, **kwargs):
        # Get selected format using get() method
        selected_format = choose_file_format_box.get()

        # If user wants to convert Video, just change other formats to video formats
        if selected_format == "Video":
            combobox_from.configure(values=video_format)
            combobox_in.configure(values=video_format)
            combobox_from.set(video_format[0])
            combobox_in.set(video_format[3])
        # Elif user wants to convert Audio, just change other formats to audio formats
        elif selected_format == "Audio":
            combobox_from.configure(values=audio_format)
            combobox_in.configure(values=audio_format)
            combobox_from.set(audio_format[0])
            combobox_in.set(audio_format[1])

    # Gui variables 
    font_title = customtkinter.CTkFont(family='Gilroy-Semibold', size=20)
    font_text = customtkinter.CTkFont(family='Gilroy-Semibold', size=15)

    # Also, we using values attribute, to set default value combobox. No highlighting (just set state to 'readonly')
    combobox_from = customtkinter.CTkComboBox(app, width=70, height=20, values=audio_format, state="readonly", font=font_text)
    combobox_from.place(relx=.4, rely=.4, anchor=customtkinter.N)
    combobox_from.set("MP3") # Set default value

    # Labels with pointed fonts
    title_label = customtkinter.CTkLabel(app, text="Converter", font=font_title)
    title_label.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

    from_label = customtkinter.CTkLabel(app, text="From", font=font_text)
    from_label.place(relx=.39, rely=.35, anchor=customtkinter.CENTER)

    in_label = customtkinter.CTkLabel(app, text="In", font=font_text)
    in_label.place(relx=.59, rely=.35, anchor=customtkinter.CENTER)

    # Here also use values attribute, to set default value combobox
    combobox_in = customtkinter.CTkComboBox(app, width=70, height=20, values=audio_format, state="readonly", font=font_text)
    combobox_in.place(relx=.6, rely=.426, anchor=customtkinter.CENTER)
    combobox_in.set("WAV") # Set default value

    choose_file_format_box = customtkinter.CTkComboBox(app, width=190, height=20, values=format, state="readonly", command=check_format_state, font=font_text)
    choose_file_format_box.place(relx=.5, rely=.49, anchor=customtkinter.CENTER)
    choose_file_format_box.set("Audio")

    # Create Choose File button with command specified function
    choose_file = customtkinter.CTkButton(app, width=190, text="Choose file", command=on_choose, font=font_text)
    choose_file.place(relx=.5, rely=.56, anchor=customtkinter.CENTER)

    # Create Convert button with command specified function
    button_convert = customtkinter.CTkButton(app, width=190, text="Convert", command=on_convert_clicked, font=font_text)
    button_convert.place(relx=.5, rely=.63,anchor=customtkinter.CENTER)

    # This is information text that is used to inform the user
    information_text = customtkinter.CTkLabel(app, text=None, font=font_text)
    information_text.place(relx=.5, rely=.9, anchor=customtkinter.CENTER)

    # Software version text
    version_info = customtkinter.CTkLabel(app, text=app_v, font=font_text, text_color="grey")
    version_info.place(relx=.98, rely= .93, anchor=customtkinter.NE)

    # End UI drawing
    app.mainloop()

if __name__ == "__main__":
    main()
