import sqlite3 as sql
from pymemcache.client import base

Name = 'Butterfly'

client = base.Client(('localhost', 11211))
result = client.get(Name)

def query_db(Name):
    db_connection = sql.connect('db.sql')
    c = db_connection.cursor()
    try:
        c.execute('select Description from my_table1 where Name = "{k}"'.format(k=Name))
        data = c.fetchone()[0]
        db_connection.close()
    except:
        data = 'invalid'
    return data

if result is None:
    print("got a miss, need to get the data from db")
    result = query_db(Name)
    if result == 'invalid':
        print("requested data does not exist in db")
    else:
        print("returning data to client from db")
        print("=> Product: {p}, Description: {d}".format(p=Name, d=result))
        print("setting the data to memcache")
        client.set(Name, result)

else:
    print("got the data directly from memcache")
    print("=> Product: {p}, Description: {d}".format(p=Name, d=result))
