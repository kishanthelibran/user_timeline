import os
import boto3
from botocore.config import Config
import base64
from datetime import datetime
import hashlib
from datetime import datetime
#from .settings import ACCESS_KEY_ID
from .config_aws import (
    AWS_UPLOAD_BUCKET,
    AWS_UPLOAD_REGION,
    AWS_UPLOAD_ACCESS_KEY_ID,
    AWS_UPLOAD_SECRET_KEY
)

def fetch_media(user_id,postlist):
    config = Config(s3={"use_accelerate_endpoint": True})
    session = boto3.session.Session(aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID,
                                        aws_secret_access_key=AWS_UPLOAD_SECRET_KEY,
                                        region_name="us-east-1")
    client = session.client('s3',
                                config=config)
    s3 = session.resource('s3',
                                config=config)
    bucket_name = s3.Bucket("upload-users-post")
    post_media = dict()
    for id in postlist:
        response = client.list_objects_v2(
            Bucket=bucket_name.name,
            Prefix=str(user_id) + "/" + id + "/",
            MaxKeys=5)
        responselist = response['Contents']
        length = len(responselist)
        piclist = []
        for pics in range(1, length):
            pic_path = responselist[pics]['Key']
            body = client.get_object(Bucket=bucket_name.name, Key=pic_path)
            pic_bytes = body['Body']._raw_stream.data
            image_b64 = base64.b64encode(pic_bytes)
            image_string = image_b64.decode('UTF-8', 'ignore')
            piclist.append(image_string)
        post_media[id] = piclist
        #print(post_media)
    return post_media






'''def get_upload(user_id,post_id,pics):
    config = Config(s3={"use_accelerate_endpoint": True})
    s3 = boto3.resource('s3',aws_access_key_id=AWS_UPLOAD_ACCESS_KEY_ID,aws_secret_access_key=AWS_UPLOAD_SECRET_KEY,region_name="us-east-1",config=config,)
    aws_bucket = s3.Bucket("uploaduserpic")
    query="select user_id from p_post where user_id="+str(user_id)+"" 
    res=c.get_result_query(query)
    if (len(res)==0):
        directory_name=str(user_id)
        s3.Bucket(aws_bucket.name).put_object(Key=directory_name+'/')
    
    dir_name=post_id
    directory_name=str(user_id)
    dirr=directory_name+'/'+dir_name+'/'
    s3.Bucket(aws_bucket.name).put_object(Key=dirr)
    #name_image=str(user_id) + "/" + (post_id) + ".jpg"
    for i in range(0,len(pics)):
        s=str(int(post_id)+i)
        name_image=dirr + s + ".jpg"
        obj = s3.Object(aws_bucket.name, name_image)
        
        response = obj.put(Body=base64.b64decode(pics[i]))
    return dirr'''                        