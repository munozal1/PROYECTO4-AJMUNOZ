from app.config.db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    
    __tablename__='user'
    
    id= db.Column(db.Integer, autoincrement=True, primary_key=True)
    username= db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(255), nullable=False)
    es_admin= db.Column(db.Boolean,nullable=False)
    es_empleado= db.Column(db.Boolean,nullable=False)
    
    
    #Funcion para cifrar el password
    def __init__(self,username:str,password:str,es_admin: bool, es_empleado: bool):
        self.username=username
        self.password=generate_password_hash(password)
        self.es_admin=es_admin
        self.es_empleado=es_empleado
    
    #Valida el hash generado para la contraseña
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
    def check_credentials(self,username:str, password:str):
        usuario=User.query.filter_by(username=username,password=password).first()
        print(usuario)
        if usuario:
            return True
        return False