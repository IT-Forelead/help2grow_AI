FROM python:3.10-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
RUN pip install -U pip setuptools wheel
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm
COPY . .
EXPOSE 5000
ENV FLASK_APP=run.py
CMD ["flask", "run", "--host", "0.0.0.0"]