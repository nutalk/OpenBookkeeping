FROM python:3.11
WORKDIR /usr/src/app

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY . .
RUN mkdir /data
COPY empty.sqlite3 /data
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:7788", "--settings", "bookkeep.settings.docker"]