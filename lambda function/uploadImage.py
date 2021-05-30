import json
import boto3
import base64

s3_client = boto3.client("s3")
s3 = boto3.resource("s3")
bucket = s3.Bucket('fit5225-a2-s3-bucket')

def lambda_handler(event, context):
    even = json.loads(event)
    image = even['image']
    # print(image)
    decoded = base64.b64decode(image)
    # print(decoded)
    
    key = even['id'] + '.jpg'

    bucket.put_object(Key = key, Body = decoded, ContentType = 'image/jpeg', ACL = 'public-read')
    
    return {
        'status': 'True',
        'statusCode': 200,
        'body': 'Image Uploaded'
      }