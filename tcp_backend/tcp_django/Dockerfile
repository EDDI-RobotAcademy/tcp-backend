FROM python:3.12

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential
#     libmysqlclient-dev \
#     pkg-config
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /app/wait-for-it.sh
COPY . /app/

RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/manage.py

# 환경 변수 설정
ENV PYTHONUNBUFFERED 1

CMD ["/app/wait-for-it.sh", "db:3306", "--", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]