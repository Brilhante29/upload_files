# Multipart Upload Example

This project demonstrates an Angular frontend uploading files to S3 using multipart uploads.
Everything runs locally with Docker Compose and [LocalStack](https://github.com/localstack/localstack).
The frontend talks to an API Gateway which invokes a Lambda function that streams the file parts to S3.
No real AWS resources are required.

## Usage

1. Edit `docker-compose.yml` if you want a different bucket name.
2. Start the stack:

```bash
docker compose up --build
```

3. When the services are up, open [http://localhost:4200](http://localhost:4200) and choose a file to upload.

The Lambda function exposes `/start`, `/part`, and `/complete` paths through API Gateway and writes the
uploaded object to the configured S3 bucket in 5&nbsp;MiB parts.
