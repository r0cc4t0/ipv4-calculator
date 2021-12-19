FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN python3 -m venv ipv4_venv

RUN . ipv4_venv/bin/activate

RUN pip install -U pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]
