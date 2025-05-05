import tkinter as tk
from controllers.salary_controller import SalaryController
from views.main_view import MainView

def main():
    # Ініціалізація головного вікна
    root = tk.Tk()
    root.title("Salary Dependency Manager")
    root.geometry("1200x600")

    # Ініціалізація контролера та головного вікна
    controller = SalaryController()
    app = MainView(root, controller)

    # Передача посилання на головне вікно в контролер
    controller.main_view = app

    # Запуск основного циклу
    root.mainloop()

if __name__ == '__main__':
    main()