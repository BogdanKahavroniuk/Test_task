import re

def validate_formula(formula):
    """
    Перевіряє валідність формули, дозволяючи лише змінні S, B та математичні операції.
    """
    allowed_chars = re.compile(r'^[0-9+\-*/(). SB]*$')
    if not allowed_chars.match(formula.replace(' ', '')):
        return False, "Формула містить недопустимі символи."

    try:
        # Перевіряємо, чи можна безпечно виконати формулу
        eval(formula, {"S": 1, "B": 1})
    except Exception as e:
        return False, f"Помилка у формулі: {e}"

    return True, "Формула валідна."

def validate_level(level):
    """
    Перевіряє, чи рівень знаходиться в межах 1-4.
    """
    if 1 <= level <= 4:
        return True
    return False

def validate_position_name(name):
    """
    Перевіряє, чи назва посади валідна (не порожня і без спеціальних символів).
    """
    if not name or not re.match(r'^[A-Za-zА-Яа-яІіЇїЄєҐґ0-9_ ]+$', name):
        return False, "Некоректна назва посади. Допустимі лише букви, цифри, пробіли та _."
    return True, "Назва валідна."

def validate_dependency(from_position, to_position, from_level, to_level):
    """
    Перевіряє коректність залежності.
    """
    if from_position == to_position and from_level == to_level:
        return False, "Посада та рівень не можуть залежати від самих себе."
    return True, "Залежність валідна."

if __name__ == '__main__':
    # Прості тести
    print(validate_formula("S * 1.1 + B * 0.5"))
    print(validate_level(3))
    print(validate_position_name("Менеджер_2024"))
    print(validate_dependency("Pos1", "Pos2", 1, 2))