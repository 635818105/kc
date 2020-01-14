from flask_script import Manager, Server
from config import DevelopmentConfig as Config
from application import create_app
app = create_app(Config)
manager = Manager(app)
manager.add_command("runserver", Server(app.config["HOST"], port=app.config["PORT"], passthrough_errors=True))

if __name__ == "__main__":
    manager.run()
