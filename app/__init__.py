from flask import Flask, render_template
from app.extensions import db
from config import Config
from flask_login import LoginManager
from flask_socketio import SocketIO
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

socketio = SocketIO()

def internal_server_error(e):
    print(e)
    return render_template('error.html')

def create_app(config_class=Config):
    app = Flask(__name__)
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

    from app.chat import bp as chat_bp
    app.register_blueprint(chat_bp)

    from app.AI_suggestion import bp as suggestion_bp
    app.register_blueprint(suggestion_bp)

    from app.user_profile import bp as user_profile_bp
    app.register_blueprint(user_profile_bp, url_prefix='/user_profile')

    from app.doctor_main import bp as doctor_main_bp
    app.register_blueprint(doctor_main_bp)

    from app.doctor_profile import bp as doctor_profile_bp
    app.register_blueprint(doctor_profile_bp)

    from app.checkout import bp as checkout_bp
    app.register_blueprint(checkout_bp)

    socketio.init_app(app)
    
    sentry_sdk.init("https://0c433812f6fa3b96275fb3c7ab6bb3f3@o4506383806431232.ingest.sentry.io/4506383807807488", integrations=[FlaskIntegration()])
    
    app.register_error_handler(Exception, internal_server_error)
    
    return app
