"""Create, Read, Update, Delete data from the model for user data."""

from homeserver.core.utility import debug_print
from flask import request, url_for
from homeserver.models import User as User_data
from flask_restplus import Resource
from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError
from validate_email import validate_email
from flask_accepts import accepts
from homeserver.apis import api, db
debug_print(__file__, '<')


ns = api.namespace('user', description='User maintenance')
ma = Marshmallow()


class UserSchema(ma.ModelSchema):

    class Meta:
        model = User_data

        # Fields to expose
        fields = ("id", "name", "email", "roll_id", "updated")

    @validates("name")
    def name_validator(self, value):
        if not value:
            raise ValidationError(f"Name cannot be empty.")        

    @validates("email")
    def email_validator(self, value):
        #   Allow empty email address and check syntax
        if value:
            is_valid = validate_email(value)
            if not is_valid:
                raise ValidationError(f"{value} is not a valid email address.")


class UserSchemaPost(ma.ModelSchema):

    class Meta:
        model = User_data

        # Fields to expose
        fields = ("name", "email", "password", "roll_id", "updated")

    @validates("name")
    def name_validator(self, value):
        debug_print(__name__)
        print(f"")
        if not value and value != 'string':
            raise ValidationError(f"Name cannot be empty.")

    @validates("email")
    def email_validator(self, value):
        #   Allow empty email address and check syntax
        if value and value != 'string':
            is_valid = validate_email(value)
            if not is_valid:
                raise ValidationError(f"{value} is not a valid email address.")


@api.doc('List the users.')
@ns.route('/')
class UserList(Resource):
    def get(self):
        """List all the users information"""
        users = User_data.query.all()
        if users is not None:
            n = 0
            for user in users:
                n += 1
            user_schema = UserSchema(many=True)
            result = user_schema.dump(users)
            debug_print(__name__)
            return {'users': result.data}, 200

        return {'status': 'success'}, 201

    @accepts(schema=UserSchemaPost, api=api)
    @api.response(201, 'Success')
    @api.response(409, 'Error saving the user')
    def post(self):
        """Add a new user."""
        debug_print(__name__)

        new_user = request.parsed_obj

        #   Check if we already have this user
        test_user = User_data.query.filter_by(name=new_user.name).first()
        if test_user is None:
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as err:
                error_msg = f'Error saving User - {new_user.name}/n{err.__cause__}'
                print(error_msg)
                return {'message': error_msg}, 409

            user_schema = UserSchemaPost()
            msg = user_schema.dump(new_user)
            http_response = 201
            link = url_for("user_user", name=new_user.name, _external=True)
            return {'message': msg, 'reference': link}, http_response

        #   This user already exists.  Return the reference
        msg = f'User {new_user.name} already exists.'
        http_response = 409
        link = url_for("user_user", name=new_user.name, _external=True)
        return {'message': msg, 'reference': link}, http_response


@ns.route('/<name>/')
@api.doc(params={'name': 'Name of an individual user'})
class User(Resource):
    @api.doc('View the data for a single user.')
    def get(self, name):
        """Get the user information"""
        user = User_data.query.filter_by(name=name).first()
        if (user):
            user_schema = UserSchema()
            result = user_schema.dump(user).data
            return {'users': result}, 200

        return {'message': 'User not found.'}, 404

        api.abort(404)

    @accepts(schema=UserSchemaPost, api=api)
    def put(self, name):
        #   Check user exists
        if name:
            user_to_update = User_data.query.filter_by(name=name).first()
            if user_to_update:
                return {'message': f'User {name} has been updated.'}

        #   No user by that name
        return {'message': 'User not found.'}, 404

    def delete(self, name):
        #   Check user exists
        if name:
            user_to_delete = User_data.query.filter_by(name=name).first()
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
                return {'message': f'User {name} has been removed.'}

        #   No user by that name
        return {'message': 'User not found.'}, 404


debug_print(__file__)
