import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
inspector = inspect(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station


inspector.get_table_names()

session = Session(engine)


app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
     
    precip =  session.query(measurement.date, measurement.prcp).\
        filter( measurement.date >= '2016-08-23', measurement.date <= '2017-08-23').all()
    
    session.close()

    all_precipitation = []
    for date, prcp in precip:
        precipitation_dict = {}
        precipitation_dict["Date"] = date
        precipitation_dict["PRCP"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():

    connect = engine.connect()

    station = pd.read_sql_query("SELECT station FROM station;", connect)
    station

    all_stations = list(np.ravel(station))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temp():

    session = Session(engine)

    temperature = session.query(measurement.tobs).\
        filter(measurement.date >= '2016-08-23', measurement.date <= '2017-08-23').all()
    
    session.close()

    all_temps = list(np.ravel(temperature))

    return jsonify(all_temps)

@app.route("/api/v1.0/start")
def start():

    print("Start date API request.")

    session = Session(engine)

    trip_start = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= '2014-08-18').all()


    session.close()

    start_list = list(np.ravel(trip_start))

    return jsonify(start_list)




@app.route("/api/v1.0/start/end")
def end():


    print("Start date and end date API request.")
    
    session = Session(engine)

    trip_complete = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= '2014-08-18').filter(measurement.date <= '2017-08-23').all()

    session.close()

    start_end_list = list(np.ravel(trip_complete))

    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)

