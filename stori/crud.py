from sqlalchemy.orm import Session

from stori.database import Tx, User


def get_user(db: Session, user_id: int):
    """Query user by id"""
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_user_by_email(db: Session, email: str):
    """Query user by email"""
    user = db.query(User).filter(User.email == email).first()
    return user


def create_user(db: Session, user: dict):
    """Create user with dict"""
    db_user = User(name=user["name"], email=user["email"])
    db.add(db_user)
    db.commit()
    return db_user


def delete_user(db: Session, user_id: int):
    """Delete user by id"""
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def get_txs(db: Session, user_id: int):
    """Query transactions from user id"""
    return db.query(Tx).filter(Tx.owner_id == user_id).limit(None).all()
