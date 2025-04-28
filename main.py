
import requests



class VideoSummarizer:
    @staticmethod
    def video_sum(text):
        """Анализирует текст субтитров и возвращает краткое описание видео."""
        prompt = f"""Проанализируй предоставленный текст субтитров YouTube-видео и сгенерируй краткое описание его содержания. Выдели основную тему, ключевые идеи и важные моменты.  

**Текст субтитров:**  
{text}  

**Требования к ответу:**  
1. Основная тема видео (1-2 предложения).  
2. Ключевые идеи или аргументы (3-5 пунктов).  
3. Дополнительные важные детали, если они есть.  
4. Если в тексте есть вопросы или обсуждения, укажи их.  
5. Будь лаконичным, но информативным."""
        return VideoSummarizer.ask_model(prompt)

    @staticmethod
    def ask_model(prompt):
        """Отправляет запрос к локальной модели Ollama."""
        url = "http://127.0.0.1:11434/api/generate"
        payload = {
            "model": "qwen2.5-coder:3b",
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
