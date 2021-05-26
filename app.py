
##Dependencies

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,inspect

from flask import Flask, jsonify


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///../sqlalchemy-challenge/Resources/hawaii.sqlite")

# Save references to each table
Base = automap_base()
Base.prepare(engine, reflect=True)
measurement = Base.classes.measurement

# Save references to each table
Base = automap_base()
Base.prepare(engine, reflect=True)
station = Base.classes.station


#################################################
# Flask Setup
app = Flask(__name__)

# Flask Routes


@app.route("/")
def welcome():
    return (
        f"Surfer, Welcome to the Climate Page!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return Precipitation Query"""
    prcp_results=session.query(measurement.date, measurement.prcp).\
    order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    prcp = list(np.ravel(prcp_results))

    return jsonify(prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return stations Query"""
    stations_results=session.query(station.station, station.name).\
    order_by(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations= list(np.ravel(stations_results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return Tobs Query"""
    tobs_results=session.query(measurement.date, measurement.tobs).\
    filter(measurement.date > '2016-08-22',measurement.station =="USC00519281" ).\
    order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    tobs= list(np.ravel(tobs_results))

    return jsonify(tobs)

@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temp stats start Query"""
    date_start = dt.datetime(2012, 5, 4)
    
    stats= [func.min(measurement.tobs), 
    func.max(measurement.tobs), 
    func.avg(measurement.tobs)] 

    start_results= session.query(*stats).\
    filter(measurement.date > date_start ).\
    order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    start_stats= list(np.ravel(start_results))

    return jsonify(start_stats)

@app.route("/api/v1.0/start/end")
def start_end():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temp stats start-end Query"""
    date_start = dt.datetime(2012, 5, 4)
    date_end = dt.datetime(2014, 5, 4)
    
    stats= [func.min(measurement.tobs), 
    func.max(measurement.tobs), 
    func.avg(measurement.tobs)] 

    start_end = session.query(*stats).\
    filter(measurement.date >= date_start).\
    filter(measurement.date <= date_end).\
    order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    start__end_stats= list(np.ravel(start_end))

    return jsonify(start__end_stats)


if __name__ == "__main__":
    app.run(debug=True)
