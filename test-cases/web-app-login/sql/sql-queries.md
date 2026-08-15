# SQL Queries – Pet Project

## Общая информация

- **Проект:** Web Application (учебный pet-проект)
- **Модуль:** База данных (пользователи, заказы, товары)
- **Дата:** 16.08.2026
- **Автор:** Shar Lodka
- **Инструменты:** SQL (PostgreSQL / MySQL / SQLite – указать нужное)

## Описание схемы 

В рамках учебного проекта рассматриваются следующие таблицы:

- `users` – пользователи
  - `id` (PK)
  - `email`
  - `name`
  - `created_at`

- `products` – товары
  - `id` (PK)
  - `name`
  - `price`
  - `category`

- `orders` – заказы
  - `id` (PK)
  - `user_id` (FK → users.id)
  - `status`
  - `created_at`

- `order_items` – позиции заказа
  - `id` (PK)
  - `order_id` (FK → orders.id)
  - `product_id` (FK → products.id)
  - `quantity`
  - `price`


---

## Примеры запросов

### 1. Получить всех пользователей

**Цель:** Проверить, что таблица `users` заполнена, и посмотреть базовые данные.

```sql
SELECT
    id,
    email,
    name,
    created_at
FROM users
ORDER BY created_at DESC;
```

**Что проверяется:**

- Наличие записей в таблице `users`.
- Корректность заполнения полей `email`, `name`.
- Сортировка по дате регистрации.

---

### 2. Получить заказы конкретного пользователя

**Цель:** Проверить связь `orders.user_id → users.id`.

```sql
SELECT
    o.id AS order_id,
    o.status,
    o.created_at,
    u.email AS user_email,
    u.name AS user_name
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE u.email = 'user@example.com'
ORDER BY o.created_at DESC;
```

**Что проверяется:**

- Корректность внешнего ключа `user_id`.
- Возможность получить все заказы по email пользователя.
- Корректность `JOIN` между `orders` и `users`.

---

### 3. Получить детали заказа с товарами

**Цель:** Проверить связь заказов с товарами через `order_items`.

```sql
SELECT
    o.id AS order_id,
    o.status,
    oi.quantity,
    oi.price AS item_price,
    p.name AS product_name,
    p.category
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON oi.product_id = p.id
WHERE o.id = 123;
```

**Что проверяется:**

- Корректность связей:
  - `orders → order_items`
  - `order_items → products`
- Наличие всех позиций заказа.
- Корректность цен и названий товаров.

---

### 4. Посчитать общую сумму заказа

**Цель:** Проверить бизнес-логику расчёта суммы заказа.

```sql
SELECT
    o.id AS order_id,
    SUM(oi.quantity * oi.price) AS total_amount
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.id = 123
GROUP BY o.id;
```

**Что проверяется:**

- Корректность расчёта: `quantity * price` по всем позициям.
- Использование агрегатной функции `SUM`.
- Группировка по заказу (`GROUP BY`).

---

### 5. Получить топ-5 самых дорогих товаров

**Цель:** Проверить сортировку и ограничение количества строк.

```sql
SELECT
    id,
    name,
    price,
    category
FROM products
ORDER BY price DESC
LIMIT 5;
```

**Что проверяется:**

- Сортировка по цене (`ORDER BY price DESC`).
- Ограничение вывода (`LIMIT 5`).
- Корректность полей в выборке.

---

### 6. Посчитать количество заказов по статусам

**Цель:** Проверить агрегацию и группировку.

```sql
SELECT
    status,
    COUNT(*) AS orders_count
FROM orders
GROUP BY status
ORDER BY orders_count DESC;
```

**Что проверяется:**

- Группировка по полю `status`.
- Подсчёт количества заказов в каждом статусе.
- Сортировка по количеству.

---

### 7. Найти пользователей без заказов

**Цель:** Проверить работу с `LEFT JOIN` и `NULL`.

```sql
SELECT
    u.id,
    u.email,
    u.name
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE o.id IS NULL;
```

**Что проверяется:**

- Корректность `LEFT JOIN`.
- Фильтрация пользователей, у которых нет ни одного заказа.
- Понимание разницы между `INNER JOIN` и `LEFT JOIN`.

---

## Как это использовалось в тестировании

- Проверка целостности данных после действий в UI (регистрация, создание заказа и т.д.).
- Сверка данных, отображаемых в интерфейсе, с данными в БД.
- Проверка бизнес-правил (сумма заказа, наличие товаров, статусы).
- Поиск аномалий: дубли, отсутствующие связи, некорректные суммы.
