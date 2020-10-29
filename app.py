import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/measurement<br/>"
        f"/api/v1.0/station"
    )
#Route requires a function for flask formatting

@app.route("/api/v1.0/measurement")
def measurements():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    results_measurement = list(np.ravel(results))

    return jsonify(results_measurement)




@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    results_station= list(np.ravel(results))

    return jsonify(results_station)


@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

  
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=366)
    scores = session.query(Measurement.station,Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
 
   

    session.close()

    # Convert list of tuples into normal list


    return jsonify(scores)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    active =session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.station== "USC00519281").order_by(Measurement.tobs).all()
    
    session.close()

    # Convert list of tuples into normal list


    return jsonify(active)



@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    scores_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
 
    session.close()

    # Convert list of tuples into normal list


    return jsonify(scores_start)



@app.route("/api/v1.0/<start>/<end>")
def stend(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
 
    scores_stend = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
 
    session.close()

    # Convert list of tuples into normal list


    return jsonify(scores_stend)


#This is always at the end of flask app, it tells how to run the app..key in the engine, if the key is out, it will stop running
if __name__ == '__main__':
    app.run(debug=True)
