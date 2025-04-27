from app import create_app
from app.config.db import db
from app.config.config import Config
from app.config.routes import registrar_rutas

#Inicializar la configuracion de la aplicacion
app=create_app(Config)

if __name__=='__main__':
    app.run(debug=True)