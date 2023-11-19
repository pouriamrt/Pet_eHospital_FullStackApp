from flask import Flask
from app.extensions import db
from config import Config
from flask_login import LoginManager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from app.models.auth import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints here
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.pet_profile import bp as pet_bp
    app.register_blueprint(pet_bp)

    from app.user_profile import bp as user_profile_bp
    app.register_blueprint(user_profile_bp, url_prefix='/user_profile')

    return app
