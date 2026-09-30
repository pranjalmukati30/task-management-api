from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(String(100))
    email : Mapped[str] = mapped_column(String(150))
    password_hash : Mapped[str] = mapped_column(String(255))

    projects: Mapped[list["Project"]] = relationship()


class Project(Base):
    __tablename__ = "projects"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100))
    description : Mapped[str | None] = mapped_column(String(250))
    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner : Mapped["User"] = relationship()


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(50))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"))