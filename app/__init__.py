__author__ = 'anurag'

from flask import Flask
import settings

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': settings.MONGODB_DB,
    'host': settings.MONGODB_HOST,
    'port': settings.MONGODB_PORT
}


if __name__ == '__main__':
    app.run(host='localhost', port=4900)

