import os


class BaseConfig(object):
    """ 配置基类 """
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True


class DevelopmentConfig(BaseConfig):
    """ 开发环境配置 """
    DEBUG = True
    ADMIN_PER_PAGE=1
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost:3306/blog?charset=utf8'

class ProductionConfig(BaseConfig):
    """ 生产环境配置 """
    pass
class TestingConfig(BaseConfig):
    """ 测试环境配置 """
    pass
configs = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}