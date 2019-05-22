import os

basedir = os.path.abspath(os.path.dirname(__file__))  # 使用当前路径
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY="ASNDAIONCALSNKLDNALD"