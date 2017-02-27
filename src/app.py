#!/usr/bin/env python

from flask import Flask, jsonify, make_response, request
from scrapers import VehicleEnquiryScraper


app = Flask(__name__)
vehicle_scraper = VehicleEnquiryScraper()


@app.route('/api/v1.0/vehicle-enquiry', methods=['GET'])
def get_vehicle():
    vehicle_scraper.setupDriver()
    vehicle = vehicle_scraper.get_data(
        request.args.get('vrn'), request.args.get('make')
    )
    vehicle_scraper.closeDriver()
    return jsonify(vehicle)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8040)
