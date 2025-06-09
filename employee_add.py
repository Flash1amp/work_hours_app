import tkinter as tk
from tkinter import messagebox
from db import add_employee
from datetime import datetime

from ui import root


def open_add_employee_window():
    add_window = tk.Toplevel(root)
    add_window.title("Добавление нового сотрудника")
    add_window.geometry("400x300")

    # Метки и поля
    tk.Label(add_window, text="Имя:").pack()
    entry_name = tk.Entry(add_window)
    entry_name.pack()

    tk.Label(add_window, text="Отдел:").pack()
    entry_dept = tk.Entry(add_window)
    entry_dept.pack()

    tk.Label(add_window, text="Роль:").pack()
    entry_role = tk.Entry(add_window)
    entry_role.pack()

    tk.Label(add_window, text="Дата найма (YYYY-MM-DD):").pack()
    entry_hire_date = tk.Entry(add_window)
    entry_hire_date.pack()

    def submit():
        name = entry_name.get().strip()
        dept = entry_dept.get().strip()
        role = entry_role.get().strip()
        hire_date = entry_hire_date.get().strip()

        if not name or not hire_date:
            messagebox.showwarning("Ошибка", "Имя и дата найма обязательны.")
            return

        try:
            datetime.strptime(hire_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD.")
            return

        from db import add_employee
        try:
            add_employee(name, dept, role, hire_date)
            messagebox.showinfo("Успех", f"Сотрудник {name} добавлен.")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника: {e}")

    tk.Button(add_window, text="Сохранить", command=submit).pack(pady=10)
