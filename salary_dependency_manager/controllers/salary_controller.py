from models.position import Position
from models.dependency import Dependency
from utils.validation import validate_formula, validate_level, validate_position_name

class SalaryController:
    def __init__(self):
        self.positions = {}
        self.dependencies = []

    def add_position(self, name, base_salary=0, bonus=0):
        if name in self.positions:
            raise ValueError(f"Посада з ім'ям {name} вже існує")
        self.positions[name] = Position(name, base_salary, bonus)
        print(self.positions[name])

    def remove_position(self, name):
        if name in self.positions:
            del self.positions[name]
            # Видалення пов'язаних залежностей
            self.dependencies = [d for d in self.dependencies if d.from_position != name and d.to_position != name]
        else:
            raise ValueError(f"Посада {name} не знайдена")


    def add_dependency(self, from_position, from_level, to_position, to_level, formula_salary, formula_bonus):

        # Перевірка чи посади існують
        if not (from_position in self.positions and to_position in self.positions):
            raise ValueError(f"add_dependency: Одна з посад не існує: {from_position} або {to_position}")

        # Перевірка рівнів
        if not (1 <= from_level <= 4 and 1 <= to_level <= 4):
            raise ValueError(f"add_dependency: Рівні мають бути в межах від 1 до 4. Введено: {from_level}, {to_level}")

        # Валідація формул
        for formula, msg in [(formula_salary, "зарплати"), (formula_bonus, "бонусу")]:
            valid, error_msg = validate_formula(formula)
            if not valid:
                raise ValueError(f"add_dependency: Невірна формула для {msg}: {error_msg}")

        # Пошук існуючої залежності та оновлення, якщо знайдено
        existing_dependency = next(
            (dep for dep in self.dependencies if dep.from_position == from_position and dep.from_level == from_level),
            None
        )

        if existing_dependency:
            existing_dependency.to_position = to_position
            existing_dependency.to_level = to_level
            existing_dependency.formula_salary = formula_salary
            existing_dependency.formula_bonus = formula_bonus
        else:
            # Додавання нової залежності
            new_dependency = Dependency(from_position, from_level, to_position, to_level, formula_salary, formula_bonus)
            self.dependencies.append(new_dependency)


    def calculate_salaries(self):
        print("Початок розрахунку зарплат...")

        # Цикл для стабілізації розрахунків
        for _ in range(10):
            for dep in self.dependencies:
                try:
                    # Перевірка чи існують посади
                    if dep.from_position not in self.positions or dep.to_position not in self.positions:
                        print(f"Помилка: Посада {dep.from_position} або {dep.to_position} не існує")
                        continue

                    from_data = self.positions[dep.from_position].get_salary_data(dep.from_level - 1)
                    to_data = self.positions[dep.to_position].get_salary_data(dep.to_level - 1)


                    salary_data = {
                        'S': from_data['base_salary'],
                        'B': from_data['bonus']
                    }


                    # Обчислення зарплати та бонусу з обробкою помилок
                    try:
                        new_salary = eval(dep.formula_salary, {}, salary_data)
                        new_bonus = eval(dep.formula_bonus, {}, salary_data)
                    except Exception as e:
                        print(f"Помилка при обчисленні формули: {e}")
                        new_salary = 0
                        new_bonus = 0


                    # Оновлення значень поточної посади
                    to_data['base_salary'] = new_salary
                    to_data['bonus'] = new_bonus
                except Exception as e:
                    print(f"Помилка при розрахунку для {dep.to_position} (Рівень {dep.to_level}): {e}")

        # Оновлення таблиці в головному вікні
        if hasattr(self, 'main_view'):
            self.main_view.update_tree()

    def get_position_data(self, name):
        if name not in self.positions:
            raise ValueError(f"Посада {name} не знайдена")
        return self.positions[name]

    def __repr__(self):
        return f"SalaryController(Positions: {list(self.positions.keys())}, Dependencies: {len(self.dependencies)})"
