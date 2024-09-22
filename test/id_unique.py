from random import randint
from extras.config import load_database


def unique_id_generator(retries=3, delay=5):
    db = load_database(retries, delay)
    cursor = db.cursor()
    cursor.execute("SELECT id FROM report")
    ids = cursor.fetchall()
    new_id = randint(1111111111111111, 9999999999999999)
    if new_id not in [row[0] for row in ids]:
        return new_id

new_id = unique_id_generator()
print(new_id)
