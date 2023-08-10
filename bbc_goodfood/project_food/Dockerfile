FROM python:slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader omw-1.4


COPY . .

EXPOSE 8000

CMD ["python", "fast_api.py"]
