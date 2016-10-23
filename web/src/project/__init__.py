from flask import Flask
app = Flask(__name__, template_folder='views')

from .controllers.api import *
from .controllers.front_end import *