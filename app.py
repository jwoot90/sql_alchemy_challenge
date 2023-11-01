# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func,Text

from flask import Flask, jsonify
import datetime

#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
def home():
    """List all available api routes."""
    print('Server Request for Home Page')
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
   
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    print('Server Request for Precipitation Page')
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data)"""
    # 
    
    dt_previous  = datetime.date(2017,8,23) - datetime.timedelta(days = 365)
    results = session.query(measurement.date,measurement.prcp).filter(measurement.date >= dt_previous).all()
    session.close()
    precip = {date:prcp for date, prcp in results}
    return jsonify(precip)
    
    """Return a JSON list of stations from the dataset."""
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.name).all() 
    session.close()
    station_list = []
    for result in results:
        station_list.append(result.name)
    return jsonify(station_list)
@app.route("/api/v1.0/tobs")
def tobs():
    dt_previous  = datetime.date(2017,8,23) - datetime.timedelta(days = 365)
    results = session.query(measurement.date,measurement.tobs).filter(measurement.date >= dt_previous,measurement.station == 'USC00519281').all()
    session.close()
    tobs_list = []
    for result in results:
        tobs_list.append(result.tobs)
    return jsonify(tobs_list)
@app.route("/api/v1.0/<start>")
def start_date(start):
    """Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
    """
    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs).filter(measurement.date >= start)).all()   
    session.close()
    temp_calc = [{"Min":results[0][0],
                  "Max":results[0][1],
                  "Avg":results[0][2]}]
    return jsonify(temp_calc)
   
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    results = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs).filter(measurement.date >= start,measurement.date<= end)).all()   
    session.close()
    end_temp_calc = [{"Min":results[0][0],
                  "Max":results[0][1],
                  "Avg":results[0][2]}]
    return jsonify(end_temp_calc)
    
if __name__ == '__main__':
        app.run(debug = True)