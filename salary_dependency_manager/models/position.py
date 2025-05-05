class Position:
    def __init__(self, name, base_salary=0, bonus=0):
        self.name = name
        self.levels = [{
            'base_salary': base_salary,
            'bonus': bonus,
            'formula_salary': '',
            'formula_bonus': '',
            'from_position': None,
            'from_level': None
        } for _ in range(4)]

    def set_base_salary(self, level, base_salary):
        if 0 <= level < 4:
            self.levels[level]['base_salary'] = base_salary
        else:
            raise ValueError("set_base_salary: Рівень має бути в межах від 0 до 3")

    def set_bonus(self, level, bonus):
        if 0 <= level < 4:
            self.levels[level]['bonus'] = bonus
        else:
            raise ValueError("set_bonus: Рівень має бути в межах від 0 до 3")

    def set_dependency(self, to_level, from_position, from_level, formula_salary, formula_bonus):
        print(f"(Position) Спроба встановлення залежності до (to:) {self.name}, Рівень {to_level} <- з (from:) {from_position}, Рівень {from_level}")

        if not (1 <= to_level <= 4):
            print(f"set_dependency: Невірний рівень для {self.name}: level={to_level}")
            raise ValueError("Рівень має бути від 1 до 4")

        if from_level is not None and not (1 <= from_level <= 4):
            print(f"set_dependency: Невірний рівень залежності для {self.name}:from_level={from_level}")
            raise ValueError("set_dependency: Рівень залежності має бути від 1 до 4")

        level_data = self.levels[to_level - 1]
        level_data['from_position'] = from_position
        level_data['from_level'] = from_level
        level_data['formula_salary'] = formula_salary
        level_data['formula_bonus'] = formula_bonus

        print( f"Position: ({self.name}, "
               f"Levels: {self.levels})")
        return f"Position({self.name}, Levels: {self.levels})"


    def get_salary_data(self, level):
        if 0 <= level < 4:
            print("get_salary_data - рівень " + str(level)+" : " +str((self.levels[level])))
            return self.levels[level]
        else:
            print("get_salary_data: Рівень має бути в межах від 0 до 3")
            raise ValueError("get_salary_data: Рівень має бути в межах від 0 до 3")

    def __repr__(self):
        return f"Position({self.name}, Levels: {self.levels})"