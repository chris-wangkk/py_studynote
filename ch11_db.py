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
    ORM就是把数据库表的行与相应的对象建立关联并互相转换
3.SQLAlchemy
    pip install sqlalchemy
'''
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# 创建对象的基类
Base = declarative_base()

class Test(Base):
    #表名
    __tablename__ = 'test'
    #表结构
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    #1 vs n
    #books = relationship

class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    #book表是通过外键关联到user表的
    #user_id = Column(String(20), ForeignKey('user.id'))


engine = create_engine("mysql+mysqlconnector://root:12345@localhost:3306/demo") #初始化数据库连接，数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名
DBSession = sessionmaker(bind=engine)

def demo002():
    session = DBSession()   #创建一个会话对象（数据库连接），也就是获取一个session
    new_user = Test(id='6', name='Bob') #一个对应记录的实例
    session.add(new_user)   #加入到session
    session.commit()    #提交保存
    session.close() #关闭session
    #
    session = DBSession()
    rec = session.query(Test).filter(Test.id=='5').one()    #创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行
    print("type: ", type(rec))
    print("name: ", rec.name)
    session.close()

if __name__=='__main__':
    demo002()