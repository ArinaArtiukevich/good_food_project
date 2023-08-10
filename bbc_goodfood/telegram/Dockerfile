FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 4000

CMD ["python", "telegram_bot.py"]
