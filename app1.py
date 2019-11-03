import sqlite3 as sql
from pymemcache.client import base

list_name = 'female'

client = base.Client(('localhost', 11211))
result = client.get(list_name)

def query_db(list_name):
    db_connection = sql.connect('db.sql')
    c = db_connection.cursor()
    try:
        c.execute('select list_description from list where list_name = "{k}"'.format(k=list_name))
        data = c.fetchone()[0]
        db_connection.close()
    except:
        data = 'invalid'
    return data

if result is None:
    print("got a miss, need to get the data from db")
    result = query_db(list_name)
    if result == 'invalid':
        print("requested data does not exist in db")
    else:
        print("returning data to client from db")
        print("=> Product: {p}, Description: {d}".format(p=list_name, d=result))
        print("setting the data to memcache")
        client.set(list_name, result)

else:
    print("got the data directly from memcache")
    print("=> Product: {p}, Description: {d}".format(p=list_name, d=result))
