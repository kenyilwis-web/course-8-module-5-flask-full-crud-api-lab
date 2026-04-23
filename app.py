from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events])

@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event.to_dict())

@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    title = data['title']
    if events:
        new_id = max(e.id for e in events) + 1
    else:
        new_id = 1
    new_event = Event(new_id, title)
    events.append(new_event)
    return jsonify(new_event.to_dict()), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if 'title' in data:
        event.title = data['title']
    return jsonify(event.to_dict()), 200

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404
    events.remove(event)
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
