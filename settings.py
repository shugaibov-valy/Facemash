import os

app_dir = os.path.abspath(os.path.dirname(__file__)).replace('\\', "/")


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supEveJkeR'
    DEBUG = False

    db_name = os.environ.get('DB_NAME', 'facemash')
    db_user = os.environ.get('DB_USER', 'postgres')
    db_password = os.environ.get('DB_PASSWORD', 'qwerty')
    db_host = os.environ.get('DB_HOST', 'psql_facemash')
    db_port = os.environ.get('DB_PORT', 5432)

    @property
    def alchemy_url(self):
        return f'postgresql+psycopg2://{self.db_user}:{self.db_password}@' \
               f'{self.db_host}:{self.db_port}/{self.db_name}'

config = BaseConfig()
