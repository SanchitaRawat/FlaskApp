#petsdb
# petid petname owner

import psycopg2
class pet:
    def __init__(self,name,pnum,type,breed,pname):
        self.name=name
        self.pnum=pnum
        self.type=type
        self.breed=breed
        self.pname=pname

class DbConnection:
    con=None
    cur=None
    def __init__(self):
        pass

    @classmethod
    def connect_db(cls):
        cls.con=psycopg2.connect(dbname='postgres', user="postgres", password="Finserv@2023")
        cls.cur=cls.con.cursor()

    @classmethod
    def create_table(cls,tablename,f1,f2,f3,f4,f5):
        cls.cur.execute("create table "+str(tablename)+"("+"id serial primary key, "+str(f1)+" varchar, "+str(f2)+" varchar, "+str(f3)+" varchar, "+str(f4)+" varchar, "+str(f5)+" varchar);")

    @classmethod
    def insert_db(cls,tablename,f1,f2,f3,f4,f5):
        cls.cur.execute(f"insert into {tablename}(name,pnum,breed,type,pname) values('{(f1)}','{(f2)}','{(f3)}','{(f4)}','{(f5)}');")
        cls.con.commit()

    @classmethod
    def select_records(cls,tablename):
        cls.cur.execute(f"select * from {tablename};")
        pets=cls.cur.fetchall()
        for s in pets:
            print(s)
        return pets

    @classmethod
    def drop_table(cls,tablename):
        cls.cur.execute("drop table "+str(tablename)+";")
        cls.con.commit()

    @classmethod
    def check_table(cls,tablename):
        cls.cur.execute(f"select exists(select from pg_tables where schemaname='public' AND tablename='{tablename}');")
        ans=cls.cur.fetchone()
        return ans

    @classmethod
    def update_table(cls,tablename,a,b,c,d,e):
        cls.cur.execute(f"update {tablename} set name='{a}', pnum='{b}',breed='{c}',type='{d}', pname='{e}' where name='{a}';")
        cls.con.commit()

    @classmethod
    def delete_record(cls,tablename,a):
        cls.cur.execute(f"delete from {tablename} where name='{a}';")
        cls.con.commit()

    @classmethod
    def close_db(cls):
        cls.con.close()
        cls.cur.close()

