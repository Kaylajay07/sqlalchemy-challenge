# Import the dependencies.
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
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/'[start_date]'<br/>"
        f"/api/v1.0/'[start_date]/[end_date]'"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

   
    # Query all results
    sel = [Measurement.date, Measurement.prcp]
    results = session.query(*sel).\
    filter(Measurement.date >= query_date).all()
    result = {date:prcp for date,prcp in results}
    session.close()

    # Convert list of tuples into normal list
    return jsonify(result)




@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all results
    results = session.query((Station.station)).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)




@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    query_date = dt.date(2016, 8, 23) - dt.timedelta(days=365)
    
    # Query all results 
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= query_date).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)





@app.route("/api/v1.0/<start_date>")
def start(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    
    # Query all results
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()

    # Convert list of tuples into normal list
    start_tobs = []
    for min, avg, max in results:
        start_dict = {}
        start_dict["min_temp"] = min
        start_dict["avg_temp"] = avg
        start_dict["max_temp"] = max
        start_tobs.append(start_dict)

    return jsonify(start_tobs)




@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

   
    # Query all results
   
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    
 

    session.close()

    # Convert list of tuples into normal list
    start_end_tobs = []
    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["min_temp"] = min
        start_end_dict["avg_temp"] = avg
        start_end_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs)


    return jsonify(start_end_tobs)







if __name__ == '__main__':
    app.run(debug=True)