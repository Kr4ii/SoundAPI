# Audio Processing API

REST API сервис для обработки аудиофайлов с возможностью:
- Подавления шумов
- Полосовой фильтрации
- Нормализации громкости

## Структура проекта
```
project/
├── app/
│ ├── api/
│ │ └── api.py # Роутеры API
│ ├── src/
│ │ └── audio_processing.py # Логика обработки аудио
│ └── logs/ # Логи приложения
│ ├── tests/ # Тесты
│ │ └── test__api.py # тесты API
│ └── main.py # Основной файл приложения
├── data/
│ ├── temp/ # Временные файлы
│ ├── output/ # Обработанные файлы
├── Dockerfile
└── requirements.txt
```
## Требования

- Docker 20.10+
- Python 3.9+ 

## Установка и запуск

### Через Docker (рекомендуется)

1. Соберите образ:
```bash
docker build -t audio-processor .
```

2. Запустите контейнер:
```bash
docker run -p 8000:8000 audio-processor
```
### Локальная установка
1. Установите зависимости:
```bash
pip install -r requirements.txt
```
2. Создайте необходимые директории:
```bash
mkdir -p data/temp data/output app/logs
```
3. Запустите сервер:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
## Использование API

Документация доступна через Swagger UI:
```url
http://localhost:8000/docs
```

### Примеры запросов
1. Подавление шумов
```bash
curl -X POST "http://localhost:8000/api/v1/noise-reduction/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@input.mp3" \
     -F "reduction_strength=0.7"
```
2. Полосовая фильтрация
```bash
curl -X POST "http://localhost:8000/api/v1/bandpass-filter/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@input.wav" \
     -F "lowcut=300" \
     -F "highcut=3400"
```
3. Нормализация громкости
```bash
curl -X POST "http://localhost:8000/api/v1/normalize-volume/" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@input.wav" \
     -F "target_dBFS=-15.0"
```
### Ответ API

Успешный ответ содержит ссылку на обработанный файл:
```json
{
  "processed_file": "http://localhost:8000/output/processed_audio.wav"
}
```
## Тестирование

1. Установите тестовые зависимости:

```bash
pip install pytest
```
2. Запустите тесты:

```bash
pytest tests/ -v
```
## Логирование
Все запросы и ошибки записываются в файл:
```
app/logs/app.log
```