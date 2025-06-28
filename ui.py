import tkinter as tk
from tkinter import ttk, messagebox
from db import get_employee_id, start_work_session, end_work_session, add_employee, get_all_employees, get_sessions_by_employee
from datetime import datetime

root = tk.Tk()
root.title("Приложение для учета рабочего времени")
root.geometry("500x300")
root.resizable(False, False)


style = ttk.Style()
style.configure('TButton', font=('Arial', 12))
style.configure('TLabel', font=('Arial', 14))
style.configure('TEntry', font=('Arial', 12))


label = ttk.Label(root, text="Добро пожаловать в приложение для учета рабочего времени")
label.pack(pady=(20, 15))

entry = ttk.Entry(root, width=40)
entry.pack(pady=10)

frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=20)

# Старт смены
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

# Конец смены
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

# Добавление нового сотрудника
def open_add_employee_window():
    add_window = tk.Toplevel(root)
    add_window.title("Добавление нового сотрудника")
    add_window.geometry("400x300")

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

        try:
            add_employee(name, dept, role, hire_date)
            messagebox.showinfo("Успех", f"Сотрудник {name} добавлен.")
            add_window.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника: {e}")

    tk.Button(add_window, text="Сохранить", command=submit).pack(pady=10)
    
def open_employee_view_window():
    window = tk.Toplevel()
    window.title("Список сотрудников и сессий")
    window.geometry("900x500")

    # Левый Treeview — сотрудники
    employee_tree = ttk.Treeview(window, columns=("ID", "Name", "Department", "Role", "Hire Date"), show="headings")
    for col in ("ID", "Name", "Department", "Role", "Hire Date"):
        employee_tree.heading(col, text=col)
        employee_tree.column(col, width=100)
    employee_tree.pack(side="left", fill="both", expand=True)

    for emp in get_all_employees():
        employee_tree.insert("", "end", values=emp)

    # Правый Treeview — сессии
    session_tree = ttk.Treeview(window, columns=("Start Time", "End Time"), show="headings")
    session_tree.heading("Start Time", text="Начало")
    session_tree.heading("End Time", text="Окончание")
    session_tree.column("Start Time", width=150)
    session_tree.column("End Time", width=150)
    session_tree.pack(side="right", fill="both", expand=True)

    # ⬇ Вставляем внутрь функции
    def on_employee_select(event):
        selected = employee_tree.selection()
        if selected:
            emp_values = employee_tree.item(selected[0], "values")
            employee_id = emp_values[0]

            session_tree.delete(*session_tree.get_children())

            sessions = get_sessions_by_employee(employee_id)
            for session in sessions:
                session_tree.insert("", "end", values=session)

    employee_tree.bind("<<TreeviewSelect>>", on_employee_select)


# Кнопочки
btn_start = ttk.Button(frame_buttons, text="Начать смену", command=start_shift)
btn_start.pack(side=tk.LEFT, padx=10)

btn_end = ttk.Button(frame_buttons, text="Закончить смену", command=end_shift)
btn_end.pack(side=tk.LEFT, padx=10)

add_btn = tk.Button(root, text="Добавить сотрудника", command=open_add_employee_window)
add_btn.pack(pady=10)

btn_view_employees = tk.Button(root, text="Просмотр сотрудников", command=open_employee_view_window)
btn_view_employees.pack(pady=10)



root.mainloop()