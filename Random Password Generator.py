import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("600x500")
        
        # Файл для истории паролей
        self.history_file = "password_history.json"
        self.password_history = []
        
        self.load_history()
        self.setup_ui()
    
    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(
            self.root,
            text="Генератор случайных паролей",
            font=("Arial", 16, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=10)
        
        # Настройки параметров
        settings_frame = tk.Frame(self.root)
        settings_frame.pack(fill="x", padx=20, pady=5)
        
        # Ползунок длины пароля
        length_frame = tk.Frame(settings_frame)
        length_frame.pack(fill="x", pady=5)
        
        tk.Label(length_frame, text="Длина пароля (8–32):",
                 font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.length_var = tk.IntVar(value=12)
        self.length_scale = tk.Scale(
            length_frame,
            from_=8, to=32,
            orient=tk.HORIZONTAL,
            variable=self.length_var
        )
        self.length_scale.pack(side=tk.LEFT, fill="x", expand=True, padx=10)
        
        # Чекбоксы для выбора символов
        checkbox_frame = tk.Frame(settings_frame)
        checkbox_frame.pack(fill="x", pady=10)
        
        self.digits_var = tk.BooleanVar(value=True)
        self.letters_var = tk.BooleanVar(value=True)
        self.special_var = tk.BooleanVar(value=True)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Цифры (0-9)",
            variable=self.digits_var,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Буквы (a-z, A-Z)",
            variable=self.letters_var,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Checkbutton(
            checkbox_frame,
            text="Спецсимволы (!@#$%)",
            variable=self.special_var,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        # Кнопка генерации
        generate_button = tk.Button(
            self.root,
            text="Сгенерировать пароль",
            command=self.generate_password,
            bg="#27AE60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20
        )
        generate_button.pack(pady=15)
        
        # Поле отображения пароля
        password_frame = tk.Frame(self.root)
        password_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(password_frame, text="Сгенерированный пароль:",
                 font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Courier", 12),
            width=40,
            state="readonly"
        )
        self.password_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        
        copy_button = tk.Button(
            password_frame,
            text="Копировать",
            command=self.copy_to_clipboard,
            bg="#3498DB",
            fg="white"
        )
        copy_button.pack(side=tk.LEFT, padx=5)
        
        # Таблица истории
        history_frame = tk.Frame(self.root)
        history_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(history_frame, text="История паролей:",
                 font=("Arial", 12, "bold")).pack(anchor="w")
        
        columns = ("ID", "Пароль", "Длина", "Символы", "Дата генерации")
        self.history_tree = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            height=8
        )
        
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical",
                               command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Обновляем историю
        self.refresh_history()
