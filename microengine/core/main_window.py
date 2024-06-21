import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os
import subprocess

def new_project():
    project_name = simpledialog.askstring("New Project", "Enter project name:")

    if project_name:
        project_location = filedialog.askdirectory(initialdir="Projects", title="Select Project Location")

        if project_location:
            project_path = os.path.join(project_location, project_name)
            try:
                os.makedirs(project_path, exist_ok=True)
                messagebox.showinfo("Success", f"New project '{project_name}' created at {project_location}")
                print(f"New project '{project_name}' created at {project_location}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not create project: {e}")
                print(f"Could not create project: {e}")
        else:
            messagebox.showwarning("Cancelled", "Project creation cancelled.")
            print("Project creation cancelled.")
    else:
        messagebox.showwarning("Cancelled", "Project creation cancelled.")
        print("Project creation cancelled.")

def open_project():
    project_path = filedialog.askdirectory(initialdir="Projects", title="Select Project Folder")
    if project_path:
        print(f"Opened project: {project_path}")
        subprocess.Popen(["python", "game_creator.py", project_path])

root = tk.Tk()
root.title("Micro Engine - Project Manager")
root.geometry('1280x720')
root.iconbitmap(r"C:\Users\Admin\Desktop\microengine\assets\micro engine logo.ico")
root.configure(bg='#2E2E2E')

new_project_button = tk.Button(root, text="New Project", command=new_project, bg='#4B4B4B', fg='white')
new_project_button.pack(pady=20)

open_project_button = tk.Button(root, text="Open Project", command=open_project, bg='#4B4B4B', fg='white')
open_project_button.pack(pady=20)

root.mainloop()
