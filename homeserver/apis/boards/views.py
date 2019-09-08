"""Create, Read, Update, Delete data from the model for boards data."""

from homeserver.core.utility import debug_print
from homeserver.models import Board as Board_data
from flask import request, url_for
from flask_restplus import Resource
from flask_accepts import accepts
from homeserver.apis import api, db
from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError
debug_print(__file__, '<')


ns = api.namespace('boards', description='Boards and Components maintenance')
ma = Marshmallow()


class BoardSchema(ma.ModelSchema):
    class Meta:
        model = Board_data


class BoardSchemaPost(ma.ModelSchema):
    class Meta:
        model = Board_data

        # Fields to expose
        fields = ("desc", "ucontroller_id", "secret",
                  "prime_location",
                  "location",
                  "sub_location",
                  "active",
                  "updated")

    @validates("prime_location")
    def email_validator(self, value):
        #   Only allow in or out doors
        if value not in ['', 'in', 'out']:
            raise ValidationError(f"{value} prime location my be 'in' or 'out'.")


@api.doc('List the Boards.  Active Only flag is false when 0 (zero)')
@ns.route('/')
class BoardList(Resource):
    def get(self):
        """List all the boards information"""
        boards = Board_data.query.all()
        if boards is not None:
            board_schema = BoardSchema(many=True)
            results = board_schema.dump(boards)
            return {'boards': results}, 200

        return {'message': 'No data available.'}, 204

    @accepts(schema=BoardSchemaPost, api=api)
    def post(self):
        """Add the new board."""
        new_board = request.parsed_obj
        debug_print(__name__)
        print(f"New Board: {new_board}")

        db.session.add(new_board)
        db.session.commit()
        url = url_for('boards_board', id=new_board.id, _external=True)
        return {'reference': f'{url}'}, 201



@api.doc('Display the details of a single board.')
@ns.route('/<int:id>')
class Board(Resource):
    """Display a board and its corresponding information"""

    def get(self, id):
        """Retrieve an individual board"""
        boards = Board_data.query.filter_by(id=id).first()
        if (boards is not None):
            board_schema = BoardSchema()
            results = board_schema.dump(boards)
            return {'boards': results}, 200

        return {'message': 'No boards found.'}, 404

    def delete(self, id):
        """Delete this board based on id"""
        board_to_del = Board_data.query.filter_by(id=id).first()
        if (board_to_del):
            db.session.delete(board_to_del)
            db.session.commit()
            return {'message':
                    f'Board {id}, {board_to_del.desc} has been removed.'}

        return ['message', 'role not found'], 404


debug_print(__file__)
