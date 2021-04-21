'''from cassandra.cluster import Cluster
from datetime import datetime
from cassandra.query import dict_factory
#import time_uuid, datetime,random
def get_insert_query(query,record_list):
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect('local_cassandra')
    session.execute(query, record_list)
    cluster.shutdown()
    return True
def get_result_query(query):
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect('local_cassandra')
    session.row_factory=dict_factory
    rows=session.execute(query)
    k=rows.all()
    cluster.shutdown()
    return k'''

'''user_id=1
query="select * from p_post where user_id="+str(user_id)+""
m=get_result_query(query)
print(m)'''

'''post='kam'
location='csdc'
user_id=1
#floor_day = lambda d: datetime.datetime(year=d.year, month=d.month, day=d.day)
#today = floor_day(datetime.datetime.utcnow())
#print(today)
#print(type(today))
#rand_time = lambda: float(random.randrange(0,30))+time_uuid.utctime()
#uids = [time_uuid.TimeUUID.with_timestamp(rand_time()) for i in range(0,1)]
#now=uuids[0]
now = datetime.now()
timestamp = str(int(datetime.timestamp(now)))
print(type(now))
print(timestamp)
print(type(timestamp))
#print(now)
#print(type(now))
query="INSERT INTO p_post(post_id,post_caption,post_location,user_id) VALUES (%s,%s,%s,%s)"
rec=[timestamp,post,location,user_id]
get_insert_query(query,rec)'''
'''user_id=5
q="select user_id from p_post where user_id="+str(user_id)+""
m=get_result_query(q)
if(m):
    print("path exits")
print(m)'''

