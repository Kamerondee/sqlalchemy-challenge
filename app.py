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

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Set up Flask
app = Flask(__name__)


# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hawaii Weather Data Routes:<br/><br>"
        f"-- Precipiation Totals: <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
        f"-- Active Weather Stations: <a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"-- Station USC00519281 Temperature Observation: <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f"-- Min, Average & Max Temperatures for Date Range: /api/v1.0/trip/yyyy-mm-dd/yyyy-mm-dd<br>"
        f"NOTE: If no end-date is provided, the trip api calculates stats through 08/23/17<br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session from Python to the database
    session = Session(engine)

    """Return a list of all Precipitation Data"""
    # Query all Precipitation data
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-24").all()
    session.close()

    # JSON the information
    json_data = []
    for date, prcp in data:
        new_dict = {"date": date, "prcp": prcp}
        json_data.append(new_dict)
        # Return the dates and prcp
    return jsonify(json_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create new session for stations
    session = Session(engine)
    data = session.query(station.name, station.longitude, station.latitude, station.elevation).all()
    session.close()

   # JSON the information
    json_data = []
    for name, longitude, latitude, elevation in data:
        new_dict = {"name": name, "longitude": longitude, "latitude": latitude, "elevation": elevation}
        json_data.append(new_dict)
        # Return the station data
    return jsonify(json_data)

@app.route("/api/v1.0/tobs")
def tobs():
   # Create a new session for tobs
    session = Session(engine)
    data = session.query(Station.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').where(Station.id == 7).all()
    session.close()

    # JSON the information
    json_data = []
    for name, date, tobs in data:
        new_dict = {"name": name, "date": date, "temperature": tobs}
        json_data.append(new_dict)
       # Return tobs data
    return jsonify(json_data)

@app.route("/api/v1.0/<start>")
def start_temp(start):
    # Find non-existing end dates and then proceed with a new session
    session = Session(engine)
    df = pd.DataFrame(session.query(measurement.date))
    df.columns = ["date"]
    # Start loop
    if start in df["date"].tolist():
        data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs)\
                             , func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        session.close()
        json_data = []
        for x, y, z in data:
            new_dict = {"units": "fahrenheit", "min": x, "avg": y, "max": z}
            json_data.append(new_dict)
        return jsonify(json_data)
    session.close()
    # Return non-existing
    return jsonify({"error": f"Date: {start} not found."}), 404



