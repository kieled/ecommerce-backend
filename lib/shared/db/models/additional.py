from sqlalchemy.orm import mapped_column, Mapped
from ..config import Base


class Settings(Base):
    __tablename__ = 'settings'

    id: Mapped[int] = mapped_column(primary_key=True)

    admin_chat_id: Mapped[str | None]
