import psycopg2
from faker import Faker
import random

# Ініціалізація Faker
fake = Faker()

# Підключення до бази даних PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="task_manager",
        user="postgres",
        password="mysecretpassword",
        host="localhost"
    )
    cur = conn.cursor()

    # Додавання статусів
    statuses = [('new',), ('in progress',), ('completed',)]
    cur.executemany("INSERT INTO status (name) VALUES (%s)", statuses)
    print("Статуси додано.")

    # Додавання користувачів
    users = []
    for _ in range(10):  # Створимо 10 користувачів
        users.append((fake.name(), fake.email()))
    cur.executemany("INSERT INTO users (fullname, email) VALUES (%s, %s)", users)
    print("Користувачів додано.")

    # Отримання id користувачів та статусів
    cur.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT id FROM status")
    status_ids = [row[0] for row in cur.fetchall()]

    # Додавання завдань
    tasks = []
    for _ in range(30):  # Створимо 30 завдань
        tasks.append((
            fake.sentence(nb_words=4),
            fake.text(),
            random.choice(status_ids),
            random.choice(user_ids)
        ))
    cur.executemany("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", tasks)
    print("Завдання додано.")

    # Збереження змін
    conn.commit()

except psycopg2.Error as e:
    print(f"Помилка бази даних: {e}")
    conn.rollback()
finally:
    # Закриття з'єднання
    cur.close()
    conn.close()
    print("З'єднання з базою даних закрито.")
