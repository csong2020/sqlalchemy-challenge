import sqlalchemy
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Create engine and reflect
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
Base.classes.keys()

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available API routes."""
    return (
        f"Aloha! This is the Hawaii Weather API!<br/>"
        f"Use these routes to surf the site:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        f"Note: The start date is the last date the API has been updated (2017-08-23)."
    )

#Week 11, Day 3, Activity 10
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query date and precipitation from the measurement class
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016,8,23').order_by(
            Measurement.date).all()

    session.close()

    # Convert to dictionary and append to a list of dates and precipitation values
    date_precipitation_list = []

    for date, prcp in results:
        date_precipitation_dict = {}
        date_precipitation_dict['date'] = date
        date_precipitation_dict['prcp'] = prcp
        date_precipitation_list.append(date_precipitation_dict)

    return jsonify(date_precipitation_list)




@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations for the station name
    results = session.query(Station.station, Station.name).all()

    session.close()

    return jsonify(results)





@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    max_station_tob=session.query(Measurement.station,func.max(Measurement.tobs)).first()
    
    updated_last = session.query(Measurement.date).\
        filter(Measurement.station==max_station_tob[0]).\
            order_by(Measurement.date.desc()).first()
    
    past_year=dt.datetime(2017,8,23) - dt.timedelta(days = 365)
    
    # Query the previous year for tobs and ordering by their date
    total_tobs = session.query(Measurement.station,Measurement.tobs).\
        filter(Measurement.station == max_station_tob[0]).order_by(Measurement.date).all()

    session.close()

    return jsonify(total_tobs)






@app.route("/api/v1.0/<start>")
def stats(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs).label('min_temp'), func.max(Measurement.tobs).label('max_temp'), func.avg(Measurement.tobs).label('avg_temp')).\
        filter(Measurement.date >= start).all()
    
    session.close()

    stats_tobs = []
    
    for bob in results:
        tobs_dict = {}
        tobs_dict['min_temp'] = bob.min_temp
        tobs_dict['max_temp'] = bob.max_temp
        tobs_dict['avg_temp'] = bob.avg_temp
        stats_tobs.append(tobs_dict)

    return jsonify(f"Start date:{start}",stats_tobs)





@app.route("/api/v1.0/<start>/<end>")
def stats_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs).label('min_temp'), func.max(Measurement.tobs).label('max_temp'), func.avg(Measurement.tobs).label('avg_temp'))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date<= end).all()
    
    session.close()
    
    stats_tobs = []
    
    for bob in results:
        tobs_dict = {}
        tobs_dict['min_temp'] = bob.min_temp
        tobs_dict['max_temp'] = bob.max_temp
        tobs_dict['avg_temp'] = bob.avg_temp
        stats_tobs.append(tobs_dict)

    return jsonify(f"Start date:{start}",f"End date:{end}",stats_tobs)







if __name__ == '__main__':
    app.run(debug=True)