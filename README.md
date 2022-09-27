# sqlalchemy-challenge
Module 10 Challenge

This code creates an engine into the hawaii.sqlite file and maps the existing database into two classes: Measurement and Station.
Measurement holds data including the inches of precipitation that fell in a given day at a particular weather station.
Station holds data including the location of a particular weather station in addition to its longitude and latitude.
The data was filtered by the previous 365 days of data, then ordered based on date, then plotted using MatPlotLib.
Max, min, and average temperatures were filtered and displayed.

In the app, the user is given all available routes.
The data is queried and returned using jsonify to display for the user based on which route they choose.
In the last routes, the user is prompted to include an ending date (proceeding backwards from the most recent update, which was 8/23/17).