# 207HW4
HW4
A Simple caching layer (Memcached) implementation on a database. 
- Database is created using SQLite product information (list_name, list_description)
- Cashing layer is Memcached 
- Our client is a python script, which will check if the required product name (list_name) is present in the cache. If not,
  a GET_MISS will be returned. Then the data will be fetched from database, returned to the client and then saved in the cache.
- The next time data is read, a GET_HIT will be recieved and the data will be returned to the client directly from the cache. 

CREATE A SIMPLE DATABASE TABLE AND POPULATE IT WITH DATA
$ sqlite3 db.sql -header -column
SQLite version 3.29.0 2019-07-10 17:32:03
Enter ".help" for usage hints.
sqlite> 
sqlite> create table my_table1( Name STRING(50), Description STRING(50));
sqlite> insert into my_table1 values ('Orange', 'Fruit');
sqlite> insert into my_table1 values ('Butterfly', 'Insect');
sqlite> insert into my_table1 values ('Phuket', 'Island');
sqlite> insert into my_table1 values ('Python', 'Coding language');

# Read all the data from the table
sqlite> select * from my_table1;
Name        Description
----------  -----------
Orange      Fruit      
Butterfly   Insect     
Phuket      Island     
Python      Coding lang

RUN A MEMCACHED CONTAINER ON DOCHER
$ docker run -itd --name memcached -p 11211:11211 rbekker87/memcached:alpine

CLIENT CODE 
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
    
    
