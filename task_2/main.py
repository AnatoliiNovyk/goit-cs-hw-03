from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Підключення до MongoDB Atlas
# Замініть <username>, <password> та <cluster-url> на ваші дані
MONGO_URI = "mongodb+srv://goitlearn:Pa55W0rd@goit-cluster.8wulc7w.mongodb.net/?retryWrites=true&w=majority&appName=GOIT-Cluster"

try:
    client = MongoClient(MONGO_URI)
    # Перевірка з'єднання
    client.admin.command('ping')
    print("Підключення до MongoDB успішне.")
    db = client.cats_db
    collection = db.cats
except ConnectionFailure as e:
    print(f"Не вдалося підключитися до MongoDB: {e}")
    exit()

def create_cat(name, age, features):
    """Створює новий запис про кота."""
    try:
        result = collection.insert_one({
            "name": name,
            "age": age,
            "features": features
        })
        print(f"Кіт '{name}' доданий з id: {result.inserted_id}")
    except OperationFailure as e:
        print(f"Помилка при додаванні кота: {e}")

def read_all_cats():
    """Виводить всі записи з колекції."""
    try:
        for cat in collection.find():
            print(cat)
    except OperationFailure as e:
        print(f"Помилка при читанні даних: {e}")

def read_cat_by_name(name):
    """Знаходить та виводить інформацію про кота за ім'ям."""
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except OperationFailure as e:
        print(f"Помилка при пошуку кота: {e}")

def update_cat_age(name, new_age):
    """Оновлює вік кота за ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота '{name}' оновлено.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений або вік вже є {new_age}.")
    except OperationFailure as e:
        print(f"Помилка при оновленні віку кота: {e}")

def add_feature_to_cat(name, feature):
    """Додає нову характеристику коту за ім'ям."""
    try:
        result = collection.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.modified_count > 0:
            print(f"Характеристику '{feature}' додано коту '{name}'.")
        else:
            print(f"Кіт з ім'ям '{name}' не знайдений або характеристика вже існує.")
    except OperationFailure as e:
        print(f"Помилка при додаванні характеристики: {e}")

def delete_cat_by_name(name):
    """Видаляє запис про кота за ім'ям."""
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Запис про кота '{name}' видалено.")
        else:
            print(f"Кота з ім'ям '{name}' не знайдено.")
    except OperationFailure as e:
        print(f"Помилка при видаленні кота: {e}")

def delete_all_cats():
    """Видаляє всі записи з колекції."""
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} записів.")
    except OperationFailure as e:
        print(f"Помилка при видаленні всіх записів: {e}")

if __name__ == "__main__":
    # Приклад використання функцій:
    # create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    # create_cat("murka", 5, ["любить спати", "їсть рибу"])
    print("Всі коти:")
    read_all_cats()
    # print("\nІнформація про кота 'barsik':")
    # read_cat_by_name("barsik")
    # update_cat_age("barsik", 4)
    # add_feature_to_cat("barsik", "любить спати на сонці")
    # delete_cat_by_name("barsik")
    # delete_cat_by_name("murka")
    delete_all_cats()
