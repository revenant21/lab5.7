# регистрация моего модуля

from flask import Flask

def create_app():
    app = Flask(__name__)

    # Регистрация модулей
    from .converter.routes import converter_bp
    app.register_blueprint(converter_bp, url_prefix='/api')

    return app