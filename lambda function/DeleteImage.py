import json
import boto3

s3_client = boto3.client("s3")
s3 = boto3.resource("s3")
database = boto3.resource('dynamodb')
itemIsExisted = True

def lambda_handler(event, context):
    even = json.loads(event)
    userURL = even["url"]
    
# -----------------For DynamoDB-----------------
    
    # Query the DynamoDB to find the image
    table = database.Table('LabelDetected')
    # Find image by user's query URL
    response = table.get_item(
        Key = {
            'URL': userURL
        }
    )

    # If this image exists, then print it, and set the identifier to True
    # If it does not exist, catch the error and set the identifier to False
    try:
        print('This image exists in the DynamoDB', response['Item']['URL'])
        itemIsExisted = True
    except:
        print('This image does not exist in the DynamoDB')
        itemIsExisted = False
    
    # Call delete_item method to delete this item from DynamoDB
    if itemIsExisted == True:
        table.delete_item(
            Key={
                'URL': userURL
            }
        )
        print("Item is deleted")
    else:
        print("No item is deleted")
    
# -----------------For Amazon S3-----------------

    # Loop over all URLs in the S3 bucket
    bucket = 'fit5225-a2-s3-bucket'

    list = s3_client.list_objects(Bucket = bucket)['Contents']
    for s3_key in list:
        imageInS3 = 'https://fit5225-a2-s3-bucket.s3.amazonaws.com/' + s3_key['Key']
        # print(imageInS3)
        
        if userURL == imageInS3:
            s3.Object(bucket, s3_key['Key']).delete()
        else:
            print("User's query does not match this image.")
        