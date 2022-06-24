# Stori Take Home Test - Project interface

## Requirements

- Use of a HTTP request library (`Python` `Requests`, `CURL`, etc) or a GUI API testing tool (`Postman`, `Insomnia`, etc).
- Active Internet connection.
- *Real email address account* able to receive messages.

## Steps

1. Create an user.
2. Get an email with user's summary.
3. Call for transaction's JSON or download CSV file.
4. Repeat with a new user.

Note:

- All calls should be made to this base url: `https://rqva7y6toj.execute-api.us-east-1.amazonaws.com/stori-take-home-test`
- Beware that all endpoint urls have ending trailing slash.


### Create an user

Method: Endpoint
``` bash
POST: /user/
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
  },
  "txs": 473
}
```

### Get an email with user's summary
Method: Endpoint
```bash
POST: /send-email/{user_id}/
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
POST: /txs/{user_id}/{format<json|csv>}/
```
Payload
```
N/A
```

Returns

If format is CSV, returns a binary file to download.*

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

## Other endpoints

- `GET: /user/{user_id}/`
- `DELETE: /user/{user_id}/`



## Caveats & Known issues
- Database is non-persistent, so any user/transactions created will be deleted after a short time window. If you want to try again, please start over.
- Email is sent through sender address `no-reply@wem.mx`. Please look into Junk/spam folder if mail is not into inbox.
- `send-email` endpoint is the 'slowest'. I made another project on the fly to process and generate the chart located at the bottom of the email message. This connection is a VPS outside AWS ecosystem.
- *CSV file is downloading wrongly enconded in base64 —you could decode it to confirm. Didn't got time to debbug this properly.

