
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Resources/hawaii.sqlite") #https://docs.sqlalchemy.org/en/13/core/engines.html initialize with 4 slashes

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes

@app.route("/")
def index():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    last_date=session.query(measurement.date).order_by(measurement.date.desc()).first()[0]
    date_str = dt.datetime.strptime(last_date, '%Y-%m-%d')-dt.timedelta(days=365)

    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= date_str).all()

    session.close()

    precipitation= []
    for date, prcp in results:
        precipitation.append({date:prcp})

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.name).all()
    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    sel = [station.name,
       func.count(measurement.tobs)]

    session = Session(engine)
    most_active = session.query(*sel).filter(station.station==measurement.station).group_by(station.name).order_by(func.count(measurement.station).desc())[0]
    results = session.query(measurement.date, measurement.tobs).filter(station.station == measurement.station).filter(station.name == most_active).filter(measurement.date >= date_str).all()
    session.close()

    tobs_list= []
    for date, tobs in results:
        precipitation.append({date:tobs})

    return jsonify(tobs_list)   
