"""
This program is a part of "FIT5225 Cloud Computing and Security - A2 TagTag", a serverless demo. The whole project is composed of a client-side UI and a set of AWS cloud resources including aws-s3, dynamo, lambda, aws-api-gateway, aws-cognito. This program functions as a command-line interface interacting with aws-cognito and aws-api-gateway.

Author@Xicheng Wang
Email:xwan0255@student.monash.edu
"""
#!/bin/bash

import uuid
import requests
import json
import os
import base64
import glob



def list_images():

    image_list=[]
    for filepath in glob.iglob(os.path.dirname(__file__)+"/upload/"+"*.jpg"):
        image_list.append(os.path.basename(filepath))

    return image_list



def upload_image(image_name, id_token):

    try:
        #prepare request url
        api=r"https://620t1q00e4.execute-api.us-east-1.amazonaws.com/prod/api/uploadimage" 

        #prepare request dt
        dt={}
        image_path=os.path.dirname(__file__)+"/upload/"+image_name
        with open (image_path, 'rb') as image_file:
            dt['image'] =  base64.b64encode(image_file.read()).decode('utf-8')
        dt ['id'] = str(uuid.uuid5(uuid.NAMESPACE_OID, image_name))


        #prepare request headers
        headers={
            "Content-Type":"application/json",
            "auth":id_token
        }

        resp = requests.post(url=api, json= json.dumps(dt), headers = headers)

        return resp.text
    
    except Exception as e:
        print("Exception  {}".format(e))


