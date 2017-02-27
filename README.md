Uk Government Services (unofficial) API
=======================================

Sometimes you just need to use a service programmatically and it doesn't have an API. A good example are the Vehicle and Driving License APIs provided by the UK government. This application allows you to use the following services via an HTTP API.

1. Vehicle Enquiry - https://vehicleenquiry.service.gov.uk/ (complete)
2. Driving Record - https://www.viewdrivingrecord.service.gov.uk/ (coming soon)

It can easily be adapted to add more and I am more than happy to review any pull requests that I receive. Some of this code was not written by me, wherever possible I have credited the relevant author. If I have missed you out please contact me.

Testing Locally
---------------

* Make sure you have Chromium or Chrome installed.
* Make sure you have the Chrome Web Driver installed. 

````
pip install -r requirements.txt
python src/app.py
````

Using Docker and UWSGI
----------------------

The easiest way to get this up and running is with Docker. Make sure you have it installed and then:

````
docker build -t ukservicesapi .
docker run -d --name ukservicesapicont -p 8001:8001 ukservicesapi
````

The container will be listening at http://localhost:8001

Production Deployment
---------------------

The docker file runs Flask under UWSGI, you should not expose it directly to the web. Deploy it behind a reverse proxy like Nginx.

Inspiration
-----------

https://github.com/jonhaddow/vehicle-enquiry-python