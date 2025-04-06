# Simple VTT Translator Script

This Python script uses Tkinter for a simple GUI to translate VTT subtitle files from English to another language using the OpenAI API (`gpt-4o`).

## Requirements

* Python 3.x
* `openai` library (`pip install openai`)
* `tkinter` (usually built-in, may need `sudo apt-get install python3-tk` on Linux)
* OpenAI API Key (for GPT-4o)

## Configuration

1.  **Edit the script:** Open the `.py` file.
2.  **Find the line:** `os.environ['OPENAI_API_KEY'] = 'API_KEY_HERE'`
3.  **Replace `'API_KEY_HERE'` with your actual OpenAI API key.**

**⚠️ Security Note:** Be careful sharing code with your API key hardcoded. For personal use only is best.

## Usage

1.  Run the script: `python vtt_translate.py`
2.  Enter the target language in the GUI.
3.  Click "Upload and Process File" and select your English `.vtt` file.
4.  Wait for the process to complete.

## Output

* The script processes the file in chunks.
* Translated chunks are saved as separate numbered files (e.g., `1_processed_...vtt`, `2_processed_...vtt`) in a new folder named `processed_files` inside the original file's directory.
* **You will need to manually combine these files if you need a single output file. Some Edge cases might not be handled perfectly, it's recommended to check the output. **

## License

MIT License
