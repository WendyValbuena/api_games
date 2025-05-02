from flask import Flask
from app.routers.characters import characters_bp
from app.routers.login import login_bp  

def create_app():
    app = Flask(__name__)

    #REGISTER BLUEPRINTS
    
    app.register_blueprint(characters_bp)
    app.register_blueprint(login_bp) 

    return app
