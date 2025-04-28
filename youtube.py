
from yt_dlp import YoutubeDL
from typing import Optional

import yt_dlp
import os


def get_subtitles(video_url, lang='en'):
    """
    Получает субтитры из YouTube видео

    :param video_url: URL видео на YouTube
    :param lang: язык субтитров (например 'en', 'ru')
    :return: текст субтитров или None в случае ошибки
    """
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'subtitlesformat': 'vtt',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': 'subtitles',  # временный файл
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

            # Проверяем наличие субтитров
            if not info['requested_subtitles'] and not info['automatic_captions']:
                print("Субтитры не найдены для этого видео")
                return None

            # Скачиваем субтитры
            ydl.download([video_url])

            # Ищем скачанный файл субтитров
            sub_file = None
            for f in os.listdir():
                if f.endswith(f'.{lang}.vtt'):
                    sub_file = f
                    break

            if sub_file:
                with open(sub_file, 'r', encoding='utf-8') as f:
                    subtitles = f.read()
                os.remove(sub_file)  # удаляем временный файл
                return subtitles

        return None

    except Exception as e:
        print(f"Ошибка при получении субтитров: {e}")
        return None

def get_video_metadata(url: str) -> Optional[dict]:
    """Получает метаданные видео через yt-dlp как библиотеку."""
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,
        'dump_single_json': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            metadata = ydl.extract_info(url, download=False)

        header_parts = {}

        if title := metadata.get('title'):
            header_parts["title"] = title

        if channel := metadata.get('channel'):
            header_parts["channel"] = channel

        if tags := metadata.get('tags'):
            header_parts["tags"] = tags

        return header_parts

    except Exception as e:
        print(f"Ошибка получения метаданных: {str(e)}")
        return None


def metadata_text(url):
    dict_meta = get_video_metadata(url)
    subtitles = get_subtitles(url, lang="ru")

    prompt = f"""
Анализируйте предоставленную информацию о YouTube видео и выполните задание, указанное ниже.

=== МЕТАДАННЫЕ ВИДЕО ===
Название: {dict_meta.get('title', 'не указано')}
Автор/канал: {dict_meta.get('channel', 'не указан')}
Теги: {', '.join(dict_meta.get('tags', [])) if dict_meta.get('tags') else 'не указаны'}

=== ТРАНСКРИПТ/СУБТИТРЫ ===
{subtitles if subtitles else 'Субтитры недоступны'}

"""
    return prompt


if __name__ == '__main__':
    # Пример использования
    url = "https://www.youtube.com/watch?v=KBXTc4l5xZw"
    metadata = get_video_metadata(url)
    if metadata:
        print(metadata)
