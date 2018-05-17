from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()  # 创建数据库实例

class Student(db.Model): # 学生模型
    s_id = db.Column(db.INTEGER,primary_key=True,autoincrement=True) # id 整型  主键  自增
    s_name = db.Column(db.String(20),unique=True) # 姓名  字符串  不重复
    s_age = db.Column(db.INTEGER,default=10) # 年龄 整型 默认10
    # 外键中的内容一定是“modelname(小写).主键”
    # 外键虽然不能像Django中的那样直接使用，但是不可或缺，否则会出现如下错误
    # NoForeignKeysError: Could not determine join condition between parent/child tables on relationship Grade.students
    # - there are no foreign keys linking these tables. Ensure that referencing columns are associated with a ForeignKey
    # or ForeignKeyConstraint, or specify a 'primaryjoin' expression.
    s_g = db.Column(db.Integer,db.ForeignKey("grade.g_id"),nullable=True) # 设置外键 or db.ForeignKey("grade.g_id")
    __tablename__ = "student"

    def __init__(self,name,age):  # 初始化函数
        self.s_name = name
        self.s_age = age

class Grade(db.Model): # 班级模型
    g_id = db.Column(db.Integer,primary_key=True,autoincrement=True) # 班级id  主键  自增
    g_name = db.Column(db.String(10),unique=True)  # 班级名称  独一无二
    g_desc = db.Column(db.String(100),nullable=True)  # 班级描述  可以为空
    g_create_time = db.Column(db.Date,default=datetime.now)  # 创建时间，默认为当前时间
    # Student:关联的模型名称  backref -- (关联模型实例.stu --> 对应的Grade实例)
    # lazy：懒加载  访问时（即 grade.students）才加载两个模型间的关系
    students = db.relationship('Student',backref='stu',lazy=True)
    __tablename__ = "grade"

    def __init__(self,name,desc):
        self.g_name = name
        self.g_desc = desc
