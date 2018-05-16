#!/usr/bin/env python
from app import create_app, db

if __name__ == '__main__':
    application = create_app('development') # We want to use the developement env
    with application.app_context():
        db.create_all()
    application.run()
