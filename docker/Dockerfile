FROM python:3.7-slim
LABEL author="Hiip Asia - DE"
LABEL service="Collectin service"
WORKDIR /app
COPY . .
RUN pip install -U pip
RUN pip install -r requirements.txt
CMD python main.py