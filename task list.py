import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import datetime
import os

FILE_NAME = "todoist.json"

# ----------------- Data Handling ----------------- #
def load_data():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    return {"Inbox": []}

def save_data(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=2)

# ----------------- Main App ----------------- #
class TodoistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Todoist")
        self.root.geometry("600x400")

        self.data = load_data()
        self.current_project = "Inbox"

        # Project Frame
        self.project_frame = tk.Frame(root, width=150, bg="#ddd")
        self.project_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.project_listbox = tk.Listbox(self.project_frame)
        self.project_listbox.pack(fill=tk.BOTH, expand=True)
        self.project_listbox.bind("<<ListboxSelect>>", self.change_project)

        # Task Frame
        self.task_frame = tk.Frame(root, bg="#f5f5f5")
        self.task_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(self.task_frame, font=("Arial", 12))
        self.task_listbox.pack(fill=tk.BOTH, expand=True)

        # Buttons
        self.add_task_btn = tk.Button(self.task_frame, text="➕ Add Task", command=self.add_task)
        self.add_task_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.done_task_btn = tk.Button(self.task_frame, text="✔️ Mark Done", command=self.mark_done)
        self.done_task_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_task_btn = tk.Button(self.task_frame, text="❌ Delete", command=self.delete_task)
        self.delete_task_btn.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_project_btn = tk.Button(self.project_frame, text="➕ Project", command=self.add_project)
        self.add_project_btn.pack(side=tk.BOTTOM, pady=5)

        self.refresh_projects()
        self.refresh_tasks()

    # ----------------- Project Functions ----------------- #
    def refresh_projects(self):
        self.project_listbox.delete(0, tk.END)
        for project in self.data.keys():
            self.project_listbox.insert(tk.END, project)

    def change_project(self, event):
        try:
            selection = self.project_listbox.curselection()
            if selection:
                self.current_project = self.project_listbox.get(selection)
                self.refresh_tasks()
        except:
            pass

    def add_project(self):
        project = simpledialog.askstring("New Project", "Enter project name:")
        if project and project not in self.data:
            self.data[project] = []
            save_data(self.data)
            self.refresh_projects()

    # ----------------- Task Functions ----------------- #
    def refresh_tasks(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.data[self.current_project]:
            status = "✔️" if task["done"] else "❌"
            due = f" (Due: {task['due']})" if task["due"] else ""
            self.task_listbox.insert(tk.END, f"{status} {task['task']}{due}")

    def add_task(self):
        task_name = simpledialog.askstring("New Task", "Enter task:")
        if task_name:
            due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD) or leave blank:")
            try:
                if due_date:
                    datetime.datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return

            task = {"task": task_name, "done": False, "due": due_date or ""}
            self.data[self.current_project].append(task)
            save_data(self.data)
            self.refresh_tasks()

    def mark_done(self):
        try:
            idx = self.task_listbox.curselection()[0]
            self.data[self.current_project][idx]["done"] = not self.data[self.current_project][idx]["done"]
            save_data(self.data)
            self.refresh_tasks()
        except:
            pass

    def delete_task(self):
        try:
            idx = self.task_listbox.curselection()[0]
            self.data[self.current_project].pop(idx)
            save_data(self.data)
            self.refresh_tasks()
        except:
            pass

# ----------------- Run App ----------------- #
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoistApp(root)
    root.mainloop()
