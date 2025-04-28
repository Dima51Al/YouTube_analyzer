import customtkinter as ctk
import asyncio
import threading
import pyperclip
from youtube import get_video_metadata as summ_video
from work_with_LLM import VideoSummarizer

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Главное приложение
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Видео Суммаризация")
        self.geometry("700x500")  # Увеличил размер окна для большего комфорта

        self.main_frame = MainFrame(self)
        self.result_frame = ResultFrame(self)
        self.loading_frame = LoadingFrame(self)

        self.main_frame.pack(fill="both", expand=True)

    def show_result_frame(self, final_text):
        self.loading_frame.pack_forget()
        self.result_frame.update_text(final_text)
        self.result_frame.pack(fill="both", expand=True)

    def show_main_frame(self):
        self.result_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)

    def show_loading_frame(self):
        self.main_frame.pack_forget()
        self.loading_frame.pack(fill="both", expand=True)


# Первая страница
class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text="Введите ссылку на видео или текст", font=("Arial", 22))
        self.label.pack(pady=20)

        input_frame = ctk.CTkFrame(self)  # Контейнер для текстбокса и кнопок
        input_frame.pack(pady=10)

        self.text_input = ctk.CTkTextbox(input_frame, width=400, height=100, font=("Arial", 16))
        self.text_input.grid(row=0, column=0, padx=(0, 10))

        self.paste_button = ctk.CTkButton(
            input_frame,
            text="Вставить",
            command=self.paste_from_clipboard,
            width=80
        )
        self.paste_button.grid(row=0, column=1, padx=(0, 10))

        self.clear_button = ctk.CTkButton(
            input_frame,
            text="Очистить",
            command=self.clear_text_input,
            width=80
        )
        self.clear_button.grid(row=0, column=2)

        self.send_button = ctk.CTkButton(self, text="Отправить", command=self.start_processing)
        self.send_button.pack(pady=10)

    def paste_from_clipboard(self):
        clipboard_text = pyperclip.paste()
        self.text_input.delete("1.0", "end")
        self.text_input.insert("1.0", clipboard_text)

    def clear_text_input(self):
        self.text_input.delete("1.0", "end")

    def start_processing(self):
        threading.Thread(target=self.send_text_async).start()

    def send_text_async(self):
        asyncio.run(self.send_text())

    async def send_text(self):
        user_text = self.text_input.get("1.0", "end").strip()
        if user_text:
            self.master.show_loading_frame()
            await asyncio.sleep(0.1)  # Чтобы окно успело появиться

            processed = await asyncio.to_thread(summ_video, user_text)
            final_text = str(await asyncio.to_thread(VideoSummarizer.video_sum, processed))

            self.master.show_result_frame(final_text)


# Вторая страница
# Вторая страница
class ResultFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text="Результат", font=("Arial", 22))
        self.label.pack(pady=10)

        self.textbox = ctk.CTkTextbox(self, width=600, height=300, font=("Arial", 16), wrap="word")
        self.textbox.pack(pady=10)
        self.textbox.configure(state="disabled")

        button_frame = ctk.CTkFrame(self)  # Рамка для кнопок
        button_frame.pack(pady=10)

        self.back_button = ctk.CTkButton(button_frame, text="Назад", command=self.master.show_main_frame)
        self.back_button.grid(row=0, column=0, padx=10)

        self.copy_button = ctk.CTkButton(button_frame, text="Копировать", command=self.copy_to_clipboard)
        self.copy_button.grid(row=0, column=1, padx=10)

    def update_text(self, new_text):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", new_text)
        self.textbox.configure(state="disabled")

    def copy_to_clipboard(self):
        text_to_copy = self.textbox.get("1.0", "end").strip()
        if text_to_copy:
            pyperclip.copy(text_to_copy)



# Окно загрузки (как страница)
class LoadingFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text="Пожалуйста, подождите...", font=("Arial", 22))
        self.label.pack(expand=True)


# Запуск приложения
if __name__ == "__main__":
    app = App()
    app.mainloop()
