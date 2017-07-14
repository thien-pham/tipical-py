import os
from flask_script import Manager
from tips import app
from tips.database import session, Base, Tip, User
from getpass import getpass
from werkzeug.security import generate_password_hash
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)

# Holds metadata changes to DB
class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

# Create instance of Flask-Migrate 'Migrate' class with metadata from SQLAlchemy model (base)
migrate = Migrate(app, DB(Base.metadata))
# Adds all commands from Migrate class to management script
manager.add_command('db', MigrateCommand)

@manager.command
def seed():
    body = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""

    for i in range(25):
        tip = Tip(
            title="Test Tip #{}".format(i),
            body=body
            # location={40.7128, 74.0059}
        )
        session.add(tip)
    session.commit()

@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    manager.run()

@manager.command
def adduser():
    name = input("Name: ")
    email = input("Email: ")
    if session.query(User).filter_by(email=email).first():
        print("User with that email address already exists")
        return

    password = ""
    password_2 = ""
    while not (password and password_2) or password != password_2:
        password = getpass("Password: ")
        password_2 = getpass("Re-enter password: ")
        break
    user = User(name=name, email=email,
                password=generate_password_hash(password))
    session.add(user)
    session.commit()
