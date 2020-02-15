# encoding:utf8
from . import admin


@admin.route('/')
def admin():
    return "<h1 style='color:red'>This is admin</h1>"
