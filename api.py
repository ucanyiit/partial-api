import datetime as dt

from flask import Flask, jsonify, request

# User statuses
P = 'paying'
C = 'completed'
NP = 'non-paying'


class UserStatusSearch:
    RECORDS = [
        {'user_id': 1, 'created_at': '2017-01-01T10:00:00', 'status': P},
        {'user_id': 1, 'created_at': '2017-03-01T19:00:00', 'status': P},
        {'user_id': 1, 'created_at': '2017-02-01T12:00:00', 'status': C},
        {'user_id': 2, 'created_at': '2017-09-01T17:00:00', 'status': P},
        {'user_id': 3, 'created_at': '2017-10-01T10:00:00', 'status': P},
        {'user_id': 3, 'created_at': '2016-02-01T05:00:00', 'status': C},
    ]

    def __init__(self):
        pass

    def get_status(self, user_id, date):
        pass


class IpRangeSearch:
    RANGES = {
        'London': [
            {'start': '10.10.0.0', 'end': '10.10.255.255'},
            {'start': '192.168.1.0', 'end': '192.168.1.255'},
        ],
        'Munich': [
            {'start': '10.12.0.0', 'end': '10.12.255.255'},
            {'start': '172.16.10.0', 'end': '172.16.11.255'},
            {'start': '192.168.2.0', 'end': '192.168.2.255'},
        ]
    }

    def __init__(self):
        pass

    def get_city(self, ip):
        pass


class AggregateUserCity:
    def __init__(self):
        pass

    def get_aggregate(self, status, city):
        pass


app = Flask(__name__)


@app.route('/user_status')
def user_status():
    """Return user status for a given date"""
    user_id = int(request.args.get('user_id'))
    date = dt.datetime.strptime(
        str(request.args.get('date')), '%Y-%m-%dT%H:%M:%S')

    user_status_search = UserStatusSearch()
    return jsonify({
        'user_status': user_status_search.get_status(user_id, date)
    })


@app.route('/ip_city')
def ip_city():
    """Return city for a given ip"""
    ip = str(request.args.get('ip'))

    ip_range_search = IpRangeSearch()
    return jsonify({'city': ip_range_search.get_city(ip)})


@app.route('/user_city')
def user_city():
    """Return aggregated sum of the product price for the given user status
    and city"""
    status = str(request.args.get('user_status'))
    city = str(request.args.get('city'))

    aggregate_user_city = AggregateUserCity()
    return jsonify({
        'product_price': aggregate_user_city.get_aggregate(status, city)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
