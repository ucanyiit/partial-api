from api import app, P
from flask import json


def test_user_status(user_id, date, expected):
    response = app.test_client().get(
        "/user_status?user_id=" + user_id + "&date=" + date,
        content_type="application/json",
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["user_status"] == expected


def test_user_city(status, city, expected):
    response = app.test_client().get(
        "/user_city?user_status=" + status + "&city=" + city,
        content_type="application/json",
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["product_price"] == expected


def test_ip_city(ip, expected):
    response = app.test_client().get(
        "/ip_city?ip=" + ip,
        content_type="application/json",
    )

    data = json.loads(response.get_data(as_text=True))

    assert response.status_code == 200
    assert data["city"] == expected


def main():
    test_user_status(str(1), "2017-01-01T10:00:00", P)
    test_ip_city("10.12.0.100", "Munich")
    test_user_city(P, "Munich", 594.0)


if __name__ == "__main__":
    main()
