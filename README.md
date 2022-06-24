# Stori Take Home Test - Project interface

## Requirements

- Use of a HTTP request library (`Python` `Requests`, `CURL`, etc) or a GUI API testing tool (`Postman`, `Insomnia`, etc).
- Active Internet connection.
- *Real email address* account able to receive messages.

## Steps

1. Create an user.
2. Get an email with user's summary.
3. Download transactions' CSV or JSON.

Note:

All calls should be made to this base url: `https://rqva7y6toj.execute-api.us-east-1.amazonaws.com/stori-take-home-test/`


### Create an user

Method: Endpoint
``` bash
POST: user/
```

Payload (JSON)
```json
{
  "name": "Your name",
  "email": "valid@address.com"
}
```

Returns
```json
{
  "result": "Success",
  "data": {
    "id": 1,
    "email": "valid@address.com",
    "name": "Your name"
  }
  "txs": 473
}
```

### Get an email with user's summary
Method: Endpoint
```bash
POST: send-email/{user_id}
```

Payload
```
N/A
```

Response
```json
{
  "result": "Success",
  "message": "Email sent to User {user_data.id}."
}
```

### Download transactions' CSV file or JSON response
Method: Endpoint
```bash
POST: txs/{user_id}/{format<json|csv>}
```
Payload
```
N/A
```

Returns

If format is CSV, returns a binary file to download.

If format is JSON, this is the response:

```json
{
"result": "Success",
"data": [
  {
    "id": 1,
    "owner_id": 1,
    "amount": "-307.17",
    "date": "2022-01-01 09:15:36.000000"
  },
  {
    "id": 2,
    "owner_id": 1,
    "amount": "-77.6",
    "date": "2022-01-01 18:31:12.000000"
  },
  {
    "id": 3,
    "owner_id": 1,
    "amount": "-129.53",
    "date": "2022-01-04 02:04:48.000000"
  },
  ...
  ]
}
```

## Caveats
- Database is non-persistent, so any user/transactions created will be deleted after some time. If you want to try again, please start over.
- Email is sent through sender address `no-reply@wem.mx`. Please look into Junk/spam folder if mail is not into inbox.

## Other endpoints

- `GET: user/{user_id}`
- `DELETE: user/{user_id}`