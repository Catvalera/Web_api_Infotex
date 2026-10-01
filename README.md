# Web API на Python (FastAPI)

Порт проекта `Web_api_Csharp` (ASP.NET Core + EF Core) на **FastAPI + SQLAlchemy (async) + Alembic**.

## Структура

```
app/
  main.py                    — точка входа, Swagger (аналог Program.cs)
  config.py                  — настройки, строка подключения (аналог appsettings.json)
  database.py                — движок и сессии БД (аналог Data/AppDbContext.cs)
  models.py                  — таблицы Values и Results (аналог Models/*.cs)
  schemas.py                 — схемы ответов (JSON в camelCase, как в ASP.NET)
  services/csv_processing.py — разбор и валидация CSV, расчёт агрегатов
  routers/
    upload_and_read.py       — Upload_and_readController
    filter_data.py           — Filter_dataController
    last_ten_values.py       — Last_ten_valuesController
    table_actions.py         — Table_actionsController
alembic/                     — миграции (аналог Migrations/)
tests/                       — автотесты (pytest)
Tests data files/            — тестовые CSV
```

## Запуск

Нужны Python 3.11+ и PostgreSQL.

1. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate    Linux/macOS: source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Запустите PostgreSQL и создайте базу `timescale_db` (например, в pgAdmin 4 или командой `createdb -U postgres timescale_db`).
3. Скопируйте `.env.example` в `.env` и при необходимости поправьте строку подключения:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/timescale_db
   ```
4. Создайте таблицы (аналог `dotnet ef database update`):
   ```bash
   alembic upgrade head
   ```
   В pgAdmin в `timescale_db/Schemas/public/Tables` появятся таблицы `Values` и `Results`.
5. Запустите API:
   ```bash
   uvicorn app.main:app --reload --port 5145
   ```
6. Откройте Swagger: http://localhost:5145/swagger

## Эндпоинты

| Раздел | Метод и путь | Параметры | Что делает |
|---|---|---|---|
| Upload_and_read | `POST /Upload_file` | `file` (CSV) | Загружает CSV, пишет строки в `Values` и итог в `Results`. Повторная загрузка файла с тем же именем заменяет его данные |
| Upload_and_read | `GET /Get_data_from_table_Value` | — | Все строки таблицы `Values` |
| Upload_and_read | `GET /Get_data_from_table_Result` | — | Все строки таблицы `Results` |
| Filter_data | `GET /Sort_by_filename` | `name` | Результаты, где имя файла содержит `name` |
| Filter_data | `GET /Sort_by_StartDate` | `startdate`, `enddate` (YYYY-mm-dd) | Результаты с датой старта в диапазоне (включительно) |
| Filter_data | `GET /Sort_by_avg-Value` | `startValue`, `endValue` | Фильтр по среднему значению |
| Filter_data | `GET /Sort_by_avg-ExecutionTime` | `startValue`, `endValue` | Фильтр по среднему времени выполнения |
| Last_ten_values | `GET /Get_last_10_values_filter_from_filename` | `Full_filename` | 10 последних результатов по имени файла, отсортированные по дате старта |
| Table_actions | `DELETE /api/Table_actions/clear_table_Value` | — | Очищает `Values` и сбрасывает счётчик Id |
| Table_actions | `DELETE /api/Table_actions/clear_table_Result` | — | Очищает `Results` и сбрасывает счётчик Id |

## Формат CSV и валидация

```
Date;ExecutionTime;Value
2025-08-03T10:15:30.0000Z;2.5;45.7
```

- расширение `.csv`, кодировка UTF-8, разделитель `;`, первая строка — заголовок;
- строк данных больше 1 и меньше 10 000;
- дата не раньше 2000-01-01 и не позже начала текущих суток (UTC);
- `ExecutionTime` и `Value` — неотрицательные числа с точкой в качестве разделителя.

Если любая строка не проходит проверку, файл не сохраняется и возвращается `400 Error validation!` с указанием строки и причины.

## Тесты

Тестам нужна отдельная база `timescale_db_test` (она пересоздаётся при каждом запуске):

```bash
createdb -U postgres timescale_db_test
pip install -r requirements-dev.txt
pytest
```

Другую строку подключения можно задать переменной `TEST_DATABASE_URL`.
