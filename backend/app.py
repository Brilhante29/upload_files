from flask import Flask, request, jsonify
import boto3
import uuid
import os

app = Flask(__name__)

endpoint = os.environ.get('AWS_ENDPOINT_URL')
s3 = boto3.client('s3', endpoint_url=endpoint) if endpoint else boto3.client('s3')
BUCKET = os.environ.get('S3_BUCKET')

def ensure_bucket(name: str):
    try:
        s3.head_bucket(Bucket=name)
    except Exception:
        s3.create_bucket(Bucket=name)

ensure_bucket(BUCKET)

@app.route('/start', methods=['POST'])
def start_upload():
    key = str(uuid.uuid4())
    response = s3.create_multipart_upload(Bucket=BUCKET, Key=key)
    upload_id = response['UploadId']
    return jsonify({'uploadId': upload_id, 'key': key})

@app.route('/part', methods=['PUT'])
def upload_part():
    upload_id = request.args.get('uploadId')
    key = request.args.get('key')
    part_number = int(request.args.get('partNumber'))
    resp = s3.upload_part(
        Bucket=BUCKET,
        Key=key,
        UploadId=upload_id,
        PartNumber=part_number,
        Body=request.data
    )
    return jsonify({'ETag': resp['ETag']})

@app.route('/complete', methods=['POST'])
def complete_upload():
    data = request.get_json()
    upload_id = data['uploadId']
    key = data['key']
    parts = [{'ETag': p['ETag'], 'PartNumber': p['PartNumber']} for p in data['parts']]
    result = s3.complete_multipart_upload(
        Bucket=BUCKET,
        Key=key,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )
    return jsonify({'location': result.get('Location', '')})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
