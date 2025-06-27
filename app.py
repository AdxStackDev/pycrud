from flask import Flask
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)

    # Register blueprints
    from users.routes import users_bp
    from visitors.routes import visitors_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(visitors_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
