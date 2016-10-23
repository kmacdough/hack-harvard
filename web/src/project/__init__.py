from flask import Flask
app = Flask(__name__, template_folder='views')

from .controllers.api import *