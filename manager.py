# encoding=utf8

from app.models import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import db

# flask 的 migrate
manager = Manager(app)
# 要使用flask-migrate，必须先绑定db和app
migrate = Migrate(app, db)
# 将MigrateCommand添加到manager中，"db"是自定义命令
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
