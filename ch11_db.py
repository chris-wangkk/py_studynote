# -*- coding: utf-8 -*-


##MySQL
'''
pip install mysql-connector

'''
import mysql.connector
def demo001():
    conn = mysql.connector.connect(user='root', password='12345', database='demo')
    cursor = conn.cursor()
    #cursor.execute('create table test (id varchar(20) primary key, name varchar(20))')
    cursor.execute('insert into test (id, name) value (%s, %s)', [3,'berry'])
    print(cursor.rowcount)
    #提交事务
    conn.commit()   #不加这句不会执行插入进去
    cursor.close()
    #
    cursor = conn.cursor()
    cursor.execute('select * from test where id = %s', ('3',))
    values = cursor.fetchall()
    print(values)
    cursor.close()
    conn.close()

##ORM
'''
1.数据库表是一个二维表(包含多行多列)-->
    把一个表的内容用Py的数据结构表示出来的话:可以用一个list表示多行,list的每一个元素是tuple,表示一行记录
2.把一个tuple用class实例来表示,ORM技术(Object-Relational Mapping)
    把关系数据库的表结构映射到对象上
3.SQLAlchemy
    pip install sqlalchemy
'''
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def demo002():
    pass

if __name__=='__main__':
    demo001()