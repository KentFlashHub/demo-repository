### FlashHub FlashCard

### Install
pip install -r requirements.txt
python manage.py migrate

### Change secret_Key
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())

- Copy the key into setting.py

### Run
python manage.py runserver

### Download Sqlite in Extension
run shift+command+p to open db.sqlite
run sqlite3 db.sqlite3 (to enter sql query)

Example:
BEGIN TRANSACTION;
DELETE FROM flashcards_flashcard;
COMMIT;

