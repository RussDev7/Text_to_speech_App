import tkinter
import customtkinter
from functions import select_file, download_converted_file

# Set up Tkinter GUI window
# Using customtkinter module to customize appearance
customtkinter.set_appearance_mode("dark")  # Setting dark mode appearance
customtkinter.set_default_color_theme("blue")  # Setting default color theme to blue
window = customtkinter.CTk()  # Creating a custom Tkinter window
window.title("PDF to Speech Converter")  # Setting window title
window.geometry("600x300")  # Setting window size
window.config(padx=50, pady=50)  # Adding padding to the window

# Label
# Creating a label to display file selection status
text = customtkinter.CTkLabel(master=window, text="File selected:\nnone", width=280, height=100,
fg_color=("white", "#2e2e2e"), corner_radius=8, text_font=('Arial', 18))
text.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)  # Placing label in the window

# Buttons
# Creating buttons for uploading PDF file and converting it to MP3
upload_button = customtkinter.CTkButton(master=window, text="Upload PDF file", width=200,
                                        command=lambda: select_file(text))  # Command to execute file selection
upload_button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)  # Placing upload button

convert_button = customtkinter.CTkButton(master=window, text="Convert to MP3 and download", width=200,
                                         command=lambda: download_converted_file(text))  # Command to convert and download
convert_button.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)  # Placing convert button

window.mainloop()  # Running the main loop for the window