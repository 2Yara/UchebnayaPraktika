from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # разрешаем запросы с других доменов

# Временное хранилище — список словарей
notes = []
next_id = 1


def find_note(note_id):
    return next((n for n in notes if n['id'] == note_id), None)


@app.route('/notes', methods=['GET'])
def get_notes():
    return jsonify(notes), 200


@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404, description="Note not found")
    return jsonify(note), 200


@app.route('/notes', methods=['POST'])
def create_note():
    global next_id
    if not request.is_json:
        abort(400, description="Request must be JSON")
    data = request.get_json()
    if 'title' not in data or 'content' not in data:
        abort(400, description="title and content are required")
    note = {
        'id': next_id,
        'title': data['title'],
        'content': data['content']
    }
    notes.append(note)
    next_id += 1
    return jsonify(note), 201


@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = find_note(note_id)
    if note is None:
        abort(404, description="Note not found")
    if not request.is_json:
        abort(400, description="Request must be JSON")
    data = request.get_json()
    note['title'] = data.get('title', note['title'])
    note['content'] = data.get('content', note['content'])
    return jsonify(note), 200


@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    global notes
    note = find_note(note_id)
    if note is None:
        abort(404, description="Note not found")
    notes = [n for n in notes if n['id'] != note_id]
    return jsonify({'message': 'Note deleted'}), 200


if __name__ == '__main__':
    app.run(debug=True)