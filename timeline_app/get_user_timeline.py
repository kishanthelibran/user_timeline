from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from datetime import datetime, date
import json
from django.http import HttpResponse
from db_connection import connect_cassandra as c
from db_connection import aws_connection as aw
from db_connection import dynamo_connection as db
import pytz


@api_view(["POST"])
def get_request(request):
    try:
        user_id = request.data['user_id']
        LastEvaluatedKey = request.data['exclusive_start_key']
        #query="select * from p_post where user_id="+str(user_id)+" LIMIT 10 "
        # all_post=c.get_result_query(query)
        IST = pytz.timezone('Asia/Kolkata')
        ctime = datetime.now(IST).strftime('%d/%m/%Y')
        now = str(ctime)
        print('before get_details : '+now)
        all_post = db.Get_details(user_id, LastEvaluatedKey)
        length = len(all_post)
        time = datetime.now()
        now = str(time)
        print('after get_details'+now)

        list_post = []
        for id in range(0, length):
            # all_post[i].update({'post_id':id})
            if "post_id" in all_post[id]:
                list_post.append(all_post[id]['post_id'])
            # else:
             #   list_post.append(all_post[id]['post_id'])'''

        print('before list_liked'+now)

        get_like_comment = []
        if len(list_post) != 0:
            get_like_comment = db.Get_like_comment(list_post)

        time = datetime.now()
        now = str(time)
        i = 0

        if len(get_like_comment) != 0:
            for id1 in get_like_comment:
                all_post[i].update({'like_comment': id1})
                if len(id1) != 0:
                    for data in id1:
                        notpresent = 0
                        if user_id == data['like']:
                            all_post[i].update({'like': 'True'})
                            break
                        else:
                            notpresent = notpresent + 1

                    '''for data in id1:
                        if data['like'] != "":
                            likeCount = likeCount+1
                        if data['comment'] != "":
                            commentCount = commentCount+1
                    all_post[i].update({'totallike':likeCount})
                    all_post[i].update({'totalcomment':commentCount})
                    i = i+1'''

                    if notpresent > 0:
                        all_post[i].update({'like': 'False'})
                    i = i+1
                else:
                    # list_liked.append('False')
                    all_post[i].update({'like': 'False'})
                    i = i+1
        else:
            like_comment = []
            all_post[0].update({'like_comment': like_comment})
            all_post[0].update({'like': 'False'})

        '''i = 0
        for get_data in get_like_comment:
            likeCount = 0
            commentCount = 0
            if len(get_data) != 0:
                for data in get_data:
                    if data['like'] != "":
                        likeCount = likeCount+1
                    if data['comment'] != "":
                        commentCount = commentCount+1
                all_post[i].update({'totallike':likeCount})
                all_post[i].update({'totalcomment':commentCount})
                i = i+1
            else:
                all_post[i].update({'totallike':likeCount})
                all_post[i].update({'totalcomment':commentCount})
                i = i+1'''

        time = datetime.now()
        now = str(time)
        print('after list_liked'+now)

        time = datetime.now()
        now = str(time)
        print('before media_details'+now)
        '''if len(list_post) != 0:
            media_details=aw.fetch_media(user_id,list_post)
            i = 0
            for media in media_details:
                all_post[i].update({'post_media':media_details[media]})
                i = i+1
        else:
            media_list = []
            all_post[0].update({'post_media':media_list})'''
        media_list = []
        all_post[0].update({'post_media': media_list})

        time = datetime.now()
        now = str(time)
        print('after media_details'+now)
        '''final_timeline_list=[]
        final_timeline_list.append(all_post)
        final_timeline_list.append(media_details)
        final_timeline_list.append(get_like_comment)
        final_timeline_list.append(list_liked)'''
        # print(final_timeline_list)
        response = json.dumps(all_post)
        return HttpResponse(response)
    except ValueError as e:
        return e
