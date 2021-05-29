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



#return all images in aws-s3
def get_all_images(id_token):

    try:
        #prepare request url
        api=r"https://620t1q00e4.execute-api.us-east-1.amazonaws.com/prod/api/findimagebytags" 

        #prepare request dt
        dt={} 
        dt["tags"]=[]
        
        #prepare request headers
        headers={
            "Content-Type":"application/json",
            "auth":id_token
        }

        resp = requests.post(url=api, json= json.dumps(dt), headers = headers)

        json_obj=json.loads(json.loads(resp.text))

        return json_obj["links"]
    
    except Exception as e:
        print("Exception  {}".format(e))



def seek_images_by_tags(tags, id_token):

    try:
        #prepare request url
        api=r"https://620t1q00e4.execute-api.us-east-1.amazonaws.com/prod/api/findimagebytags" 

        #prepare request dt
        dt={} 
        dt["tags"]=tags
        
        #prepare request headers
        headers={
            "Content-Type":"application/json",
            "auth":id_token
        }

        resp = requests.post(url=api, json= json.dumps(dt), headers = headers)

        json_obj=json.loads(json.loads(resp.text))

        # as per spec, the response json should follow {"links":[url1, url2, url3,..]}
        return json_obj["links"]
    
    except Exception as e:
        print("Exception  {}".format(e))



def seek_images_by_image(image_name, id_token):

    try:
        #prepare request url
        api=r"https://620t1q00e4.execute-api.us-east-1.amazonaws.com/prod/api/findimagebyimage" 

        #prepare request dt
        dt={}
        i_path=os.path.dirname(__file__)+"/upload/"+image_name
        with open (i_path, 'rb') as image_file:
            dt['image'] =  base64.b64encode(image_file.read()).decode('utf-8')
        dt['id'] = str(uuid.uuid5(uuid.NAMESPACE_OID, image_name))

        #prepare request headers
        headers={
            "Content-Type":"application/json",
            "auth":id_token
        }

        resp = requests.post(url=api, json= json.dumps(dt), headers = headers)

        json_obj=json.loads(json.loads(resp.text))

        return json_obj["links"]
    
    except Exception as e:
        print("Exception  {}".format(e))



def add_tags_to(tags, image_url, id_token):

    try:
        #prepare request url
        api=r"https://620t1q00e4.execute-api.us-east-1.amazonaws.com/prod/api/updateextratags"

        #prepare request dt
        dt={} 
        dt["url"]=image_url
        dt["tags"]=tags
        
        #prepare request headers
        headers={
            "Content-Type":"application/json",
            "auth":id_token
        }

        resp = requests.post(url=api, json= json.dumps(dt), headers = headers)

        return resp.text
    
    except Exception as e:
        print("Exception  {}".format(e))



def delete_image(image_url, id_token):

    try:
        #prepare request url
        api=r"https://620t1q00e4.execute-api.us-east-1.amazonaws.com/prod/api/deleteimage"

        #prepare request dt
        dt={}
        dt["url"]=image_url
        
        #prepare request headers
        headers={
            "Content-Type":"application/json",
            "auth":id_token
        }

        resp = requests.post(url=api, json= json.dumps(dt), headers = headers)

        return resp.text
    
    except Exception as e:
        print("Exception  {}".format(e))



