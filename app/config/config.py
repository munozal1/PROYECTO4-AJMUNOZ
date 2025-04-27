from  dotenv import load_dotenv
import os

load_dotenv(override=True)

class Config():
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=f"mysql+pymysql://{os.getenv('MYSQL_PYTHON_USER')}:{os.getenv('MYSQL_PYTHON_PWD')}@localhost:3306/heladeria?charset=utf8mb4"