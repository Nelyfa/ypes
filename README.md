# ypes - Зеркальное отображение текста

🔄 Docker-приложение для зеркального отображения текста, работающее на порту 1.

## 📋 Описание

Приложение `ypes` предназначено для зеркального отображения текста. Например, текст "привет" становится "тевирп". Приложение предоставляет как веб-интерфейс, так и REST API.

## 🚀 Быстрая установка

### Предварительные требования

- Docker (НЕ docker.io)
- curl (для проверки работоспособности)

### Установка в один клик

```bash
chmod +x setup.sh
./setup.sh
```

Скрипт автоматически:
- Проверит наличие Docker
- Соберет Docker образ
- Запустит контейнер на порту 1
- Проверит работоспособность приложения

## 🔧 Ручная установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Nelyfa/ypes.git
cd ypes
```

### 2. Сборка Docker образа

```bash
docker build -t ypes-mirror .
```

### 3. Запуск контейнера

```bash
docker run -d --name ypes-mirror-app -p 1:1 ypes-mirror
```

Или с помощью docker-compose:

```bash
docker-compose up -d
```

## 🌐 Использование

### Веб-интерфейс

Откройте в браузере: http://localhost:1

### REST API

#### POST запрос

```bash
curl -X POST http://localhost:1/api/mirror \
  -H "Content-Type: application/json" \
  -d '{"text": "привет мир"}'
```

Ответ:
```json
{
  "original": "привет мир",
  "mirrored": "рим тевирп",
  "length": 10,
  "status": "success"
}
```

#### GET запрос

```bash
curl "http://localhost:1/api/mirror?text=привет+мир"
```

### Health Check

```bash
curl http://localhost:1/health
```

## 📁 Структура проекта

```
ypes/
├── app.py              # Основное приложение Flask
├── requirements.txt    # Python зависимости
├── Dockerfile         # Docker конфигурация
├── docker-compose.yml # Docker Compose конфигурация
├── setup.sh          # Скрипт автоматической установки
└── README.md         # Документация
```

## 🔧 Управление контейнером

### Просмотр логов

```bash
docker logs ypes-mirror-app
```

### Остановка приложения

```bash
docker-compose down
# или
docker stop ypes-mirror-app
```

### Перезапуск

```bash
docker-compose restart
# или
docker restart ypes-mirror-app
```

### Проверка статуса

```bash
docker ps | grep ypes
```

## 🛠️ Разработка

### Локальный запуск без Docker

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Запустите приложение:
```bash
python app.py
```

### Переменные окружения

- `PORT` - порт для запуска приложения (по умолчанию: 1)

## 🐛 Устранение неполадок

### Порт 1 занят

Если порт 1 занят другим приложением:

```bash
# Найти процесс, использующий порт 1
sudo lsof -i :1

# Остановить процесс (замените PID на реальный)
sudo kill -9 PID
```

### Проблемы с правами доступа

```bash
# Добавить пользователя в группу docker
sudo usermod -aG docker $USER

# Перелогиниться или выполнить
newgrp docker
```

### Контейнер не запускается

```bash
# Просмотр подробных логов
docker logs ypes-mirror-app

# Проверка образа
docker images | grep ypes

# Пересборка образа
docker-compose build --no-cache
```

## 📊 Примеры использования

### Зеркальное отображение русского текста

Вход: `"Привет, как дела?"`
Выход: `"?алед как ,тевирП"`

### Зеркальное отображение английского текста

Вход: `"Hello, World!"`
Выход: `"!dlroW ,olleH"`

### Зеркальное отображение чисел

Вход: `"12345"`
Выход: `"54321"`

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 📞 Поддержка

- 🐛 Сообщить об ошибке: [Issues](https://github.com/Nelyfa/ypes/issues)
- 💡 Предложить улучшение: [Discussions](https://github.com/Nelyfa/ypes/discussions)
- 📧 Email: support@ypes.dev

## 🏷️ Версии

- **v1.0.0** - Первый релиз с базовой функциональностью зеркального отображения текста

---

Сделано с ❤️ для сообщества разработчиков