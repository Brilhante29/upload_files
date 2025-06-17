FROM python:3.12-slim
RUN pip install awscli awscli-local
RUN apt-get update && apt-get install -y zip && rm -rf /var/lib/apt/lists/*
COPY setup.sh /setup.sh
COPY lambda/lambda_function.py /lambda/lambda_function.py
CMD ["sh", "/setup.sh"]
