# from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# class Grade(db.Model):
#     g_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     g_name = db.Column(db.String(10),unique=True)
#     g_desc = db.Column(db.String(100),nullable=True)
#     g_create_time = db.Column(db.Date,default=datetime.now)
#     # lazy：懒加载  访问时（.student）才加载关系
#     students = db.relationship('Student',backref='stu',lazy=True)
#     __tablename__ = "grade"
#
#     def __init__(self,name,desc):
#         self.g_name = name
#         self.g_desc = desc
