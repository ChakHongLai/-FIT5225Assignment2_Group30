import json
import boto3

# Initialise the database and imageURL list
database = boto3.resource('dynamodb')

def lambda_handler(event, context):
    imageURL = []
    # Receive user's query JSON
    even = json.loads(event)
    queryTags = even['tags'] 
    table = database.Table('LabelDetected')

    response = table.scan()
    dbdata = response['Items']

    # Loop over the database items
    for index, element in enumerate(dbdata):
        
        url = element['URL']
        tags = element['Tags']
        imageInDatabase = set(tags)
        # print(imageInDatabase)
        # print(url)
        
        queryFromUser = set(queryTags)
        # print(queryFromUser)
        # print(queryTags)
        
        # If user's query match one image's JSON object, append this image to the list
        # If user's query input is an empty list, then ALL url in the database will be returned
        # if queryFromUser == imageInDatabase:
        #     imageURL.append(url)
        
        if len(queryTags) == 0:
            imageURL.append(url)
        else:
            if queryFromUser == imageInDatabase:
                imageURL.append(url)
    

    
    result = {"links": imageURL}
    jsonResult = json.dumps(result)
    
    return jsonResult