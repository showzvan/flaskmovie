# encoding:utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@127.0.0.1:3306/movie?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机号
    info = db.Column(db.Text)  # 个人简介
    face = db.Column(db.String(255), unique=True)  # 头像
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标识
    userlogs = db.relationship("Userlog", backref="user")  # 会员日志外键关系
    comments = db.relationship("Comment", backref="user")  # 评论外键关系
    moviecols = db.relationship("Moviecol", backref="user")  # 收藏外键关系

    def __repr__(self):
        return "<User %r>" % self.name


# 会员登陆日志
class Userlog(db.Model):
    __tablename__ = "userlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登陆ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 登陆时间

    def __repr__(self):
        return "<Userlog %r" % self.id


# 标签
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    movies = db.relationship("Movie", backref="tag")  # 电影外键日志

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影
class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 播放地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 评级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))  # 电影标签
    area = db.Column(db.String(255))  # 地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    comments = db.relationship("Comment", backref="movie")  # 评论外键关系
    moviecols = db.relationship("Moviecol", backref="movie")  # 收藏外键关系

    def __repr__(self):
        return "<Movie %r>" % self.title


# 上映预告
class Preview(db.Model):
    __tablename__ = "preview"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论
class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))  # 电影编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户编号
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间

    def __repr__(self):
        return "<Comment %r>" % self.id


# 收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))  # 电影编号
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 用户编号
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id


# 权限
class Auth(db.Model):
    __tablename__ = "auth"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色
class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名称
    auths = db.Column(db.String(600))  # 权限列表
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 添加时间
    admins = db.relationship("Admin", backref="role")  # 管理员外键关系

    def __repr__(self):
        return "<Role %r>" % self.id


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    pwd = db.Column(db.String(100))  # 密码
    is_super = db.Column(db.SmallInteger)  # 是否为超级管理员 0为超级管理员
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 注册时间
    adminlogs = db.relationship("Adminlog", backref="admin")  # 管理员登陆日志外键关系
    oplogs = db.relationship("Oplog", backref="admin")  # 管理员操作日志外键关系

    def __repr__(self):
        return "<Admin %r>" % self.name


# 管理员登陆日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登陆ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 登陆时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id


# 管理员操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登陆ip
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 登陆时间

    def __repr__(self):
        return "<Oplog %r>" % self.id


if __name__ == "__main__":
    db.create_all()
    """
    role = Role(
        name="超级管理员",
        auths=""
    )
    db.session.add(role)
    db.session.commit()
    """
    # 密码加密
    # from werkzeug.security import generate_password_hash
    #
    # admin = Admin(
    #     name="admin",
    #     pwd=generate_password_hash('123456'),
    #     is_super=0,
    #     role_id=1
    # )
    # db.session.add(admin)
    # db.session.commit()
