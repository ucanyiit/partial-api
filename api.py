import datetime as dt
import json

from flask import Flask, jsonify, request

# User statuses
P = "paying"
C = "completed"
NP = "non-paying"

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


def convert_str_to_date(str_date):
    return dt.datetime.strptime(str_date, DATE_FORMAT)


class UserStatusSearch:
    RECORDS = [
        {"user_id": 1, "created_at": "2017-01-01T10:00:00", "status": P},
        {"user_id": 1, "created_at": "2017-03-01T19:00:00", "status": P},
        {"user_id": 1, "created_at": "2017-02-01T12:00:00", "status": C},
        {"user_id": 2, "created_at": "2017-09-01T17:00:00", "status": P},
        {"user_id": 3, "created_at": "2017-10-01T10:00:00", "status": P},
        {"user_id": 3, "created_at": "2016-02-01T05:00:00", "status": C},
    ]

    def __init__(self):
        self.user_records = {}

        for record in self.RECORDS:
            user_id = record["user_id"]

            if user_id not in self.user_records:
                self.user_records[record["user_id"]] = []

            new_record = {
                "created_at": convert_str_to_date(record["created_at"]),
                "status": record["status"],
            }

            self.user_records[user_id].append(new_record)

        def sort_function(e):
            return e["created_at"]

        for user_id in self.user_records:
            self.user_records[user_id].sort(key=sort_function)

    def get_status(self, user_id, date):
        status = NP

        if type(date) == str:
            date = convert_str_to_date(date)

        if user_id not in self.user_records:
            return NP

        for record in self.user_records[user_id]:
            if record["created_at"] <= date:
                status = record["status"]

        return status


class IpRangeSearch:
    RANGES = {
        "London": [
            {"start": "10.10.0.0", "end": "10.10.255.255"},
            {"start": "192.168.1.0", "end": "192.168.1.255"},
        ],
        "Munich": [
            {"start": "10.12.0.0", "end": "10.12.255.255"},
            {"start": "172.16.10.0", "end": "172.16.11.255"},
            {"start": "192.168.2.0", "end": "192.168.2.255"},
        ],
    }

    def __init__(self):
        pass

    def parse_ip(self, ip):
        return [int(i) for i in ip.split(".")]

    def ip_in_range(self, ip, ip_range):
        ip_address = self.parse_ip(ip)
        start_address = self.parse_ip(ip_range["start"])
        end_address = self.parse_ip(ip_range["end"])

        for i in range(0, 4):
            if ip_address[i] < start_address[i]:
                return False
            if ip_address[i] > end_address[i]:
                return False

        return True

    def get_city(self, ip):
        for city_name, city in self.RANGES.items():
            for ip_range in city:
                if self.ip_in_range(ip, ip_range):
                    return city_name
        return "unknown"


class AggregateUserCity:
    def __init__(self):
        self.user_status_search = UserStatusSearch()
        self.ip_range_search = IpRangeSearch()
        self.transactions = []

        with open("transactions.json", "r") as transactions_file:
            lines = transactions_file.readlines()
            for line in lines:
                self.transactions.append(json.loads(line))

    def check_transaction_status(self, transaction, status):
        user_id = transaction["user_id"]
        created_at = transaction["created_at"]
        t_status = self.user_status_search.get_status(user_id, created_at)
        return status == t_status

    def check_transaction_city(self, transaction, city):
        ip = transaction["ip"]
        t_city = self.ip_range_search.get_city(ip)
        return t_city == city

    def get_aggregate(self, status, city):
        product_price = 0

        for transaction in self.transactions:
            if not self.check_transaction_status(transaction, status):
                continue
            if not self.check_transaction_city(transaction, city):
                continue

            product_price += transaction["product_price"]

        return product_price


app = Flask(__name__)


@app.route("/user_status")
def user_status():
    """Return user status for a given date"""
    user_id = int(request.args.get("user_id"))
    date = convert_str_to_date(str(request.args.get("date")))

    user_status_search = UserStatusSearch()
    user_status = user_status_search.get_status(user_id, date)

    return jsonify({"user_status": user_status})


@app.route("/ip_city")
def ip_city():
    """Return city for a given ip"""
    ip = str(request.args.get("ip"))

    ip_range_search = IpRangeSearch()
    city = ip_range_search.get_city(ip)

    return jsonify({"city": city})


@app.route("/user_city")
def user_city():
    """Return aggregated sum of the product price for the given user status
    and city"""
    status = str(request.args.get("user_status"))
    city = str(request.args.get("city"))

    aggregate_user_city = AggregateUserCity()
    product_price = aggregate_user_city.get_aggregate(status, city)

    return jsonify({"product_price": product_price})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")
