if [ -f "/data/db.sqlite3" ];then
    echo "file exist"
    else
    cp docker/db.sqlite3 /data
fi

python manage.py runserver 0.0.0.0:7788