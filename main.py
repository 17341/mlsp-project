import tkinter as tk
import tkinter.scrolledtext as st

def log_message(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)

def update_buttons():
    start_button.config(state=tk.NORMAL if not is_streaming and not is_paused else tk.DISABLED)
    stop_button.config(state=tk.NORMAL if is_streaming else tk.DISABLED)
    pause_button.config(text="Pause Streaming" if not is_paused else "Resume Streaming", state=tk.NORMAL if is_streaming or is_paused else tk.DISABLED)

def toggle_streaming():
    global is_streaming, is_paused
    if not is_streaming:
        log_message("Streaming started")
        is_streaming = True
        is_paused = False
        update_buttons()
    elif is_paused:
        log_message("Streaming resumed")
        is_paused = False
        update_buttons()

def stop_streaming():
    global is_streaming, is_paused
    if is_streaming:
        log_message("Streaming stopped")
        is_streaming = False
        is_paused = False
        update_buttons()

def pause_streaming():
    global is_paused
    if not is_paused:
        log_message("Streaming paused")
        is_paused = True
        update_buttons()
    else:
        log_message("Streaming resumed")
        is_paused = False
        update_buttons()

def add_word():
    word = entry.get()
    if word:
        listbox.insert(tk.END, word)
        entry.delete(0, tk.END)
        log_message(f"Word added: {word}")

def remove_word():
    selected = listbox.curselection()
    if selected:
        word = listbox.get(selected[0])
        listbox.delete(selected[0])
        log_message(f"Word removed: {word}")

# Initialize streaming state
is_streaming = False
is_paused = False

app = tk.Tk()
app.title("Streaming Control")
app.geometry("800x500")  # Set window size

# Create Frames
left_frame = tk.Frame(app)
left_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

right_frame = tk.Frame(app)
right_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ns")

# Buttons in the left frame
start_button = tk.Button(left_frame, text="Start Streaming", command=toggle_streaming, font=("Helvetica", 14))
start_button.grid(row=0, column=0, pady=10, sticky="ew")

stop_button = tk.Button(left_frame, text="Stop Streaming", command=stop_streaming, state=tk.DISABLED, font=("Helvetica", 14))
stop_button.grid(row=1, column=0, pady=10, sticky="ew")

pause_button = tk.Button(left_frame, text="Pause Streaming", command=pause_streaming, state=tk.DISABLED, font=("Helvetica", 14))
pause_button.grid(row=2, column=0, pady=10, sticky="ew")

# Input Field and List in the right frame
entry = tk.Entry(right_frame, font=("Helvetica", 16))
entry.grid(row=0, column=0, pady=10, sticky="ew")

add_button = tk.Button(right_frame, text="Add Word", command=add_word, font=("Helvetica", 14))
add_button.grid(row=1, column=0, pady=10, sticky="ew")

# Creating a Scrollbar and attaching it to Listbox
listbox = tk.Listbox(right_frame, font=("Helvetica", 16))
scrollbar = tk.Scrollbar(right_frame, orient="vertical", command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)

# Grid the Listbox and Scrollbar
listbox.grid(row=2, column=0, pady=10, sticky="ew")
scrollbar.grid(row=2, column=1, pady=10, sticky="ns")

remove_button = tk.Button(right_frame, text="Remove Selected Word", command=remove_word, font=("Helvetica", 14))
remove_button.grid(row=3, column=0, pady=10, sticky="ew")

# Log Text Area under the buttons in the left frame
log_frame = tk.Frame(left_frame)
log_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

log_text = st.ScrolledText(log_frame, wrap=tk.WORD, state=tk.DISABLED, font=("Helvetica", 12), height=10, width=40)
log_text.pack(expand=True, fill='both')

update_buttons()  # Initialize button states

app.mainloop()
