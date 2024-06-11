# Import the dependencies.

from sqlalchemy.ext.automap import automap_database
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime, timedelta
import numpy as np

#################################################
# Database Setup
#################################################
engine = create_engine ("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_database()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return{
        f"Climate of Hawai API<br/>"
        f"Choose your route<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
}

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
    recent = session.query(func.max(Measurement.date)).scalar()
    recent_date = datetime.strptime(recent, '%Y-%m-%d')
    year_before= recent_date - timedelta(days=365)

    results = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_before).all()
    
    session.close()

    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)
    #Return the JSON representation of your dictionary.
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations<br/>")
#Return a JSON list of stations from the dataset.
def stations():
# Query station data from the Station dataset
    results = session.query(Station.station).all()

    session.close()

# Convert list of tuples into normal list
    station_list = list(np.ravel(results))

    # Return a list of jsonified station data
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
#Query the dates and temperature observations of the most-active station for the previous year of data.
def temp():    
    recent = session.query(func.max(Measurement.date)).scalar()
    recent_date = datetime.strptime(recent, '%Y-%m-%d')
    year_before= recent_date - timedelta(days=365)

    results = session.query(Measurement.station, Measurement.tobs).\
                filter(Measurement.station == "USC00519281").\
                filter(Measurement.date >= year_before).all()

    session.close()

    temp_list = list(np.ravel(results))

#Return a JSON list of temperature observations for the previous year.
    return jsonify(temp_list)