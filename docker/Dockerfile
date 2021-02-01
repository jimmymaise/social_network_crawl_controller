FROM python:3.7-slim
LABEL author="Hiip Asia - DE"
LABEL service="Comment service"
LABEL social-network="Facebook"
ENV AM_BASE_URL=http://34.219.102.184:9099/
ENV MONGODB_HOST=172.31.58.208
ENV MONGODB_PORT=27017
ENV MONGODB_DB=facebook
ENV MONGODB_USER=bigdatateam
ENV MONGODB_PASS=superbighiipasia
ENV LAMBDA_BASE_URL=https://1bidkl51r1.execute-api.us-west-2.amazonaws.com/fb/post-comments
ENV LAMBDA_X_API_KEY_POST_DETAIL=gRsge79XJIaoJUNDGEY4g5aQFuylUtswaAQCx8ZT
ENV SLACK_NOTIFICATION_URL=https://hooks.slack.com/services/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
ENV PROCESS_SLEEP_INTERVAL=5
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD python main.py