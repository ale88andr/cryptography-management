import datetime
from typing import Annotated

from sqlalchemy import String, Date, text
from sqlalchemy.orm import mapped_column


pk = Annotated[
    int,
    mapped_column(primary_key=True)
]

created_at = Annotated[
    datetime.datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())"))
]

updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    )
]

title = Annotated[
    str,
    mapped_column(String(50), nullable=False, unique=True)
]

date = Annotated[
    datetime.date,
    mapped_column(Date, nullable=True)
]

required_date = Annotated[
    datetime.date,
    mapped_column(Date, nullable=False)
]
