from flask import request, jsonify
from config import create_app, db
from models import Episode, Guest, Appearance

app = create_app()


@app.route("/")
def home():
    return {"message": "Late Show API Running"}


# ======================
# GET /episodes
# ======================
@app.route("/episodes", methods=["GET"])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([
        ep.to_dict(only=("id", "date", "number"))
        for ep in episodes
    ])


# ======================
# GET /episodes/<id>
# ======================
@app.route("/episodes/<int:id>", methods=["GET"])
def get_episode(id):
    episode = Episode.query.get(id)

    if not episode:
        return {"error": "Episode not found"}, 404

    # serialize_rules in models control nesting
    return jsonify(episode.to_dict())


# ======================
# GET /guests
# ======================
@app.route("/guests", methods=["GET"])
def get_guests():
    guests = Guest.query.all()
    return jsonify([
        guest.to_dict(only=("id", "name", "occupation"))
        for guest in guests
    ])


# ======================
# POST /appearances
# ======================
@app.route("/appearances", methods=["POST"])
def create_appearance():
    data = request.get_json()

    try:
        new_appearance = Appearance(
            rating=data["rating"],
            episode_id=data["episode_id"],
            guest_id=data["guest_id"]
        )

        db.session.add(new_appearance)
        db.session.commit()

        # serialize_rules will include episode and guest
        return jsonify(new_appearance.to_dict()), 201

    except Exception:
        db.session.rollback()
        return {"errors": ["validation errors"]}, 400


if __name__ == "__main__":
    app.run(debug=True)
