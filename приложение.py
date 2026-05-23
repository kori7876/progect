import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random

# --- БАЗА ДАННЫХ И ВОПРОСЫ ---

# Цены на курсы
COURSES_PRICES = {
    "Python": 15000,
    "C++": 18000,
    "Java": 17000
}

# Промокод (скидка 20%)
PROMO_CODE = "SKIDKA"
DISCOUNT = 0.20

# База студентов
students_db = [
    {"name": "Иванов Иван Иванович", "email": "ivanov@mail.ru", "course": "Python", "status": "Активен", "score": 85},
    {"name": "Петров Петр Петрович", "email": "petrov@gmail.com", "course": "Java", "status": "Отчислен", "score": 40},
]

# Банк вопросов (Новый формат: правильный ответ отделен от неправильных)
QUESTIONS = {
    "Python": [
        {"q": "Какой тип данных используется для хранения целых чисел?", "correct": "int", "wrong": ["str", "float", "bool"]},
        {"q": "Какая функция выводит текст на экран?", "correct": "print()", "wrong": ["echo()", "console.log()", "write()"]},
        {"q": "Как правильно создать список?", "correct": "list = []", "wrong": ["list = {}", "list = ()", "list = <>"]},
        {"q": "Какой оператор используется для возведения в степень?", "correct": "**", "wrong": ["^", "//", "%"]},
        {"q": "Какой результат выражения 10 % 3?", "correct": "1", "wrong": ["3", "0", "3.33"]},
        {"q": "Как создать функцию?", "correct": "def myFunc():", "wrong": ["function myFunc():", "func myFunc():", "create myFunc():"]},
        {"q": "Какой метод добавляет элемент в конец списка?", "correct": "append()", "wrong": ["add()", "insert()", "push()"]},
        {"q": "Какая библиотека используется для работы с математикой?", "correct": "math", "wrong": ["sys", "calc", "numbers"]},
        {"q": "Как обозначается начало блока кода?", "correct": "отступ (табуляция)", "wrong": ["begin", "{}", "end"]},
        {"q": "Какой тип данных изменяемый?", "correct": "list", "wrong": ["tuple", "str", "int"]},
        {"q": "Какой результат bool('False')?", "correct": "True", "wrong": ["False", "Error", "None"]},
        {"q": "Как перебрать элементы списка?", "correct": "for", "wrong": ["while", "loop", "repeat"]},
        {"q": "Как импортировать модуль?", "correct": "import", "wrong": ["include", "using", "require"]},
        {"q": "Что означает pass?", "correct": "Ничего не делать", "wrong": ["Выйти из цикла", "Ошибка", "Пропустить итерацию"]},
        {"q": "Как получить длину строки?", "correct": "len()", "wrong": ["length()", "size()", "count()"]}
    ],
    "C++": [
        {"q": "Какой символ используется для указателя?", "correct": "*", "wrong": ["&", "#", "@"]},
        {"q": "Как включить библиотеку ввода-вывода?", "correct": "#include <iostream>", "wrong": ["import iostream", "using io;", "#include <stdio>"]},
        {"q": "С чего начинается выполнение программы?", "correct": "main()", "wrong": ["start()", "init()", "int main()"]},
        {"q": "Как объявить целочисленную переменную?", "correct": "int x;", "wrong": ["var x;", "integer x;", "num x;"]},
        {"q": "Какой оператор выделяет память динамически?", "correct": "new", "wrong": ["malloc", "alloc", "create"]},
        {"q": "Какой тип данных для текста (строки)?", "correct": "string", "wrong": ["text", "char", "str"]},
        {"q": "Какой цикл с предусловием?", "correct": "while", "wrong": ["do-while", "for", "loop"]},
        {"q": "Как освобождать память?", "correct": "delete", "wrong": ["free", "remove", "clear"]},
        {"q": "Для чего нужен namespace std?", "correct": "Чтобы избежать конфликтов имен", "wrong": ["Чтобы быстрее работало", "Для шифрования", "Для красоты"]},
        {"q": "Какой стандартный поток вывода?", "correct": "cout", "wrong": ["cin", "print", "write"]},
        {"q": "Как передать массив в функцию?", "correct": "По адресу", "wrong": ["По значению", "Нельзя", "По ссылке"]},
        {"q": "Указатель на ничего?", "correct": "nullptr", "wrong": ["void", "null", "empty"]},
        {"q": "Какой класс для строк в STL?", "correct": "string", "wrong": ["String", "str", "text"]},
        {"q": "Какой оператор доступа к члену класса через указатель?", "correct": "->", "wrong": [".", "::", ":"]},
        {"q": "Что такое заголовочный файл?", "correct": ".h", "wrong": [".exe", ".cpp", ".py"]}
    ],
    "Java": [
        {"q": "С какой буквы пишется имя класса?", "correct": "Большой", "wrong": ["маленькой", "любой", "с подчеркивания"]},
        {"q": "Какой метод является точкой входа?", "correct": "main()", "wrong": ["run()", "start()", "init()"]},
        {"q": "Все является объектом, кроме...", "correct": "примитивных типов", "wrong": ["массивов", "строк", "классов"]},
        {"q": "Как правильно объявить массив?", "correct": "int[] arr;", "wrong": ["int arr[];", "array<int> arr;", "int arr[5];"]},
        {"q": "Какая платформа Java позволяет запускать код?", "correct": "JVM", "wrong": ["JDK", "JRE", "API"]},
        {"q": "Какой оператор сравнения объектов?", "correct": ".equals()", "wrong": ["==", "compare()", "is"]},
        {"q": "Какие исключения проверяемые?", "correct": "Checked", "wrong": ["Unchecked", "Error", "Fatal"]},
        {"q": "Какой интерфейс для создания потоков?", "correct": "Runnable", "wrong": ["Threadable", "Process", "Task"]},
        {"q": "Какой модификатор доступа самый строгий?", "correct": "private", "wrong": ["public", "protected", "default"]},
        {"q": "Какой класс родитель для всех классов?", "correct": "Object", "wrong": ["Main", "Super", "Base"]},
        {"q": "Как вывести на консоль?", "correct": "System.out.println()", "wrong": ["console.log()", "print()", "echo()"]},
        {"q": "Сборщик мусора (GC) удаляет...", "correct": "недостижимые объекты", "wrong": ["все объекты", "нулевые ссылки", "файлы"]},
        {"q": "Для чего ключевое слово static?", "correct": "Принадлежит классу, а не объекту", "wrong": ["Для памяти", "Для констант", "Для импорта"]},
        {"q": "Какой тип данных для дробных чисел?", "correct": "double", "wrong": ["float", "decimal", "real"]},
        {"q": "Где хранятся объекты?", "correct": "Heap", "wrong": ["Stack", "Register", "Cache"]}
    ]
}

# --- ГЛАВНЫЙ КЛАСС ПРИЛОЖЕНИЯ ---

class OnlineCourseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Онлайн-Курс: Образовательная Платформа")
        self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        self.root.configure(bg="#f0f2f5")

        # Переменные состояния
        self.current_student = {}
        self.selected_course = tk.StringVar()
        self.current_price = tk.IntVar()
        self.promo_code = tk.StringVar()
        
        # Переменные теста
        self.test_questions = []
        self.current_question_index = 0
        self.test_score = 0
        self.user_answers = []

        # Стиль
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Arial', 12), padding=10, relief='flat')
        self.style.configure('TLabel', font=('Arial', 12), background="#f0f2f5")
        self.style.configure('Header.TLabel', font=('Arial', 24, "bold"), background="#f0f2f5", foreground="#333")
        
        # Основной контейнер
        self.main_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True)

        # Запуск первого экрана
        self.show_start_screen()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- ЭКРАН 1: ВЫБОР РОЛИ ---
    def show_start_screen(self):
        self.clear_frame()
        
        title = ttk.Label(self.main_frame, text="Добро пожаловать на платформу онлайн-курсов!", style='Header.TLabel')
        title.pack(pady=100)

        btn_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        btn_frame.pack(pady=20)

        student_btn = tk.Button(btn_frame, text="Студент", font=("Arial", 16), bg="#4CAF50", fg="white", 
                                width=20, height=2, command=self.show_registration)
        student_btn.pack(side="left", padx=20)

        teacher_btn = tk.Button(btn_frame, text="Преподаватель", font=("Arial", 16), bg="#2196F3", fg="white", 
                                width=20, height=2, command=self.show_teacher_login)
        teacher_btn.pack(side="left", padx=20)

    # --- ЭКРАН 2: РЕГИСТРАЦИЯ СТУДЕНТА ---
    def show_registration(self):
        self.clear_frame()
        
        frame = tk.Frame(self.main_frame, bg="white", padx=40, pady=40, relief="raised", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(frame, text="Регистрация студента", font=("Arial", 20, "bold"), background="white").grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(frame, text="ФИО:", background="white").grid(row=1, column=0, sticky="w", pady=10)
        self.entry_name = ttk.Entry(frame, width=30)
        self.entry_name.grid(row=1, column=1, pady=10)

        ttk.Label(frame, text="Почта:", background="white").grid(row=2, column=0, sticky="w", pady=10)
        self.entry_email = ttk.Entry(frame, width=30)
        self.entry_email.grid(row=2, column=1, pady=10)

        ttk.Label(frame, text="Курс:", background="white").grid(row=3, column=0, sticky="w", pady=10)
        course_combo = ttk.Combobox(frame, textvariable=self.selected_course, values=list(COURSES_PRICES.keys()), state="readonly", width=27)
        course_combo.grid(row=3, column=1, pady=10)
        course_combo.bind("<<ComboboxSelected>>", self.update_price)

        ttk.Label(frame, text="Промокод:", background="white").grid(row=4, column=0, sticky="w", pady=10)
        entry_promo = ttk.Entry(frame, textvariable=self.promo_code, width=30)
        entry_promo.grid(row=4, column=1, pady=10)
        entry_promo.bind("<KeyRelease>", self.update_price)

        self.lbl_price = ttk.Label(frame, text="", font=("Arial", 14, "bold"), foreground="#d32f2f", background="white")
        self.lbl_price.grid(row=5, column=0, columnspan=2, pady=20)

        reg_btn = tk.Button(frame, text="Регистрация", font=("Arial", 12), bg="#4CAF50", fg="white", 
                            command=self.process_registration)
        reg_btn.grid(row=6, column=0, columnspan=2, pady=10, ipadx=20)

        back_btn = tk.Button(frame, text="Назад", font=("Arial", 10), command=self.show_start_screen)
        back_btn.grid(row=7, column=0, columnspan=2, pady=5)

    def update_price(self, event=None):
        course = self.selected_course.get()
        if not course:
            return
        
        price = COURSES_PRICES[course]
        if self.promo_code.get() == PROMO_CODE:
            price = int(price * (1 - DISCOUNT))
        
        self.current_price.set(price)
        self.lbl_price.config(text=f"Цена курса: {price} руб.")

    def process_registration(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        course = self.selected_course.get()

        if not name or not email or not course:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля!")
            return

        self.current_student = {
            "name": name,
            "email": email,
            "course": course,
            "status": "Активен",
            "score": 0
        }

        self.test_questions = random.sample(QUESTIONS[course], len(QUESTIONS[course]))
        self.current_question_index = 0
        self.test_score = 0
        self.user_answers = []

        self.show_success_screen()

    # --- ЭКРАН 3: УСПЕШНАЯ РЕГИСТРАЦИЯ ---
    def show_success_screen(self):
        self.clear_frame()
        
        msg = ttk.Label(self.main_frame, text="Успешно!! Вы зарегистрировались.\nТеперь, пожалуйста, пройдите небольшой тест на знания.", 
                        style='Header.TLabel', justify="center")
        msg.pack(pady=200)

        btn = tk.Button(self.main_frame, text="Пройти тест", font=("Arial", 14), bg="#FF9800", fg="white", 
                        command=self.start_test)
        btn.pack(pady=20)

    # --- ЭКРАН 4: ТЕСТ ---
    def start_test(self):
        self.clear_frame()
        self.show_next_question()

    def show_next_question(self):
        self.clear_frame()
        
        if self.current_question_index < len(self.test_questions):
            q_data = self.test_questions[self.current_question_index]
            question_text = q_data["q"]
            
            # Собираем 1 правильный и 3 неправильных ответа
            answers = [q_data["correct"]] + q_data["wrong"]
            # Перемешиваем
            random.shuffle(answers)
            
            progress = ttk.Label(self.main_frame, text=f"Вопрос {self.current_question_index + 1} из {len(self.test_questions)}", 
                                 font=("Arial", 10), background="#f0f2f5")
            progress.pack(pady=10)

            q_label = ttk.Label(self.main_frame, text=question_text, font=("Arial", 16, "bold"), wraplength=800, background="#f0f2f5")
            q_label.pack(pady=40)

            self.selected_answer = tk.StringVar()
            for ans in answers:
                rb = tk.Radiobutton(self.main_frame, text=ans, variable=self.selected_answer, value=ans, 
                                    font=("Arial", 12), bg="#f0f2f5", indicatoron=0, width=40, height=2,
                                    selectcolor="#ddd")
                rb.pack(pady=5)

            btn = tk.Button(self.main_frame, text="Далее", font=("Arial", 12), bg="#2196F3", fg="white",
                            command=self.save_answer_and_next)
            btn.pack(pady=40)
        else:
            self.finish_test()

    def save_answer_and_next(self):
        if not self.selected_answer.get():
            messagebox.showwarning("Выбор ответа", "Пожалуйста, выберите вариант ответа!")
            return
        
        self.user_answers.append(self.selected_answer.get())
        self.current_question_index += 1
        self.show_next_question()

    def finish_test(self):
        correct_count = 0
        for i, q_data in enumerate(self.test_questions):
            correct_ans = q_data["correct"]
            if self.user_answers[i] == correct_ans:
                correct_count += 1
        
        self.test_score = (correct_count / len(self.test_questions)) * 100
        self.current_student['score'] = self.test_score
        
        students_db.append(self.current_student)

        self.clear_frame()
        res_text = f"Ваш результат: {int(self.test_score)}%"
        color = "green" if self.test_score >= 60 else "red"
        
        lbl = ttk.Label(self.main_frame, text=res_text, font=("Arial", 30, "bold"), foreground=color, background="#f0f2f5")
        lbl.pack(pady=200)

        self.root.after(2000, self.show_student_dashboard)

    # --- ЭКРАН 5: ГЛАВНАЯ СТУДЕНТА ---
    def show_student_dashboard_logic(self, view="home"):
        self.clear_frame()
        
        # --- САЙДБАР ---
        sidebar = tk.Frame(self.main_frame, bg="#2c3e50", width=250)
        sidebar.pack(side="left", fill="y")
        
        def create_menu_btn(text, cmd, is_exit=False):
            bg = "#c0392b" if is_exit else "#34495e"
            btn = tk.Button(sidebar, text=text, bg=bg, fg="white", relief="flat", font=("Arial", 12),
                            anchor="w", command=cmd)
            btn.pack(fill="x", padx=10, pady=5)

        create_menu_btn("Мои курсы", lambda: self.show_student_dashboard_logic("courses"))
        create_menu_btn("Расписание", lambda: self.show_student_dashboard_logic("schedule"))
        create_menu_btn("Дипломная работа", lambda: None)
        create_menu_btn("Чат с куратором", lambda: None)
        create_menu_btn("Настройки", lambda: None)
        
        tk.Frame(sidebar, height=2, bg="#7f8c8d").pack(fill="x", pady=10)
        create_menu_btn("Выход", self.student_logout, is_exit=True)

        # --- КОНТЕНТ ---
        content = tk.Frame(self.main_frame, bg="#f0f2f5")
        content.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        if view == "home":
            self._render_home(content)
        elif view == "courses":
            self._render_courses(content)
        elif view == "schedule":
            self._render_schedule(content)

    def _render_home(self, parent):
        ttk.Label(parent, text=f"Привет, {self.current_student['name']}!", style='Header.TLabel').pack(pady=20, anchor="w")
        info_frame = tk.Frame(parent, bg="white", padx=20, pady=20)
        info_frame.pack(fill="x", pady=10)
        ttk.Label(info_frame, text=f"Ваш курс: {self.current_student['course']}", font=("Arial", 14), background="white").pack(anchor="w")
        ttk.Label(info_frame, text=f"Ваш прогресс теста: {int(self.test_score)}%", font=("Arial", 14), background="white").pack(anchor="w")
        tk.Frame(parent, bg="black", height=200).pack(fill="x", pady=20)
        ttk.Label(parent, text="Добро пожаловать на главную страницу", font=("Arial", 20)).pack(pady=50)

    def _render_courses(self, parent):
        ttk.Label(parent, text="Мои курсы", style='Header.TLabel').pack(pady=20, anchor="w")
        c_frame = tk.Frame(parent, bg="white", padx=20, pady=20, relief="raised", bd=1)
        c_frame.pack(fill="x", pady=10)
        ttk.Label(c_frame, text=f"Курс: {self.current_student['course']}", font=("Arial", 18, "bold"), background="white").pack(anchor="w")
        ttk.Label(c_frame, text="Статус: Оплачен", foreground="green", background="white").pack(anchor="w", pady=5)
        ttk.Label(c_frame, text="Программа курса: 15 модулей", background="white").pack(anchor="w", pady=10)
        tk.Button(c_frame, text="Перейти к урокам", bg="#2196F3", fg="white").pack(anchor="w")

    def _render_schedule(self, parent):
        ttk.Label(parent, text="Расписание занятий", style='Header.TLabel').pack(pady=20, anchor="w")
        headers = ["День", "Время", "Предмет"]
        data = [
            ("Понедельник", "10:00", f"Лекция: {self.current_student['course']}"),
            ("Среда", "14:00", "Практика"),
            ("Пятница", "16:00", "Консультация")
        ]
        table = ttk.Treeview(parent, columns=headers, show="headings", height=10)
        for h in headers:
            table.heading(h, text=h)
            table.column(h, width=200)
        for row in data:
            table.insert("", "end", values=row)
        table.pack(fill="both", expand=True)

    def show_student_dashboard(self):
        self.show_student_dashboard_logic("home")

    def student_logout(self):
        self.current_student = {}
        self.show_start_screen()

    # --- ЛОГИКА ПРЕПОДАВАТЕЛЯ ---
    def show_teacher_login(self):
        password = simpledialog.askstring("Вход преподавателя", "Введите пароль для захода в аккаунт:", show='*', parent=self.root)
        
        if password is None: 
            return 
            
        if password == "867678":
            self.show_teacher_dashboard()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль!")

    def show_teacher_dashboard(self):
        self.clear_frame()
        
        # Шапка с заголовком и кнопкой выхода
        header = tk.Frame(self.main_frame, bg="#34495e", height=60)
        header.pack(fill="x")
        
        # Заголовок слева
        ttk.Label(header, text="Панель преподавателя", font=("Arial", 18, "bold"), 
                  foreground="white", background="#34495e").pack(side="left", padx=20, pady=10)
        
        # Кнопка выхода справа
        logout_btn = tk.Button(header, text="Выйти", bg="#c0392b", fg="white", 
                              font=("Arial", 12), relief="flat", padx=15,
                              command=self.teacher_logout)
        logout_btn.pack(side="right", padx=20, pady=10)

        main_content = tk.Frame(self.main_frame, bg="#f0f2f5")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)

        left_col = tk.Frame(main_content, bg="white")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(left_col, text="Список студентов", font=("Arial", 16, "bold"), background="white").pack(pady=10)

        columns = ("name", "course", "score", "status")
        self.tree = ttk.Treeview(left_col, columns=columns, show="headings", height=15)
        self.tree.heading("name", text="ФИО")
        self.tree.heading("course", text="Курс")
        self.tree.heading("score", text="Балл")
        self.tree.heading("status", text="Статус")
        
        self.tree.column("name", width=250)
        self.tree.column("course", width=100)
        self.tree.column("score", width=80)
        self.tree.column("status", width=100)
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = tk.Frame(left_col, bg="white")
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="Добавить студента", bg="#4CAF50", fg="white", command=self.add_student_dialog).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Отчислить", bg="#f44336", fg="white", command=self.expel_student).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Обновить", bg="#2196F3", fg="white", command=self.refresh_student_list).pack(side="left", padx=5)

        right_col = tk.Frame(main_content, bg="white")
        right_col.pack(side="right", fill="both", expand=True)

        ttk.Label(right_col, text="Расписание занятий", font=("Arial", 16, "bold"), background="white").pack(pady=10)
        schedule_frame = tk.Frame(right_col, bg="#ecf0f1", padx=10, pady=10)
        schedule_frame.pack(fill="x", padx=10)
        schedule_items = [
            "10:00 - Python: Основы",
            "12:00 - Java: Многопоточность",
            "14:00 - C++: Память",
            "16:00 - Практика"
        ]
        for item in schedule_items:
            ttk.Label(schedule_frame, text=item, background="#ecf0f1").pack(anchor="w", pady=2)

        ttk.Label(right_col, text="Статистика", font=("Arial, 16, bold"), background="white").pack(pady=20)
        stats_frame = tk.Frame(right_col, bg="#3498db", height=100)
        stats_frame.pack(fill="x", padx=10)
        ttk.Label(stats_frame, text=f"Всего студентов: {len(students_db)}", foreground="white", background="#3498db", font=("Arial", 14)).pack(pady=10)
        ttk.Label(stats_frame, text="Средний балл: 65%", foreground="white", background="#3498db", font=("Arial", 12)).pack()

        self.refresh_student_list()
    
    def teacher_logout(self):
        # Функция выхода для преподавателя
        self.show_start_screen()

    def refresh_student_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for student in students_db:
            self.tree.insert("", "end", values=(student["name"], student["course"], student["score"], student["status"]))

    def expel_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Внимание", "Выберите студента из списка!")
            return
        item_values = self.tree.item(selected_item)["values"]
        name = item_values[0]
        for s in students_db:
            if s["name"] == name:
                s["status"] = "Отчислен"
                break
        self.refresh_student_list()
        messagebox.showinfo("Успешно", f"Студент {name} отчислен.")

    def add_student_dialog(self):
        top = tk.Toplevel(self.root)
        top.title("Добавить студента")
        top.geometry("300x250")
        tk.Label(top, text="ФИО").pack(pady=5)
        e_name = tk.Entry(top)
        e_name.pack()
        tk.Label(top, text="Курс").pack(pady=5)
        e_course = ttk.Combobox(top, values=["Python", "C++", "Java"])
        e_course.pack()
        def save():
            new_student = {
                "name": e_name.get(),
                "email": "unknown@mail.ru",
                "course": e_course.get(),
                "status": "Активен",
                "score": 0
            }
            if new_student["name"] and new_student["course"]:
                students_db.append(new_student)
                self.refresh_student_list()
                top.destroy()
            else:
                messagebox.showerror("Ошибка", "Заполните поля")
        tk.Button(top, text="Сохранить", command=save).pack(pady=20)

# --- ЗАПУСК ---
if __name__ == "__main__":
    root = tk.Tk()
    root.state('zoomed') 
    app = OnlineCourseApp(root)
    root.mainloop()