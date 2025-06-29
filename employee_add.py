import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox
from db import add_employee
from datetime import datetime
from ui import root

def open_add_employee_window():
    add_window = tk.Toplevel(root)
    add_window.title("Добавление нового сотрудника")
    add_window.geometry("400x300")

    tk.Label(add_window, text="Имя:").pack()
    entry_name = tk.Entry(add_window)
    entry_name.pack()

    # Отдел (Combobox)
    tk.Label(add_window, text="Отдел:").pack()
    departments = ["Отдел разработки", "Бухгалтерия", "Отдел кадров", "Маркетинг", "Продажи"]
    combo_dept = ttk.Combobox(add_window, values=departments, state="readonly")
    combo_dept.pack()

    # Роль (Combobox)
    tk.Label(add_window, text="Роль:").pack()
    roles = ["Менеджер", "Разработчик", "Бухгалтер", "HR", "Аналитик"]
    combo_role = ttk.Combobox(add_window, values=roles, state="readonly")
    combo_role.pack()

    tk.Label(add_window, text="Дата найма (YYYY-MM-DD):").pack()
    entry_hire_date = tk.Entry(add_window)
    entry_hire_date.pack()

    def submit():
        name = entry_name.get().strip()
        dept = combo_dept.get().strip()
        role = combo_role.get().strip()
        hire_date = entry_hire_date.get().strip()

        if not name or not hire_date:
            messagebox.showwarning("Ошибка", "Имя и дата найма обязательны.")
            return

        if not dept:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите отдел из списка.")
            return

        if not role:
            messagebox.showwarning("Ошибка", "Пожалуйста, выберите роль из списка.")
            return

        try:
            datetime.strptime(hire_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD.")
            return

        try:
            add_employee(name, dept, role, hire_date)
            messagebox.showinfo("Успех", f"Сотрудник {name} добавлен.")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника: {e}")


    tk.Button(add_window, text="Сохранить", command=submit).pack(pady=10)
