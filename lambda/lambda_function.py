import json
import os
import uuid
import base64
import boto3

s3 = boto3.client('s3', endpoint_url=os.environ.get("AWS_ENDPOINT_URL"))
BUCKET = os.environ["S3_BUCKET"]

def lambda_handler(event, context):
    path = event.get("rawPath") or event.get("path")
    method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod")
    if path == "/start" and method == "POST":
        key = str(uuid.uuid4())
        resp = s3.create_multipart_upload(Bucket=BUCKET, Key=key)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"uploadId": resp["UploadId"], "key": key})
        }
    elif path == "/part" and method == "PUT":
        params = event.get("queryStringParameters") or {}
        upload_id = params.get("uploadId")
        part_number = int(params.get("partNumber"))
        key = params.get("key")
        body = base64.b64decode(event["body"]) if event.get("isBase64Encoded") else event["body"].encode()
        resp = s3.upload_part(Bucket=BUCKET, Key=key, UploadId=upload_id, PartNumber=part_number, Body=body)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"ETag": resp["ETag"]})
        }
    elif path == "/complete" and method == "POST":
        data = json.loads(event["body"])
        upload_id = data["uploadId"]
        key = data["key"]
        parts = [{"ETag": p["ETag"], "PartNumber": p["PartNumber"]} for p in data["parts"]]
        resp = s3.complete_multipart_upload(Bucket=BUCKET, Key=key, UploadId=upload_id, MultipartUpload={"Parts": parts})
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"location": resp.get("Location", "")})
        }
    elif path == "/latest" and method == "GET":
        objs = s3.list_objects_v2(Bucket=BUCKET).get("Contents", [])
        if not objs:
            return {"statusCode": 404, "headers": {"Access-Control-Allow-Origin": "*"}, "body": "No objects"}
        latest = max(objs, key=lambda o: o["LastModified"])
        obj = s3.get_object(Bucket=BUCKET, Key=latest["Key"])
        data = obj["Body"].read()
        return {
            "statusCode": 200,
            "isBase64Encoded": True,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/octet-stream",
                "Content-Disposition": f"attachment; filename={latest['Key']}"
            },
            "body": base64.b64encode(data).decode()
        }
    else:
        return {"statusCode": 404, "body": "Not Found", "headers": {"Access-Control-Allow-Origin": "*"}}
