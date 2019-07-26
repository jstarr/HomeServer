"""Create, Read, Update, Delete data from the model for user data."""

from homeserver.core.utility import debug_print
from homeserver.models import Board as Board_data
from flask_restplus import Resource, fields
from homeserver.apis import api
debug_print(__file__, '<')


ns = api.namespace('boards', description='Boards and Components maintenance')

board_model = api.model('Board', {
    # 'id': fields.Integer(required=False, description='The user primary key'),
    'desc': fields.String(required=True, unique=True,
                          description='Description of the board'),
    'ucontroller_id': fields.Integer(required=False,
                                     description='MicroController'),
    'secret': fields.String(required=False,
                            description='Secret pass code for this board.'),
    'prime_location': fields.String(required=False,
                                    description="'in' or 'out' as in indoor & outdoor"),
    'location': fields.String(required=False,
                              description="Where the board is located e.g. 'room 1'"),
    'sub_location': fields.String(required=False,
                                  description="secondary board location e.g. ' east wall '"),
    'active': fields.Boolean(default=False, description="Board is actively sending data."),
    'vendor_id': fields.Integer(required=False,
                                description="Vendor where board was purchased"),
    'manufacturer_id': fields.Integer(required=False,
                                      description="Who made the board"),
    'updated': fields.DateTime(required=False,
                               description='Time last created or updated',
                               dt_format='rfc822')
})


@api.doc('List the users.')
@ns.route('/')
class BoardList(Resource):
    @api.marshal_with(board_model, as_list=True, envelope='boards')
    def get(self):
        """List all the boards information"""
        boards = Board_data.query.all()
        if boards is not None:
            print(f'Found Boards')
            return boards

        api.abort(404)

    @api.expect(board_model)
    def post(self):
        """Add the new board."""
        # data = api.
        return {'response': 'New board added.'}, 201


debug_print(__file__)
