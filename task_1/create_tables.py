import psycopg2

def create_tables():
    """Створює таблиці users, status, та tasks у базі даних PostgreSQL."""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS status (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            status_id INTEGER,
            user_id INTEGER,
            FOREIGN KEY (status_id) REFERENCES status (id),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        );
        """
    )
    conn = None
    try:
        # Підключення до бази даних PostgreSQL
        conn = psycopg2.connect(
            dbname="task_manager", 
            user="postgres", 
            password="Pa55W0rd", 
            host="localhost"
        )
        cur = conn.cursor()
        # Створення таблиць
        for command in commands:
            cur.execute(command)
        # Збереження змін
        conn.commit()
        cur.close()
        print("Таблиці успішно створено.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_tables()
