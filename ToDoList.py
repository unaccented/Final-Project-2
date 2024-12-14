import json
from tkinter import Tk, Listbox, Button, Entry, Label, END, messagebox

class Task:
    def __init__(self, description, due_date=None, completed=False):
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def to_dict(self):
        return {
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(data["description"], data.get("due_date"), data.get("completed", False))

class TaskManager:
    def __init__(self, data_file="tasks.json"):
        self.data_file = data_file
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].completed = True
            self.save_tasks()

    def load_tasks(self):
        try:
            with open(self.data_file, "r") as f:
                self.tasks = [Task.from_dict(task) for task in json.load(f)]
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []

    def save_tasks(self):
        with open(self.data_file, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)

class TaskApp:
    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("To-Do List Application")

        self.task_list = Listbox(root, width=50, height=15)
        self.task_list.pack()

        self.add_label = Label(root, text="Task Description:")
        self.add_label.pack()
        self.add_entry = Entry(root, width=40)
        self.add_entry.pack()

        self.due_label = Label(root, text="Due Date (optional):")
        self.due_label.pack()
        self.due_entry = Entry(root, width=40)
        self.due_entry.pack()

        self.add_button = Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.complete_button = Button(root, text="Mark Completed", command=self.mark_completed)
        self.complete_button.pack()

        self.delete_button = Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack()

        self.load_tasks()

    def load_tasks(self):
        self.task_list.delete(0, END)
        for i, task in enumerate(self.manager.tasks):
            status = "[Done]" if task.completed else "[Pending]"
            self.task_list.insert(END, f"{i + 1}. {status} {task.description} (Due: {task.due_date or 'N/A'})")

    def add_task(self):
        description = self.add_entry.get().strip()
        due_date = self.due_entry.get().strip()
        if not description:
            messagebox.showerror("Error", "Task description cannot be empty.")
            return
        self.manager.add_task(Task(description, due_date))
        self.add_entry.delete(0, END)
        self.due_entry.delete(0, END)
        self.load_tasks()

    def delete_task(self):
        selected = self.task_list.curselection()
        if not selected:
            messagebox.showerror("Error", "No task selected.")
            return
        self.manager.delete_task(selected[0])
        self.load_tasks()

    def mark_completed(self):
        selected = self.task_list.curselection()
        if not selected:
            messagebox.showerror("Error", "No task selected.")
            return
        self.manager.mark_completed(selected[0])
        self.load_tasks()

if __name__ == "__main__":
    root = Tk()
    app = TaskApp(root)
    root.mainloop()
