# Обзор проекта
Сервис для обработки жалоб клиентов с интеграцией публичных API. Стек: FastAPI, SQLite, SQLalchemy, Docker, n8n.

Реализована функциональность создания жалоб через API. Кроме того, настроен воркфлоу в n8n, автоматизирующий
взаимодействие с Телеграм и Google Sheets. Демонстрацию работы можно увидеть на [скринкасте](https://disk.yandex.ru/i/iTA-K8W5_aldcA) (для иллюстрации Schedule Trigger в n8n отрабатывает каждые 45 сек, а не ежечасно).
Также реализована доп. проверка на спам:
[](https://github.com/David-Roklem/Screenshots_screencasts/raw/main/%D0%94%D0%BE%D0%BF%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%BD%D0%B0%20%D1%81%D0%BF%D0%B0%D0%BC%201.png)
[](https://github.com/David-Roklem/Screenshots_screencasts/raw/main/%D0%94%D0%BE%D0%BF%20%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%BD%D0%B0%20%D1%81%D0%BF%D0%B0%D0%BC%202.png)

## Начало работы
Склонируйте данный репозиторий командой:
```
https://github.com/David-Roklem/complaints_n8n_automation
```

### Зависимости
Зависимости проекта описаны в файлах pyproject.toml и requirements.txt.

### Docker
По примеру переменных окружения, указанных в файле .env.example, видоизмените их по необходимости

На компьютере должен быть установлен Docker. Чтобы запустить проект, вам необходимо (находясь в корне проекта) поднять контейнеры командой:
```
docker compose up -d
```

### Запуск
В браузере перейдите по адресу http://127.0.0.1:8001/docs, чтобы попасть в Swagger UI для взаимодействия с API.
По адресу http://127.0.0.1:5678/ находится панель управления n8n
