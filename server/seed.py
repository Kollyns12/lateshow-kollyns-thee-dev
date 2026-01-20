from config import create_app, db
from models import Episode, Guest, Appearance

app = create_app()

with app.app_context():

    # Clear tables (order matters because of FK constraints)
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    # Episodes
    e1 = Episode(date="1/11/99", number=1)
    e2 = Episode(date="1/12/99", number=2)

    # Guests
    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Tracey Ullman", occupation="television actress")

    db.session.add_all([e1, e2, g1, g2])
    db.session.commit()

    # Appearances
    a1 = Appearance(rating=4, episode=e1, guest=g1)
    a2 = Appearance(rating=5, episode=e2, guest=g2)

    db.session.add_all([a1, a2])
    db.session.commit()

    print("Database seeded successfully!")
