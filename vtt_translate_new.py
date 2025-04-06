import tkinter as tk
from tkinter import filedialog, messagebox
import openai
import os
import re

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = 'API_KEY_HERE'
openai.api_key = os.getenv('OPENAI_API_KEY')

PROMPT_TEMPLATE = """
Act like a professional audiovisual localization specialist with 15+ years of experience in translating subtitles for global corporate training videos, executive briefings, and business tutorials. You are an expert in professional tone, cultural nuance, and VTT subtitle formatting.

Objective: I have an English VTT file that needs to be translated into {language}. The goal is to produce a translation that is suitable for business contexts, with language that is both professional and easy to understand, similar to the tone of the original English version. 

Task Instructions: Maintain Structural Elements: Keep all VTT structural elements, such as time stamps and formatting codes, intact. Do not alter the formatting or time codes. 
Translation Process: Translate the English text into {language}, ensuring the language is appropriate for business processes. Aim for a translation that is both professional and easy to understand, mirroring the accessibility of the original English text. Shorten long sentences and restructure them as needed to enhance readability in {language}. 

Terminology and Context: Use precise and commonly understood business terminology in {language}, replacing technical terms with more accurate or widely used alternatives. 
Cultural and Professional Appropriateness: Adjust the language to ensure it is culturally appropriate for {language} business settings. Maintain a tone that is professional yet conversational and natural, making it easy for viewers to understand. 
Formatting and Consistency: Ensure consistent use of punctuation, line breaks, and time codes. Allow sentences to carry over into subsequent timestamps if necessary to maintain clarity and readability. 
Output Guidelines: The final {language} subtitles should be concise, clear, and professionally suitable for a business audience, while remaining easy to understand.
No unnecessary outputs other than the VTT file.

Final Step: Take a deep breath and work on this problem step-by-step.

File:
"""

def process_file(language):
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")], title="Select a File")
    if not file_path:
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Split the file content into sections based on VTT structure (ensure not to cut in the middle of a section)
        sections = re.split(r'\n(?=\w{8}-.+?\n\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})', file_content)

        # Create smaller chunks of approximately 10000 characters, ensuring to end at a complete sentence (with a period followed by a newline)
        chunks = []
        current_chunk = ""
        for section in sections:
            if len(current_chunk) + len(section) <= 10000:
                current_chunk += section + '\n'
            else:
                # Find the last complete sentence end (period followed by a newline)
                last_sentence_end_index = current_chunk.rfind('.\n')
                if last_sentence_end_index != -1:
                    complete_chunk = current_chunk[:last_sentence_end_index + 2]  # Include the period and newline
                    remainder = current_chunk[last_sentence_end_index + 2:].lstrip() + section + '\n'
                else:
                    complete_chunk = current_chunk
                    remainder = section + '\n'

                chunks.append(complete_chunk)
                current_chunk = remainder

        if current_chunk:
            chunks.append(current_chunk)

        # Create a separate folder for the processed files
        output_folder = os.path.join(os.path.dirname(file_path), "processed_files")
        os.makedirs(output_folder, exist_ok=True)

        # Process each chunk
        for idx, chunk in enumerate(chunks, start=1):
            combined_prompt = PROMPT_TEMPLATE.format(language=language) + chunk

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": combined_prompt}
                ],
                max_tokens=16384,
                temperature=0.2, # Lower temperature for more accurate outputs
                frequency_penalty=0.0
            )

            response_text = response.choices[0].message.content.strip()

            # Save each processed chunk in the separate folder
            output_path = os.path.join(output_folder, f"{idx}_processed_{os.path.basename(file_path)}")
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(response_text)

        messagebox.showinfo("Success", f"Processed files saved in folder: {output_folder}")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def on_process_button_click():
    language = language_entry.get()
    if language:
        process_file(language)
    else:
        messagebox.showerror("Error", "Please enter a target language.")

root = tk.Tk()
root.title("File Processor")

language_label = tk.Label(root, text="Enter Target Language:")
language_label.pack(pady=5)

language_entry = tk.Entry(root)
language_entry.pack(pady=5)

process_button = tk.Button(root, text="Upload and Process File", command=on_process_button_click)
process_button.pack(pady=20)

root.mainloop()
