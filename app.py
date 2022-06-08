# Import your dependancies
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Set up your database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the database in a variable
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)