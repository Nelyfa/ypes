#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода цветного текста
print_color() {
    printf "${1}${2}${NC}\n"
}

# Функция для проверки успешности команды
check_command() {
    if [ $? -eq 0 ]; then
        print_color $GREEN "✅ $1 выполнено успешно"
    else
        print_color $RED "❌ Ошибка при выполнении: $1"
        exit 1
    fi
}

print_color $BLUE "🐳 Установка Docker приложения ypes - Зеркальное отображение текста"
print_color $BLUE "📦 Репозиторий: https://github.com/Nelyfa/ypes"
echo ""

# Проверка наличия Docker
print_color $YELLOW "🔍 Проверка наличия Docker..."
if ! command -v docker &> /dev/null; then
    print_color $RED "❌ Docker не найден! Пожалуйста, установите Docker сначала."
    print_color $YELLOW "Инструкция по установке: https://docs.docker.com/get-docker/"
    exit 1
fi
print_color $GREEN "✅ Docker найден"

# Проверка наличия docker-compose
print_color $YELLOW "🔍 Проверка наличия docker-compose..."
if ! command -v docker-compose &> /dev/null; then
    print_color $YELLOW "⚠️  docker-compose не найден, используем docker compose"
    COMPOSE_CMD="docker compose"
else
    COMPOSE_CMD="docker-compose"
    print_color $GREEN "✅ docker-compose найден"
fi

# Остановка и удаление существующих контейнеров
print_color $YELLOW "🛑 Остановка существующих контейнеров..."
$COMPOSE_CMD down --remove-orphans 2>/dev/null
docker stop ypes-mirror-app 2>/dev/null
docker rm ypes-mirror-app 2>/dev/null
print_color $GREEN "✅ Очистка завершена"

# Сборка Docker образа
print_color $YELLOW "🔨 Сборка Docker образа..."
$COMPOSE_CMD build --no-cache
check_command "Сборка образа"

# Запуск контейнера
print_color $YELLOW "🚀 Запуск приложения..."
$COMPOSE_CMD up -d
check_command "Запуск контейнера"

# Ожидание запуска приложения
print_color $YELLOW "⏳ Ожидание запуска приложения..."
sleep 5

# Проверка статуса контейнера
print_color $YELLOW "🔍 Проверка статуса контейнера..."
if docker ps | grep -q "ypes-mirror-app"; then
    print_color $GREEN "✅ Контейнер запущен успешно"
else
    print_color $RED "❌ Ошибка запуска контейнера"
    print_color $YELLOW "📋 Логи контейнера:"
    docker logs ypes-mirror-app
    exit 1
fi

# Проверка доступности приложения
print_color $YELLOW "🌐 Проверка доступности приложения..."
sleep 3
if curl -s http://localhost:1/health > /dev/null; then
    print_color $GREEN "✅ Приложение доступно"
else
    print_color $YELLOW "⚠️  Приложение может быть еще не готово, проверьте через несколько секунд"
fi

echo ""
print_color $GREEN "🎉 Установка завершена успешно!"
echo ""
print_color $BLUE "📋 Информация о приложении:"
print_color $BLUE "   🌐 Веб-интерфейс: http://localhost:1"
print_color $BLUE "   🔗 API endpoint: http://localhost:1/api/mirror"
print_color $BLUE "   ❤️  Health check: http://localhost:1/health"
print_color $BLUE "   📦 Репозиторий: https://github.com/Nelyfa/ypes"
echo ""
print_color $YELLOW "🔧 Полезные команды:"
print_color $YELLOW "   Просмотр логов: docker logs ypes-mirror-app"
print_color $YELLOW "   Остановка: $COMPOSE_CMD down"
print_color $YELLOW "   Перезапуск: $COMPOSE_CMD restart"
print_color $YELLOW "   Статус: docker ps | grep ypes"
echo ""
print_color $GREEN "🚀 Приложение готово к использованию!"