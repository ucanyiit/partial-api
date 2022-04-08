# Partial API Task
## Running Project

You can run the project using Docker if you have it installed on your system:

```
docker-compose up
```

Or you can use python directly.

```
pip install -r requirements.txt
python api.py
```

## Tests

You can run the tests using:

```
python tests.py
```

## Tasks

1. `/user_status`

In the initialization, the `UserStatusSearch` class groups the records according to their `user_id`s. Then it sorts those records according to their `created_at` times. In the process, it converts the dates from `str` to `date` format.

In the `get_status` function it first sets the result variable `status` to `NP`. Then it iterates over all of the dates for the given `user_id` and sets `status` if the date is before the given date. (We can use the binary search here since the records are sorted)

2. `/ip_city`

`get_city` method iterates over all of the cities in the `RANGES` and `ip_range`s for each city. It checks it using the `ip_in_range` function. If this function returns `True`, it simply returns the corresponding `city_name`.

If, in the end, there are no cities within the given range, the function returns `unknown`.

3. `/user_city`

In initialization, it creates the 2 classes that are used for previous endpoints (`UserStatusSearch` and `IpRangeSearch`). Afterward, it reads the `transactions.json` file and saves the data into a dictionary named `transactions`.

The `get_aggegate` function checks transaction status using `check_transaction_status` and transaction city using `check_transaction_city`. Those functions call the corresponding class. If both of them return `True`, it adds the `product_price`s into the return variable.

## Goal

For this assignment, you are expected to implement the missing parts 
in the `api.py` file. 

Our goal is to see how you implement the missing parts of the API and how you
deal with file processing and data structures manipulation.

Please provide the code in a way that you would push to production.

## Task description

There are three API endpoints that need to be implemented:

1. `/user_status`

Description:

On this endpoint please provide an implementation that searches the records and
returns the correct `user_status` at the given date. You can imagine the
records as single events which get fired on a user status change. If a user
starts paying, there will be one record stored with status `paying`, whereas if
this user finishes paying, there will be another record added with status
`completed`. Consequently, a user remains in status `paying` until the next
`completed` event. In case there is no status available for a specific date,
simply return `non-paying`. The valid responses that should be provided are:
`paying`, `completed` or `non-paying`.

Required GET parameters:
- `user_id` (int)
- `date` (datetime)

Example request:

`/user_status?user_id=1&date=2017-01-01T10:00:00`

Example response:

```json
{
  "user_status": "paying"
}
```

2. `/ip_city`

Description:

On this endpoint please provide an implementation that searches the provided IP
ranges and returns the correct city based on the IP. In case the IP range is
not within any of the provided cities, `unknown` should be returned.

Required GET parameters:
- `ip` (str)

Example request:

`/ip_city?ip=10.12.0.100`

Example response:

```json
{
  "city": "Munich"
}
```

3. `/user_city`

Description:

Please read the `transactions.json` file and enrich it with the data given by
the API. This endpoint should provide an aggregate containing the
sum of `product_price` grouped by the given `user_status` and `city`.

Required GET parameters:
- `user_status` (string)
- `city` (string)

Example request:

`/user_city?user_status=paying&city=Munich`

Example response:

```json
{
  "product_price": 123456 
}
```

Note that this is just an example and not a real answer from API.

## Setup

There is a simple `requirements.txt` file which you'll need to install. 
Then simply run the `api.py` file.

```
pip install -r requirements.txt
python api.py
```

### Delivery

Please provide a link of your solution via a public Github repository.

### Bonus points

- PEP-8 conventions are followed
- Unit tests are included 
- Application is containerized with Docker
- A README.md file is included containing the instructions, thinking process 
  and assumptions (if any).
