import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk
import threading
import subprocess

def run_workflow():
    topic = topic_entry.get()
    results = results_entry.get()
    preview_flag = "preview" if preview_var.get() else "no-preview"
    if topic:
        # clean and show log
        output_text.delete(1.0, tk.END)
        output_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)
        # Start progress bar
        progress_bar.pack(pady=5)
        progress_bar.start()
        def run_script():
            try:
                # subprocess.run(["python", "ai_scraper_backend.py", topic], check=True)
                process = subprocess.Popen([
                    r"python3",
                    "ai_scraper_backend.py",
                    topic,
                    preview_flag,
                    results
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8')

                for line in process.stdout:
                    # output_text.insert(tk.END, line)
                    if "✅" in line or "completed" in line.lower():
                        output_text.insert(tk.END, line, "success")
                    elif "❌" in line or "failed" in line.lower():
                        output_text.insert(tk.END, line, "error")
                    elif "🔍" in line or "🧭" in line:
                        output_text.insert(tk.END, line, "info")
                    elif "http" in line:
                        output_text.insert(tk.END, line, "highlight")
                    else:
                        output_text.insert(tk.END, line)
                    # end of the output log box
                    output_text.see(tk.END)
                process.wait()
                # clean up the topic field
                topic_entry.delete(0, tk.END)

            except Exception as e:
                output_text.insert(tk.END, f"Workflow failed:\n{e}\n")
            finally:
                # Stop progress bar
                progress_bar.stop()
                progress_bar.pack_forget()
        # start thread
        threading.Thread(target=run_script).start()
    else:
        messagebox.showwarning("Input Required", "Please enter a topic.")

# Create the main window
root = tk.Tk()
root.title("AI Web Scraper")

# create frame for topic input
input_frame = tk.Frame(root)
input_frame.pack(padx=15)

# create frame for options input
options_frame = tk.Frame(root)
options_frame.pack(padx=15)

# create frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(padx=10, pady=10)

# create frame for output log
output_frame = tk.Frame(root)

# Create and place widgets
# topic label and entry
tk.Label(input_frame, text="Enter topic to scrape:").pack(pady=5)
topic_entry = tk.Entry(input_frame, width=60)
topic_entry.pack(pady=5)
# preview checkbox
preview_var = tk.BooleanVar()
preview_check = tk.Checkbutton(options_frame, text="Enable Preview", variable=preview_var)
preview_check.pack(side=tk.LEFT, padx=10, pady=5)
# results entry and label
tk.Label(options_frame, text="Number of Results:").pack(side=tk.LEFT, padx=10)
results_entry = tk.Entry(options_frame, width=5)
results_entry.pack(side=tk.LEFT, padx=10)
results_entry.insert(0, "3")  # default value
# create buttons
tk.Button(button_frame, text="Run Scrape", command=run_workflow).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Exit", command=root.quit).pack(side=tk.LEFT, padx=10)

# create output log
output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=15)
output_text.pack(fill=tk.BOTH, expand=True)
# 🎨 Define color tags
output_text.tag_config("info", foreground="blue")
output_text.tag_config("success", foreground="green")
output_text.tag_config("error", foreground="red")
output_text.tag_config("highlight", foreground="orange")

# progress bar
progress_bar = ttk.Progressbar(root, mode='determinate')
progress_bar.pack_forget()  # Hide it initially

# Start the GUI event loop
root.mainloop()