# Multipart Upload Example

This repository demonstrates a Docker Compose setup with an Angular frontend and a Python backend. All S3 interactions are performed against [LocalStack](https://github.com/localstack/localstack) so no real AWS resources are required. Files are sent in 5&nbsp;MiB chunks through the backend which acts as an API Gateway/Lambda.

## Usage

1. Set the desired bucket name in `docker-compose.yml`.
2. Build and start the containers (this will also start LocalStack):

```bash
docker compose up --build
```

3. Once running, create the bucket inside LocalStack:

```bash
aws --endpoint-url http://localhost:4566 s3 mb s3://my-upload-bucket
```

4. Access the frontend at [http://localhost:4200](http://localhost:4200) and select a file to upload.

The backend exposes `/start`, `/part`, and `/complete` endpoints that map directly to S3's multipart upload API running in LocalStack.
