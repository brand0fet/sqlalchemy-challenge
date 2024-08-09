# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt
import pandas as pd

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
# reflect the tables
base.prepare(autoload_with= engine)

# Save references to each table
station = base.classes.station
measure = base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start><end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    twelve_months_ago = dt.date(2017,8,23)- dt.timedelta(days=365)
    precipitation_data = session.query(measure.date,measure.prcp).filter(measure.date >= twelve_months_ago.all())
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    stations_data = session.query(station.station).all()
    stations = list(np.ravel(stations_data))
    return jsonify(stations)    

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date(2017,8,23)-dt.timedelta(days=365)
    data = session.query(measure.tobs).\
        filter(measure.station== 'USC00519281').\
        filter(measure.date >= last_year).all()
    tempers = list(np.ravel(data))
    return jsonify(tempers)



@app.route("/api/v1.0/<start>")
def calc(start):
    dates = dt.datetime.strptime(start,"%Y-%m-%d")

    datas = session.query(func.min(measure.tobs),func.max(measure.tobs),func.avg(measure.tobs)).\
        filter(measure.date >= dates).all()
    
    result = list(np.ravel(datas))

    return jsonify(result)

@app.route("/api/v1.0/<start><end>")
def calc2(start,end):
    start = dt.datetime.strftime(start, "%Y-%m-%d")
    end = dt.datetime.strftime(end, "%Y-%m-%d")

    datas2 = session.query(func.min(measure.tobs),func.max(measure.tobs),func.avg(measure.tobs)).\
        filter(measure.date.between(start,end)).all()
    
    show = list(np.ravel(query_data))
    return jsonify(show)

if __name__ == '__main__':
    app.run(debug=False)