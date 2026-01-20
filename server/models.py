from sqlalchemy import CheckConstraint
from sqlalchemy_serializer import SerializerMixin
from config import db

# ======================
# Episode Model
# ======================
class Episode(db.Model, SerializerMixin):
    __tablename__ = "episodes"

    serialize_rules = ("-appearances.episode",)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    appearances = db.relationship(
        "Appearance",
        back_populates="episode",
        cascade="all, delete-orphan"
    )


# ======================
# Guest Model
# ======================
class Guest(db.Model, SerializerMixin):
    __tablename__ = "guests"

    serialize_rules = ("-appearances.guest",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    appearances = db.relationship(
        "Appearance",
        back_populates="guest",
        cascade="all, delete-orphan"
    )


# ======================
# Appearance Model
# ======================
class Appearance(db.Model, SerializerMixin):
    __tablename__ = "appearances"

    serialize_rules = ("-episode.appearances", "-guest.appearances")

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)

    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"))
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"))

    episode = db.relationship("Episode", back_populates="appearances")
    guest = db.relationship("Guest", back_populates="appearances")

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="rating_range"),
    )
