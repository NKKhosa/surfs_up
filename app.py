# import dependencies
import datetime as dt
from unittest import result 
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func 

from flask import Flask, jsonify 

# set up the database engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the database into our classes 
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save references to each table in varaibles
Measurement = Base.classes.measurement
Station = Base.classes.station 

# create a session link
session = Session(engine)

# create a new Flask instance
app = Flask(__name__)

# define the root
@app.route('/')

# create a function for the welcome route 
def welcome():
    return(
        f"Welcome to the Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
        )

# precipitation route
@app.route('/api/v1.0/precipitation')
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}

    return jsonify(precip)

# stations route
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    #unravel results into 1d array and convert into a list
    stations = list(np.ravel(results))

    return jsonify(stations=stations)

# temperature observations route
@app.route('/api/v1.0/tobs')
def temp_monthly():
    prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# statistics route
@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))

    return jsonify(temps)
    