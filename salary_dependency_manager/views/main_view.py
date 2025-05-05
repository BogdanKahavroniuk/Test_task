import tkinter as tk
from tkinter import ttk, messagebox
from controllers.salary_controller import SalaryController
from views.rule_editor import RuleEditor

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class MainView:
    def __init__(self, root, controller):
        self.root = root
        self.root.title('Salary Dependency Manager')
        self.controller = controller

        # Верхній фрейм для введення даних
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(pady=10)

        self.entry_position = tk.Entry(self.frame_top)
        self.entry_position.grid(row=0, column=0)

        self.button_add = tk.Button(self.frame_top, text="Додати посаду", command=self.add_position)
        self.button_add.grid(row=0, column=1)

        self.button_delete = tk.Button(self.frame_top, text="Видалити посаду", command=self.delete_position)
        self.button_delete.grid(row=0, column=2)

        # Кнопки "Зберегти" та "Завантажити"
        self.frame_buttons = tk.Frame(root)
        self.frame_buttons.pack(pady=5)

        self.button_save = tk.Button(self.frame_buttons, text="Зберегти", command=self.save_data)
        self.button_save.pack(side=tk.LEFT, padx=5)

        self.button_load = tk.Button(self.frame_buttons, text="Завантажити", command=self.load_data)
        self.button_load.pack(side=tk.LEFT, padx=5)

        # Таблиця для відображення посад
        self.tree = ttk.Treeview(root, columns=("Посада", "ЗП1", "Бонус1", "Сума1", "ЗП2", "Бонус2", "Сума2", "ЗП3", "Бонус3", "Сума3", "ЗП4", "Бонус4", "Сума4"), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree.bind('<Double-1>', self.open_rule_editor)

    def add_position(self):
        name = self.entry_position.get().strip()
        if not name:
            messagebox.showerror("Помилка", "Назва посади не може бути порожньою.")
            return
        try:
            self.controller.add_position(name)
            self.update_tree()
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def delete_position(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Помилка", "Оберіть посаду для видалення.")
            return

        name = self.tree.item(selected_item)['values'][0]
        try:
            self.controller.remove_position(name)
            messagebox.showinfo("Успіх", f"Посаду '{name}' видалено.")
            self.update_tree()
        except ValueError as e:
            messagebox.showerror("Помилка", str(e))

    def update_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        for name, position in self.controller.positions.items():
            row_data = [name]
            for level in range(4):
                salary_data = position.get_salary_data(level)
                total = salary_data['base_salary'] + salary_data['bonus']
                row_data.extend([salary_data['base_salary'], salary_data['bonus'], total])
            self.tree.insert('', 'end', values=row_data)

    def open_rule_editor(self, event):
        item = self.tree.selection()[0]
        position_name = self.tree.item(item)['values'][0]
        # Припускається, що RuleEditor визначено в іншому файлі
        # Вам потрібно буде адаптувати імпорт, якщо це не так
        from rule_editor import RuleEditor
        RuleEditor(self.root, self.controller, position_name)

    def save_data(self):
        
        
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not filepath:
            return
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
           
                writer.writerow(self.tree['columns'])
             
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)['values'])
            messagebox.showinfo("Успіх", f"Дані збережено у '{filepath}'")
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при збереженні файлу: {e}")

    def load_data(self):
        
        filepath = filedialog.askopenfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        
        if not filepath:
            return
        try:
            
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  
                self.controller.positions.clear()
                self.update_tree() 
                for row in reader:
                    if len(row) == 13: 
                        position_name = row[0]
                        salary_data = {}
                        try:
                            for i in range(4):
                                base_salary = int(row[1 + i * 3])
                                bonus = int(row[2 + i * 3])
                                salary_data[i] = {'base_salary': base_salary, 'bonus': bonus}
                            self.controller.add_position(position_name, initial_data=salary_data)
                        except ValueError:
                            messagebox.showerror("Помилка", f"Неправильний формат числових даних у рядку: {row}")
                            continue
                self.update_tree()
                
                
            messagebox.showinfo("Успіх", f"Дані завантажено з '{filepath}'")
        except FileNotFoundError:
            messagebox.showerror("Помилка", "Файл не знайдено.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка при завантаженні файлу: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    # Припускається, що Controller вже визначено
    class Controller:
        def __init__(self):
            self.positions = {}

        def add_position(self, name, initial_data=None):
            if name in self.positions:
                raise ValueError(f"Посада '{name}' вже існує.")
            if initial_data is None:
                self.positions[name] = Position(name)
            else:
                self.positions[name] = Position(name, initial_data)

        def remove_position(self, name):
            if name not in self.positions:
                raise ValueError(f"Посади '{name}' не існує.")
            del self.positions[name]

        def get_position(self, name):
            return self.positions.get(name)

    class Position:
        
        def __init__(self, name, initial_data=None):
            self.name = name
            self.salary_levels = {}
            if initial_data:
                self.salary_levels = initial_data
            else:
                for i in range(4):
                    self.salary_levels[i] = {'base_salary': 0, 'bonus': 0}


        def get_salary_data(self, level):
            return self.salary_levels.get(level, {'base_salary': 0, 'bonus': 0})

    controller = Controller()
    app = MainView(root, controller)
    root.mainloop()