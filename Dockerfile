FROM python:3.11
WORKDIR /usr/src/app
RUN apt update
RUN apt install -y gettext 
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
COPY . .
RUN mkdir /data
ENTRYPOINT ["bash", "docker/init_run.sh"]