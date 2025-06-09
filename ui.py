import tkinter as tk
from tkinter import ttk, messagebox
from db import get_employee_id, start_work_session, end_work_session

root = tk.Tk()
root.title("Приложение для учета рабочего времени")
root.geometry("500x300")
root.resizable(False, False)

style = ttk.Style()
style.configure('TButton', font=('Arial', 12))
style.configure('TLabel', font=('Arial', 14))
style.configure('TEntry', font=('Arial', 12))

label = ttk.Label(root, text="Добро пожаловать в приложение для учета рабочего времени!")
label.pack(pady=(20, 15))

entry = ttk.Entry(root, width=40)
entry.pack(pady=10)

frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=20)

def start_shift():
    name = entry.get().strip()
    if not name:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите имя сотрудника.")
        return
    if messagebox.askyesno("Подтверждение", f"Начать смену для {name}?"):
        employee_id = get_employee_id(name)
        if employee_id:
            start_work_session(employee_id)
            messagebox.showinfo("Информация", f"Смена начата для {name} (ID {employee_id})")
            entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", f"Сотрудник {name} не найден.")

def end_shift():
    name = entry.get().strip()
    if not name:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите имя сотрудника.")
        return
    if messagebox.askyesno("Подтверждение", f"Завершить смену для {name}?"):
        employee_id = get_employee_id(name)
        if employee_id:
            end_work_session(employee_id)
            messagebox.showinfo("Информация", f"Смена завершена для {name} (ID {employee_id})")
            entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", f"Сотрудник {name} не найден.")

btn_start = ttk.Button(frame_buttons, text="Начать смену", command=start_shift)
btn_start.pack(side=tk.LEFT, padx=10)

btn_end = ttk.Button(frame_buttons, text="Закончить смену", command=end_shift)
btn_end.pack(side=tk.LEFT, padx=10)

root.mainloop()
