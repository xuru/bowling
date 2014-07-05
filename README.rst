
============
Introduction
============

This is an exercise in creating a REST API that simulates a bowling score board.


------------
Requirements
------------

- Python 2.7 or later


============
Installation
============

To run the api, you will need to install the pre-requisites::

    pip install -r requirements.txt


=============
Configuration
=============
    

-------------
API Endpoints
-------------

- "/games" lists games; POST to create
- "/games/<id>" get a specific game including the running score totals, DELETE to delete
- "/games/<id>/roll" PUT to add a pin count to the current frame


----
Demo
----

To run the demo, once you have the pre-requisites installed (preferrably in a
virtual environment) you can::

    python ./manage.py serve &

to run the api server, and::

    python ./demo.py

to run a simple example of scoring a bowling game.


-------------
Documentation
-------------

To view the documentation::

    python ./manage.py docs

Should open your browser with the built documentation.


===============
What isn't done
===============

- It would have been nice to implement a more direct way to edit a game, specific frames or rolls.
- Define custom error messages so that errors would be more easily understood.
- More unit tests for negative cases.



