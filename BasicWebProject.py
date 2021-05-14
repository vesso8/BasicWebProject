from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter.ttk import Combobox
import json
from tkinter import messagebox

priority_mapper = {1: "Low", 2: "Medium", 3: "High"}


def clear_view():
    for slave in tk.grid_slaves():
        slave.destroy()


def render_main_view():
    clear_view()
    Button(tk, text="List all tasks", bg="blue", fg="white", command=render_list_tasks_view).grid(column=0, row=0, padx=20, pady=20)
    Button(tk, text="Create task", bg="green", fg="white", command=render_create_view).grid(column=1, row=0, padx=20, pady=20)


def create_task(name, description, priority, is_completed):
    try:
        with open("db.txt", "r") as file:
            tasks = json.loads(file.read())
    except:
        tasks = []

    task = {"name": name, "description": description, "priority": priority_mapper[priority], "is_completed": is_completed}
    tasks.append(task)
    with open("db.txt", "w") as file:
        json.dump(tasks, file)


def delete_task(task):
    answer = messagebox.askquestion("Confirm delete", "Are you sure?")
    if answer == "no":
        return
    task_as_obj = eval(task)
    if task:
        with open("db.txt", "r+") as file:
            all_tasks = json.loads(file.read())
            for index in range(len(all_tasks)):
                if all_tasks[index]["name"] == task_as_obj["name"]:
                    break
            del all_tasks[index]
            file.truncate(0)
            file.seek(0)
            json.dump(all_tasks, file)
    render_list_tasks_view()


def render_list_tasks_view():
    clear_view()
    try:
        with open("db.txt", "r") as file:
            tasks = json.loads(file.read())
    except:
        tasks = []

    selected_task = StringVar(tk)
    dropdown = Combobox(tk, textvariable=selected_task, width="100")
    dropdown['values'] = tasks
    dropdown.grid(row=0, column=0)
    Button(tk, text="Delete", bg="red", command=lambda: delete_task(selected_task.get())).grid(row=1, column=0)
    Button(tk, text="Cancel", bg="black", fg="white",
           command=render_main_view).grid(column=1, row=1)


def render_create_view():
    clear_view()
    Label(tk, text="Enter your task's name:").grid(column=0, row=0, padx=20, pady=20)
    task_name = Entry(tk)
    task_name.grid(column=1, row=0, padx=20, pady=20)
    Label(tk, text="Enter your task's description:").grid(column=0, row=1, padx=20, pady=20)
    task_description = ScrolledText(tk,  width =20, height=10)
    task_description.grid(column=1, row=1, padx=20, pady=20)
    Label(tk, text="Enter your task's priority:").grid(column=0, row=2, padx=20, pady=20)
    task_priority = IntVar()
    radio_button_1 = Radiobutton(tk, text="Low", value=1, variable=task_priority)
    radio_button_2 = Radiobutton(tk, text="Medium", value=2, variable=task_priority)
    radio_button_3 = Radiobutton(tk, text="High", value=3, variable=task_priority)
    radio_button_1.grid(column=1,  row=2, padx=20, pady=20)
    radio_button_2.grid(column=2,  row=2, padx=20, pady=20)
    radio_button_3.grid(column=3,  row=2, padx=20, pady=20)
    Label(tk, text="Is the task completed?:").grid(column=0, row=3, padx=20, pady=20)
    task_completed = BooleanVar()
    check_box = Checkbutton(tk, variable=task_completed)
    check_box.grid(column=1, row=3, padx=20, pady=20)
    Button(tk, text="Create task", bg="green", fg="white",
           command=lambda: create_task(task_name.get(), task_description.get("1.0", END),
                                       task_priority.get(), task_completed.get()))\
        .grid(column=0, row=4)
    Button(tk, text="Cancel", bg="black", fg="white",
           command=render_main_view).grid(column=1, row=4)


if __name__ == '__main__':
    tk = Tk()
    tk.geometry("700x500")
    tk.title("Hello")
    render_main_view()
    tk.mainloop()
