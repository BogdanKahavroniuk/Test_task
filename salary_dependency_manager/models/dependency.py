class Dependency:
    def __init__(self, from_position, from_level, to_position, to_level, formula_salary, formula_bonus):
        if not (1 <= from_level <= 4 and 1 <= to_level <= 4):
            raise ValueError("Dependency: Рівні мають бути від 1 до 4")

        self.from_position = from_position
        self.from_level = from_level
        self.to_position = to_position
        self.to_level = to_level
        self.formula_salary = formula_salary
        self.formula_bonus = formula_bonus

    def calculate_salary(self, salary_data):
        try:
            return eval(self.formula_salary, {}, salary_data)
        except Exception as e:
            print(f"calculate_salary: Помилка при обчисленні зарплати: {e}")
            return 0

    def calculate_bonus(self, salary_data):
        try:
            return eval(self.formula_bonus, {}, salary_data)
        except Exception as e:
            print(f"calculate_bonus: Помилка при обчисленні бонусу: {e}")
            return 0

    def __repr__(self):
        return (f"Dependency({self.from_position}, Level {self.from_level} -> "
                f"{self.to_position}, Level {self.to_level}, "
                f"Formula Salary: {self.formula_salary}, Formula Bonus: {self.formula_bonus})")