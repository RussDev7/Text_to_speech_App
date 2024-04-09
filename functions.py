from tkinter import filedialog
import pyttsx3
from PyPDF2 import PdfReader
import os
import re
import threading

def select_file(text):
    """Opens filedialog and uploads selected PDF file"""
    # This function opens a file dialog window allowing the user to select a PDF file.
    # It then sets global variables for the selected PDF file and its name without filetype.
    
    global pdf_file, name_without_filetype
    
    # Load file dialog
    filetypes = (("PDF files", '.pdf'), ("all files", "*.*"))
    current_dir = os.getcwd()
    pdf_folder_path = os.path.join(current_dir, 'PDF')
    
    # Create 'PDF' folder if it doesn't exist
    if not os.path.exists(pdf_folder_path):
        os.makedirs(pdf_folder_path)
        
    # Ask user to select a file
    pdf_file = filedialog.askopenfilename(title="Select a file", initialdir=pdf_folder_path, filetypes=filetypes)
    
    # Gets name of the selected file
    name_with_filetype = os.path.basename(pdf_file)
    name_without_filetype = os.path.splitext(name_with_filetype)[0]
    
    # Shows name of the selected file on screen
    text.configure(text=f"File selected:\n{name_with_filetype}", text_color="white")

def run_pyttsx3():
    """Converts string to mp3 file and saves it to downloads folder"""
    # This function initializes pyttsx3 engine, converts the extracted text to speech,
    # saves it as an mp3 file in the 'MP3' folder.
    
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # Set speech rate
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Set the voice
    
    current_dir = os.getcwd()
    mp3_folder_path = os.path.join(current_dir, 'MP3')
    
    # Create 'MP3' folder if it doesn't exist
    if not os.path.exists(mp3_folder_path):
        os.makedirs(mp3_folder_path)
        
    mp3_file_name = os.path.splitext(os.path.basename(pdf_file))[0] + '.mp3'
    mp3_file_path = os.path.join('MP3', mp3_file_name)
    
    # Remove existing mp3 file if present
    if os.path.exists(mp3_folder_path + '\\' + mp3_file_name):
        os.remove(mp3_folder_path + '\\' + mp3_file_name)
        
    # Save speech to mp3 file
    engine.save_to_file(pdf_string, mp3_file_path)
    engine.runAndWait()

def preprocess_text(text):
    """Preprocess the extracted text to remove unnecessary formatting"""
    # This function preprocesses the extracted text to remove excessive line breaks and spaces.
    # It helps in cleaning up the text before converting it to speech.
    
    # Remove excessive line breaks, multiple spaces, etc.
    text = re.sub(r'\n+', '\n', text)  # Replace multiple line breaks with a single one
    text = re.sub(r'\s+', ' ', text)   # Replace multiple spaces with a single one
    return text.strip()

def download_converted_file(text):
    """Converts uploaded PDF file to mp3 format and saves it to downloads folder"""
    # This function extracts text from the uploaded PDF file, preprocesses it,
    # then converts it to an mp3 file using threading to avoid blocking the main Tkinter loop.
    
    global pdf_string
    
    # Get string from PDF
    pdf_string = ""
    try:
        reader = PdfReader(pdf_file)
        number_of_pages = len(reader.pages)
        
        # Extract text from each page
        for number in range(number_of_pages):
            page = reader.pages[number]
            pdf_string += page.extract_text()
        
        # Preprocess the text
        pdf_string = preprocess_text(pdf_string)
        
        # Convert string to mp3 (using threading so that Tk window doesn't exit the mainloop)
        threading.Thread(
            target=run_pyttsx3, daemon=True
        ).start()
        text.configure(text=f"{name_without_filetype}.mp3\ndownloaded", text_color="green")
    except (NameError, FileNotFoundError):
        text.configure(text=f"File selected:\nnone", text_color="red")