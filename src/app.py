#!/usr/bin/env python

from flask import Flask, jsonify, make_response, request
from scrapers import LicenseScraper, LicenseAuthorizationScraper, VehicleEnquiryScraper

from ukpostcodeparser.parser import parse_uk_postcode


app = Flask(__name__)
license_scraper = LicenseScraper()
license_authorization_scraper = LicenseAuthorizationScraper()
vehicle_scraper = VehicleEnquiryScraper()


@app.route('/api/v1.0/license', methods=['GET'])
def get_license():
    license_scraper.setupDriver()
    license = license_scraper.get_data(
        request.args.get('dln'), request.args.get('nino')
    )
    license_scraper.closeDriver()
    return jsonify(license)


@app.route('/api/v1.0/license-auth', methods=['GET'])
def get_license_authorization():
    license_authorization_scraper.setupDriver()
    outcode, incode = parse_uk_postcode(request.args.get('postcode'))
    postcode = '{}{}'.format(outcode, incode)
    license_authorization = license_authorization_scraper.get_data(
        request.args.get('dln'), request.args.get('nino'), postcode
    )
    # license_authorization_scraper.closeDriver()
    return jsonify(license_authorization)


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
