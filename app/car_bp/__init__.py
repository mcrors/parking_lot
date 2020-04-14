from flask import Blueprint

car_bp = Blueprint('car_bp', __name__)

from . import resources
