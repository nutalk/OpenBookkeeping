if [ -f "/data/db.sqlite3" ];then
    echo "file exist"
    else
    cp docker/db.sqlite3 /data
fi

python manage.py makemigrations
python manage.py migrate

# python manage.py makemessages -a
python manage.py compilemessages

python manage.py runserver 0.0.0.0:7788