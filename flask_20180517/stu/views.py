import random
from flask import Blueprint,render_template,request
from stu.models import db, Student
from sqlalchemy import and_,or_,not_

stu = Blueprint('stu',__name__)

@stu.route("/")
def index():
    return render_template("index.html")

@stu.route("/createdb/")
def create_db():
    db.create_all() # 创建数据库表
    return '创建数据表成功'

@stu.route("/dropdb/")
def drop_db():
    db.drop_all() # 删除数据库表
    return '删除数据表成功'

@stu.route("/createstu/",methods=['GET','POST']) # methods -- 指定请求方式
def create_stu():
    if request.method == "GET":
        return render_template('create_stu.html')
    if request.method == "POST":
        username = request.form.get("username") # form -- 对应post请求
        age = request.form.get("age")
        stu = Student(username,age)  # 创建一个学生实例
        db.session.add(stu)
        db.session.commit()
        return "单个学生实例创建成功"

@stu.route('/createstus',methods=['GET','POST'])
def create_stus():
    if request.method == "GET":
        return render_template('createstus.html')
    else:
        stus_list = []
        username1 = request.form.get("username1")
        age1 = request.form.get("age1")

        username2 = request.form.get("username2")
        age2 = request.form.get("age2")

        stu1 = Student(username1, age1)
        stu2 = Student(username2, age2)

        stus_list.append(stu1)
        stus_list.append(stu2)


        db.session.add_all(stus_list)  # 添加多个学生对象，放置列表
        db.session.commit() # 提交至数据库
        return "多个学生实例创建成功"

@stu.route('/selectstu/')
def select_stu():
    # 年龄小于23岁的学生的信息
    # stus = Student.query.filter(Student.s_age < 23)

    # stus = Student.query.filter(Student.s_age.__lt__(22)) # 小于
    # stus = Student.query.filter(Student.s_age.__le__(22))  # 小于等于
    # stus = Student.query.filter(Student.s_age.__gt__(22)) # 大于
    # stus = Student.query.filter(Student.s_age.__ge__(22)) # 大于等于

    # in_ -- 固定取值范围
    # stus = Student.query.filter(Student.s_age.in_([16,1,20,34,23,32]))

    # 获取所有学生信息(执行原生sql语句)
    # sql = "select * from student;"
    # stus = db.session.execute(sql)

    # 对BaseQuery进行order_by 按照id降序排列
    # Student.query.all().order_by('-s_id') -- 错误！！ Student.query.all()为一列表 列表没有order_by属性
    # stus = Student.query.order_by('-s_id') -- 正确 ！！

    # 按照id降序获取三个学生信息
    # stus = Student.query.order_by('-s_id').limit(3)

    # 获取年龄最大的学生信息
    # stus = Student.query.order_by('-s_age').first()

    # 跳过三个元素后查询五个元素
    # stus = Student.query.order_by('-s_age').offset(3).limit(5)

    # 跳过三个元素后显示所有元素
    # stus = Student.query.order_by('-s_age').offset(3)

    # 过滤的两种形式(返回的皆为BaseQuery对象)
    #     1）.filter(模型名.字段==value)
    #     2) .filter_by(字段=value)
    # stus = Student.query.filter(Student.s_id==1)
    stus = Student.query.filter_by(s_id=1)

    # get括号内只放主键的值  不能加关键字
    # stu = Student.query.get(1) # 获取id=1的学生

    # 按照多个条件查找值（默认多个条件采取and操作）
    # stus = Student.query.filter(Student.s_name == '张三',Student.s_age == 18)


    # and / not / or  -- 与/或/非
    # stus = Student.query.filter(and_(Student.s_id == 20, Student.s_age == 18))
    # stus = Student.query.filter(or_(Student.s_id == 20, Student.s_age == 18))
    # stus = Student.query.filter(not_(Student.s_id == 20))
    return render_template("student_list.html", stus=stus)

@stu.route('/createstusbyrange/')
def create_random_stus():  # 批量创建信息
    stus_list = []
    for i in range(20):
        stu = Student("员工%d" % random.randrange(500),  # s_name
                "%d" % random.randrange(50))  # s_age
        stus_list.append(stu)


    db.session.add_all(stus_list)  # 添加多个学生对象，放置列表
    db.session.commit() # 提交到数据库
    return "批量实例创建成功"

@stu.route('/stupage/')
def stu_page():  # 设置分页
    page = int(request.args.get('page',1)) # page:当前页数  默认为1
    per_page = int(request.args.get('per_page',10)) # per_page:每页显示多少信息  默认为10
    paginate = Student.query.order_by('-s_id').paginate(page,per_page,error_out=False) # error_out:是否显示错误信息
    stus  = paginate.items # 获取学生信息
    return render_template('stupage.html',paginate=paginate,stus=stus)

@stu.route('/selectgradebystu/<int:id>')
def select_grade_by_stu(id):  #　通过学生找所属的班级信息
    stu = Student.query.get(id)
    grade = stu.stu # .stu from Grade students's backref
    # stu.s_g --> 只会显示g_id(int类型)，此点Django不同
    return render_template('student_grade.html',grade=grade,stu=stu)