### FlashHub FlashCard

### Install
- pip install -r requirements.txt
- python3 manage.py makemigrations
- python manage.py migrate


### Change secret_Key
from django.core.management.utils import get_random_secret_key

print(get_random_secret_key())

- Copy the key into `.env` file based on `.env.example`

- Acquire google oauth 2 credentials based on ```https://support.google.com/cloud/answer/6158849?hl=en```

- Copy the credentials to the `.env` too based on the `.env.example` file.

### Run
python manage.py runserver
