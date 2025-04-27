#from app.controllers.home_controller import home_blueprint
from app.controllers.iceCreamStoreController import IceCreamParlor
from app.controllers.apiController import IceCreamParlorApi


def registrar_rutas(app):
    app.register_blueprint(IceCreamParlor)
    app.register_blueprint(IceCreamParlorApi)