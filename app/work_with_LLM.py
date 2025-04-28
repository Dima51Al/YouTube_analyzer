import os

import requests
import dotenv


class VideoSummarizer:
    @staticmethod
    def video_sum(text):
        """Анализирует текст субтитров и возвращает описание видео."""
        prompt = f"""Проанализируй предоставленный текст субтитров YouTube-видео и сгенерируй максимально детальное и полное описание его содержания, включающее все важные детали, упомянутые аспекты и контекст. Укажи основную тему, ключевые идеи, аргументы, детали, вопросы, а также упомянутые примеры и контексты.  

        **Информация о видео и субтитры (субтитры в формате: время речи : текст речи):**  
        {text}  

        **Требования к ответу:**  
        1. Основная тема видео (1-10 предложений): постарайся выразить суть как можно точнее.  
        2. Ключевые идеи или аргументы (все, что было озвучено, до 20 пунктов): приведи их максимально полно.  
        3. Дополнительные важные детали, включая упомянутые примеры, даты, имена, события, контексты и термины.  
        4. Вопросы, обсуждения или гипотезы, если они есть, включая ответы, предположения или выводы из видео.  
        5. Перечисли упомянутые факты, даже если они кажутся второстепенными.  
        6. Если в видео есть структурированные блоки (например, "введение", "заключение"), укажи это.  
        7. Будь предельно информативным и включи максимум деталей, но сохрани логическую структуру и ясность.  
        """

        return VideoSummarizer.ask_model(prompt)

    @staticmethod
    def ask_model(prompt):
        """Отправляет запрос к локальной модели Ollama."""
        dotenv.load_dotenv()
        url = os.getenv("LLM_adress")
        model = os.getenv("LLM_model")
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json().get("response", "")
            return f"Ошибка: {response.status_code}, {response.text}"
        except requests.exceptions.RequestException as e:
            return f"Ошибка соединения: {e}"


if __name__ == '__main__':
    print(VideoSummarizer.ask_model("как дела"))
