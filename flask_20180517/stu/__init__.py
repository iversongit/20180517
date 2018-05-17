import os
from flask import Flask

from grade.views import grade
from stu.views import stu
from flask_sqlalchemy import SQLAlchemy

def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(BASE_DIR,"templates")
    static_dir = os.path.join(BASE_DIR,"static")
    # template_folder -- 默认访问stu下的templates文件夹
    # static_folder -- 默认访问stu下的static文件夹
    app = Flask(__name__,template_folder=templates_dir,static_folder=static_dir)
    app.register_blueprint(blueprint=stu,url_prefix="/stu")  # 学生应用与stu蓝图绑定起来，并以/stu前缀与其他应用进行区分
    app.register_blueprint(blueprint=grade, url_prefix="/grade") # 班级应用与grade蓝图绑定起来，并以/grade前缀与其他应用进行区分

    # 数据库相关配置信息的设定
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:5201314@localhost:3306/flask_20180517"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # 初始化app 将其置于SQLAlchemy框架之下，便于进行orm映射
    # 同时加载数据库配置信息，为后续的使用做准备
    # 若少了此句，则会报如下错误：
    # AssertionError: The sqlalchemy extension was not registered to the current application.
    # Please make sure to call init_app() first.
    # 即具体应用一定要被SQLAlchemy框架初始化，置于其下
    SQLAlchemy(app=app)


    return app