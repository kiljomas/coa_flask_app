from app import create_app, db

application = create_app('development') # We want to use the developement env
with application.app_context():
    db.create_all()
