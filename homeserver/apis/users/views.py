"""Create, Read, Update, Delete data from the model for user data."""

from homeserver.core.utility import debug_print
from homeserver.models import User as User_data, Role as Role_data
from flask_restplus import Resource, fields
from homeserver.apis import api
debug_print(__file__, '<')


ns = api.namespace('user', description='User maintenance')

user_model = api.model('User', {
    # 'id': fields.Integer(required=False, description='The user primary key'),
    'name': fields.String(required=True, unique=True,
                          description='The user name'),
    'email': fields.String(required=False, description="The user's name"),
    'password': fields.String(required=False,
                              description="The user's password"),
    'roll_id': fields.Integer(required=False, description="The user's roll"),
    'reset_token': fields.String(),
    'updated': fields.DateTime(required=False,
                               description='Time last created or updated'),
})

role_model = api.model('Role', {
    # 'id': fields.Integer(required=False, description='Primary Key'),
    'name': fields.String(required=True, unique=True,
                          description="The role''s name"),
    'desc': fields.String(required=False,
                          description='Description of the role'),
    'updated': fields.DateTime(required=False, description='Date last updated')
})


@api.doc('List the users.')
@ns.route('/')
class UserList(Resource):
    @api.marshal_with(user_model, as_list=True, envelope='Users')
    def get(self):
        """List all the users information"""
        users = User_data.query.all()
        if users is not None:
            print(f'Found Users')
            return users

        api.abort(404)

    @api.expect(user_model)
    def post(self):
        """Add the new user."""
        data = api.re
        return {'response': 'New user added.'}, 201


@api.doc('Maintain the user table data')
@ns.route('/<int:id>')
class User(Resource):
    @api.marshal_with(user_model, envelope='User')
    def get(self, id):
        """Get the user information"""
        user = User_data.query.filter_by(id=id).first()
        if (user):
            print(f"User {id} found...")
            return user, 200
        else:
            print(f'User: {id} not found.')
            return {'message': 'User not found.'}, 404

        api.abort(404)


@api.doc('List the valid roles')
@ns.route('/roles')
class RoleList(Resource):
    @api.marshal_with(role_model)
    def get(self):
        """Get the list of roles"""
        roles = Role_data.query.all()
        if roles is not None:
            print(f'Found roles')
            return roles

        api.abort(404)


@api.doc('Get and individual valid role')
@ns.route('/role/<id>')
class Role(Resource):
    @api.marshal_with(role_model)
    def get(self, id):
        """Get role based on id"""
        role = Role_data.query.filter_by(id=id).first()
        if (role):
            print(f'Found role: {Role_data.id}')
            return role, 200
        else:
            print(f'Role {id} not found')
            return ['message', 'role not found'], 404


debug_print(__file__)
