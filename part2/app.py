from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
CORS(app)  # разрешаем запросы с других доменов

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:exam@localhost:5432/notes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        """Удобное представление заметки в виде словаря для JSON."""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
        }


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error.description)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error.description)}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/notes', methods=['GET'])
def get_notes():
    title_filter = request.args.get('title')
    content_filter = request.args.get('content')
    search_filter = request.args.get('search')

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = Note.query

    if title_filter:
        query = query.filter(Note.title.ilike(f'%{title_filter}%'))

    if content_filter:
        query = query.filter(Note.content.ilike(f'%{content_filter}%'))

    if search_filter:
        query = query.filter(
            or_(
                Note.title.ilike(f'%{search_filter}%'),
                Note.content.ilike(f'%{search_filter}%'),
            )
        )

    paginated = query.order_by(Note.id).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        'notes': [note.to_dict() for note in paginated.items],
        'total': paginated.total,
        'pages': paginated.pages,
        'current_page': paginated.page,
        'per_page': paginated.per_page,
    }), 200


# GET /notes/<id> — одна заметка
@app.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        abort(404, description=f'Note with id={note_id} not found')
    return jsonify(note.to_dict()), 200


# POST /notes — создать заметку
@app.route('/notes', methods=['POST'])
def create_note():
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()

    if 'title' not in data or 'content' not in data:
        abort(400, description='Fields "title" and "content" are required')

    if not data['title'].strip() or not data['content'].strip():
        abort(400, description='Fields "title" and "content" cannot be empty')

    new_note = Note(title=data['title'], content=data['content'])
    db.session.add(new_note)
    db.session.commit()

    return jsonify(new_note.to_dict()), 201


# PUT /notes/<id> — обновить заметку
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        abort(404, description=f'Note with id={note_id} not found')

    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()

    if 'title' in data:
        if not data['title'].strip():
            abort(400, description='Field "title" cannot be empty')
        note.title = data['title']

    if 'content' in data:
        if not data['content'].strip():
            abort(400, description='Field "content" cannot be empty')
        note.content = data['content']

    db.session.commit()
    return jsonify(note.to_dict()), 200


# DELETE /notes/<id> — удалить заметку
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = db.session.get(Note, note_id)
    if note is None:
        abort(404, description=f'Note with id={note_id} not found')

    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': f'Note with id={note_id} deleted'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)