# YouTube_analyzer


---

# Проект: Работа с LLM и YouTube

## Описание

Проект взаимодействует с локальным LLM-сервером и YouTube.  
**Важно**: проект предназначен для личного использования.

## Структура проекта

```
app/
├── .env
├── .gitignore
├── main.py
├── requirements.txt
├── work_with_LLM.py
├── youtube.py
└── README.md
```

## Быстрый старт

### 1. Клонируйте репозиторий и перейдите в папку `app`:

```bash
cd app
```

### 2. Создайте файл `.env`

В корне папки `app/` создайте файл `.env` со следующим содержимым:

```dotenv
LLM_adress="http://127.0.0.1:11434/api/generate"
LLM_model="qwen2.5-coder:3b"
```

> Эти настройки используются только для локальной работы.

### 3. Создайте виртуальное окружение и активируйте его:

```bash
#Windows
python -m venv venv

venv\Scripts\activate

```
или
```bash
#Linux
python -m venv venv

source venv/bin/activate
```



### 4. Установите зависимости:

```bash
pip install -r requirements.txt
```

### 5. Запуск проекта:

```bash
python main.py
```


### 6. Сборка проекта в exe (опционально)

Для создания исполняемого файла используйте :

```bash
python builder.py
```

После сборки exe-файл будет находиться в папке `dist/`.

### 7. Работа с собранным exe-файлом

1. Поместите `YouTube_analyzer.exe`  в отдельную папку
2. В этой же папке создайте файл `config.txt` со следующим содержимым:

```
LLM_adress="http://127.0.0.1:11434/api/generate" # в моём случае
LLM_model="qwen2.5-coder:3b" # в моём случае
```

3. Запустите приложение 

> Примечание: Для работы exe-файла требуется, чтобы локальный LLM-сервер (например, Ollama) был запущен и доступен по указанному в config.txt адресу.


---