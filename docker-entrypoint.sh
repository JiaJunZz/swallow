#!/bin/sh
set -e
python manage.py makemigrations
python manage.py migrate
sleep 30
u=`echo "from django.contrib.auth import get_user_model; User = get_user_model(); u = len(User.objects.filter(username='admin')); print(u)" | python manage.py shell`
if [ "$u" -eq 0 ]
then
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin','admin@admin.com','admin123456')" | python manage.py shell
fi
celery multi start w1 -A swallow -B -l info
python manage.py runserver 0.0.0.0:8000
