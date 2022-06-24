from fastapi import FastAPI, Request
from mangum import Mangum
from starlette.responses import FileResponse

from stori.config import csv_filepath, email_subject
from stori.crud import create_user, delete_user, get_txs, get_user, get_user_by_email
from stori.database import Base, engine
from stori.generator import generate_txs
from stori.helpers import from_db_to_df, get_db
from stori.sender import process_data, send_email

Base.metadata.create_all(bind=engine)
app = FastAPI()


def user_exist(user_id):
    db = get_db()
    user_data = get_user(db, user_id)
    return bool(user_data)


@app.post("/user/")
async def create_user_endpoint(request: Request):
    """Create user"""
    db = get_db()
    body = await request.json()
    email = get_user_by_email(db, body["email"])
    if not email:
        user_data = create_user(db, body)
        user_data = get_user(db, user_data.id)
        txs = generate_txs()
        txs["owner_id"] = user_data.id
        len_txs = txs.to_sql("transactions", engine, if_exists="append", index=False)
        return {"result": "Success", "message": f"User {user_data.id} created. {len_txs} transactions generated."}
    else:
        return {"result": "Failed", "message": f"User {email.id} already created"}


@app.get("/user/{user_id}/")
async def get_user_endpoint(user_id: int):
    """Get user information by id"""
    if user_exist(user_id):
        db = get_db()
        user_data = get_user(db, user_id)
        txs = get_txs(db, user_id)
        return {"result": "Success", "data": user_data, "txs": len(txs)}
    else:
        return {"result": "Failed"}


@app.delete("/user/{user_id}/")
async def delete_user_endpoint(user_id: int):
    """Delete user"""
    if user_exist(user_id):
        db = get_db()
        delete_user(db, user_id)
        return {"result": "Success", "message": f"User {user_id} and their transactions deleted."}
    else:
        return {"result": "Failed"}


@app.get("/txs/{user_id}/{format}/")
async def txs_user_csv_endpoint(user_id: int, format: str):
    """Get user transactions"""
    if user_exist(user_id):
        db = get_db()
        txs = get_txs(db, user_id)
        if format == "csv":
            df = from_db_to_df(txs)
            df.to_csv(csv_filepath, mode="w", index=False)
            return FileResponse(csv_filepath, media_type="application/octet-stream", filename="txs.csv")
        else:
            return {"result": "Success", "data": txs}
    else:
        return {"result": "Failed"}


@app.post("/send-email/{user_id}/")
async def get_user_endpoint(user_id: int):
    """Send email"""
    if user_exist(user_id):
        db = get_db()
        txs = get_txs(db, user_id)
        df = from_db_to_df(txs)
        user_data = get_user(db, user_id)
        em = send_email(
            user_data.email,
            email_subject,
            process_data(user_data.name, df),
        )
        if len(em):
            return {"result": f"Success", "message": f"Email sent to User {user_data.id}."}
        else:
            return {"result": "Failed"}
    else:
        return {"result": "Failed"}


handler = Mangum(app)
