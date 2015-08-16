__author__ = 'anurag'

import os
import sys

#from app.models.extra import fixture

from flask.ext.assets import ManageAssets
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask.ext.script import Manager, Server


from designer.app import flaskapp, assets
manager = Manager(flaskapp)

manager.add_command("runserver", Server(use_debugger = True, use_reloader = True, host = '0.0.0.0', port=4901))
manager.add_command("assets", ManageAssets(assets))

if __name__ == '__main__':
    manager.run()

