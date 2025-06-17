#!/bin/sh
set -e
AWS="aws --endpoint-url=http://localstack:4566 --region us-east-1"

# wait for LocalStack to be ready
until $AWS s3 ls >/dev/null 2>&1; do
  echo "Waiting for LocalStack..."
  sleep 2
done

$AWS s3api create-bucket --bucket "$S3_BUCKET" || true
mkdir -p /tmp/lambda
cp /lambda/lambda_function.py /tmp/lambda/
cd /tmp/lambda
zip function.zip lambda_function.py
$AWS lambda create-function --function-name uploader \
  --runtime python3.12 --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --role arn:aws:iam::000000000000:role/lambda-role \
  --environment Variables="{AWS_ENDPOINT_URL=http://localstack:4566,S3_BUCKET=$S3_BUCKET}" || true

api_id=$($AWS apigatewayv2 create-api --name uploader-api --protocol-type HTTP --target arn:aws:lambda:us-east-1:000000000000:function:uploader --route-key 'ANY /{proxy+}' --query 'ApiId' --output text)

$AWS lambda add-permission --function-name uploader \
  --statement-id apigw \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn arn:aws:execute-api:us-east-1:000000000000:$api_id/*/*/* || true

$AWS apigatewayv2 create-stage --api-id $api_id --stage-name prod --auto-deploy

mkdir -p /config
echo http://localstack:4566/restapis/$api_id/prod/_user_request_ > /config/api_url
