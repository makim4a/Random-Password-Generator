    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.password_history, f, ensure_ascii=False, indent=2)