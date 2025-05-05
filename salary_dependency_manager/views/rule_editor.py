import tkinter as tk
from tkinter import ttk, messagebox
from utils.validation import validate_formula, validate_level, validate_position_name

class RuleEditor:
    def __init__(self, root, controller, position_name):
        self.root = tk.Toplevel(root)
        self.controller = controller
        self.position_name = position_name
        self.root.title(f'Редагування правил - {position_name}')

        # Таблиця для редагування правил
        columns = ('Рівень', 'Стартова посада', 'Стартовий рівень', 'Формула для ЗП', 'Формула для Бонусу')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=4)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.grid(row=0, column=0, columnspan=5)

        # Кнопка збереження
        self.save_button = tk.Button(self.root, text='Зберегти', command=self.save_rules)
        self.save_button.grid(row=1, columnspan=5)

        self.tree.bind('<Double-1>', self.on_double_click)

        self.load_rules()

    def load_rules(self):
        # Очищення таблиці
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Отримання даних про позицію
        position = self.controller.get_position_data(self.position_name)

        # Проходження по рівнях і вставка даних у таблицю
        for level in range(4):
            level_data = position.get_salary_data(level)

            values = (
                level + 1,
                level_data['from_position'] if level_data['from_position'] is not None else '-' if level == 0 else self.position_name,
                level_data['from_level'] if level_data['from_level'] is not None else '-' if level == 0 else level,
                level_data['formula_salary'] if level_data['formula_salary'] else 'S',
                level_data['formula_bonus'] if level_data['formula_bonus'] else 'B'
            )
            self.tree.insert('', 'end', values=values)

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        col_index = int(col[1:]) - 1

        if col_index == 1: # Залежна посада
            self.edit_combobox(item, col_index, list(self.controller.positions.keys()))
        elif col_index == 2: # Рівень залежності
            self.edit_combobox(item, col_index, ['1', '2', '3', '4'])
        else: # Формули
            self.edit_entry(item, col_index)

    def edit_combobox(self, item, col_index, values):
        x, y, width, height = self.tree.bbox(item, column=col_index)
        combobox = ttk.Combobox(self.root, values=values, state='readonly')
        combobox.place(x=x, y=y, width=width, height=height)
        combobox.focus_set()

        def save_selection(event):
            self.tree.set(item, column=col_index, value=combobox.get())
            combobox.destroy()

        combobox.bind('<<ComboboxSelected>>', save_selection)

    def edit_entry(self, item, col_index):
        x, y, width, height = self.tree.bbox(item, column=col_index)
        entry = tk.Entry(self.root)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, self.tree.item(item, 'values')[col_index])
        entry.focus_set()

        def save_entry(event):
            self.tree.set(item, column=col_index, value=entry.get())
            entry.destroy()

        entry.bind('<Return>', save_entry)
        entry.bind('<FocusOut>', save_entry)

    def save_rules(self):
        position = self.controller.get_position_data(self.position_name)
        print(self.tree.get_children())
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            to_level = int(values[0])
            from_position = values[1] if values[1] != '-' else None
            from_level = int(values[2]) if values[2] != '-' else None
            formula_salary = values[3].strip()
            formula_bonus = values[4].strip()
            print(" **** ")
            print(to_level)
            print(from_position)
            print(from_level)
            print(formula_salary)
            print(formula_bonus)
            print(" **** ")

            # Валідація формул
            valid_salary, msg_salary = validate_formula(formula_salary)
            valid_bonus, msg_bonus = validate_formula(formula_bonus)

            if not valid_salary or not valid_bonus:
                messagebox.showerror("Помилка", msg_salary if not valid_salary else msg_bonus)
                return

            try:
                # Зберігання залежності в посаді
                position.set_dependency(to_level, from_position, from_level, formula_salary, formula_bonus)


                # Зберігання залежності в контролері
                if from_position and from_level:
                    self.controller.add_dependency(from_position, from_level, self.position_name, to_level, formula_salary, formula_bonus)


            except Exception as e:
                messagebox.showerror("Помилка", str(e))
                return

        # Закриття вікна після успішного збереження
        self.controller.main_view.update_tree()
        self.controller.calculate_salaries()
        self.root.destroy()
