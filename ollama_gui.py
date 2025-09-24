import tkinter as tk
from tkinter import scrolledtext
import requests
import os
import json
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # Replace with your model name
VAULT_DIR = "ollama_vault" # update to preferred location, for now the vault is in your home directory

ASCII_ART = """⠀⠀⣀⣀⠀⠀⠀⠀⠀⣀⣀⠀⠀
⠀⢰⡏⢹⡆⠀⠀⠀⢰⡏⢹⡆⠀
⠀⢸⡇⣸⡷⠟⠛⠻⢾⣇⣸⡇⠀
⢠⡾⠛⠉⠁⠀⠀⠀⠈⠉⠛⢷⡄
⣿⠀⢀⣄⢀⣠⣤⣄⡀⣠⡀⠀⣿
⢻⣄⠘⠋⡞⠉⢤⠉⢳⠙⠃⢠⡿
⣼⠃⠀⠀⠳⠤⠬⠤⠞⠀⠀⠘⣷
⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿
⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇
⢸⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡿"""

def ensure_vault_directory():
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)

def save_interaction(prompt, response):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = os.path.join(VAULT_DIR, f"{timestamp}.json")
    interaction = {
        "timestamp": timestamp,
        "prompt": prompt,
        "response": response
    }
    with open(filename, 'w') as f:
        json.dump(interaction, f, indent=2)

def send_prompt():
    prompt = prompt_entry.get("1.0", tk.END).strip()
    if not prompt:
        return
    output_text.insert(tk.END, f"You: {prompt}\n")

    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })

    if response.ok:
        result = response.json()["response"]
        output_text.insert(tk.END, f"\nOllama: {result}\n\n")
        ensure_vault_directory()
        save_interaction(prompt, result)
    else:
        output_text.insert(tk.END, "\n Error talking to Ollama.\n\n")
        save_interaction(prompt, "Error: Failed to get response from Ollama")

    prompt_entry.delete("1.0", tk.END)

# GUI Setup
root = tk.Tk()
root.title("OllamaChat")

# Center ASCII art
ascii_frame = tk.Frame(root)
ascii_frame.pack(pady=10)
ascii_label = tk.Label(ascii_frame, text=ASCII_ART, font=("Courier", 10), justify="center")
ascii_label.pack()

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
output_text.pack(padx=10, pady=10)

prompt_entry = tk.Text(root, height=4, width=80)
prompt_entry.pack(padx=10, pady=(0, 5))

send_button = tk.Button(root, text="Send", command=send_prompt)
send_button.pack(pady=(0, 10))

root.mainloop()