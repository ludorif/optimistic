#  Copyright (c) 2025 Ludovic Riffiod
#
from fastapi import Depends
from sqlalchemy import Column, String, text
from sqlalchemy.orm import relationship, Session

from .sql_model import User


def add_user_if_missing( client_uuid, session: Session ):
    result = session.execute(
        text("SELECT * FROM users WHERE uuid = :client_id "),
        {"client_id": client_uuid}  # safe binding
    )

    exists = result.fetchall()

    if not exists:
        user = User(
            uuid=client_uuid
        )
        session.add(user)
        session.commit()

