Проект представляет собой RAG-систему (Retrieval-Augmented Generation) для работы с данными о смартфонах из интернет-магазина. Система включает:

1. Парсинг данных о смартфонах
2. Хранение данных в ChromaDB
3. Использование языковых моделей через LangChain и HuggingFace
4. API на FastAPI с авторизацией через JWT (PyJWT)

## Установка и настройка

### Предварительные требования

- Python 3.8+
- Docker (опционально, для запуска ChromaDB в контейнере)

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Переменные окружения

Создайте файл `.env` в корне проекта со следующими переменными:

```
DATABASE_URL=localhost:8000
CHROMA_DB_PATH=./chroma_db
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
HUGGINGFACEHUB_API_TOKEN=your-huggingface-token
```

## Запуск системы

### Запуск парсера

```bash
python scripts/parse_phones.py
```

### Запуск API сервера

```bash
uvicorn app.main:app --reload
```

API будет доступно по адресу: `http://localhost:8000`

## API Endpoints

### Аутентификация

- `POST /token` - Получение JWT токена
- `POST /register` - Регистрация нового пользователя

### Работа со смартфонами

- `GET /phones` - Получить список смартфонов (требует аутентификации)
- `GET /phones/search` - Поиск смартфонов по запросу (RAG-система)
- `POST /phones` - Добавить новый смартфон (админ)
- `PUT /phones/{id}` - Обновить информацию о смартфоне (админ)
- `DELETE /phones/{id}` - Удалить смартфон (админ)

## Примеры запросов

### Получение токена

```bash
curl -X POST "http://localhost:8000/token" \
-H "Content-Type: application/json" \
-d '{"username":"user","password":"password"}'
```

### Поиск смартфонов

```bash
curl -X GET "http://localhost:8000/phones/search?query=лучший смартфон с хорошей камерой" \
-H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Структура проекта

```
.
├── app/                  # Основное приложение FastAPI
│   ├── api/              # API endpoints
│   ├── core/             # Основная логика
│   ├── models/           # Pydantic и DB модели
│   ├── services/         # Сервисные классы
│   └── main.py           # Точка входа FastAPI
├── chroma_db/            # База данных ChromaDB
├── scripts/              # Скрипты для парсинга и инициализации
├── requirements.txt      # Зависимости
└── .env                  # Переменные окружения
```

## Используемые технологии

- **FastAPI** - веб-фреймворк для API
- **ChromaDB** - векторная база данных
- **LangChain** - работа с языковыми моделями
- **HuggingFace** - языковые модели и эмбеддинги
- **PyJWT** - аутентификация через JWT
- **BeautifulSoup/Scrapy** - парсинг данных (уточните, что использовали)

## Лицензия

[Укажите вашу лицензию, например MIT]

## Контакты

Ваше имя/контакты для связи по вопросам проекта
