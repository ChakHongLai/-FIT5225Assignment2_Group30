import boto3
import json

# Initialise the DynamoDB and the item existing identifier
database = boto3.resource('dynamodb')
itemIsExisted = True

def lambda_handler(event, context):
    even = json.loads(event)
    # GET user's adding query
    queryURL = even['url']
    # print(queryURL)
    addingTags = even['tags']
    # print(addingTags)
    
    # Initialise the LabelDetected database, the key will be user's query key
    table = database.Table('LabelDetected')
    response = table.get_item(
        Key = {
            'URL': queryURL
        }
    )

    # If user's query key matches one in the database, print the image URL and set the identifier to be True
    # If not, set the identifier to be False
    try:
        print('Tags will be added to: ', response['Item']['URL'])
        itemIsExisted = True
    except:
        itemIsExisted = False


    if itemIsExisted == True:
        # Adding user's tags to the original tags
        databaseItemTags = response['Item']['Tags']
        databaseItemTags.extend(addingTags)
        # print(databaseItemTags)
        
        # Update the item in DynamoDB
        table.update_item(
            Key = {
                'URL': queryURL
            },
            UpdateExpression = 'SET Tags = :val1',
            ExpressionAttributeValues = {
                ':val1' : databaseItemTags
            }
        )
        
        print('Updated item: ', response['Item'])
        return 'Extra tags are added to the image'
    else:
        print("Sorry, there is no such image in the database.")
    