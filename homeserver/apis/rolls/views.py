"""Create, Read, Update, Delete data from the model for user data."""

from homeserver.core.utility import debug_print
from flask import request, url_for
from homeserver.models import Role as Role_data
from flask_restplus import Resource
from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError
from validate_email import validate_email
from flask_accepts import accepts
from homeserver.apis import api, db
debug_print(__file__, '<')


ns = api.namespace('roles', description='Roles maintenance')
ma = Marshmallow()


class RoleSchema(ma.ModelSchema):
    class Meta:
        model = Role_data


class RoleSchemaPost(ma.ModelSchema):
    class Meta:
        model = Role_data

        # Fields to expose
        fields = ("name", "email", "desc")

    @validates("name")
    def name_validator(self, value):
        debug_print(__name__)
        print(f"Name: {value}")
        if not value and value != 'string':
            raise ValidationError(f"Name cannot be empty.")

    @validates("email")
    def email_validator(self, value):
        #   Allow empty email address and check syntax
        if value and value != 'string':
            is_valid = validate_email(value)
            if not is_valid:
                raise ValidationError(f"{value} is not a valid email address.")


@api.doc('List the valid roles')
@ns.route('/roles')
class RoleList(Resource):
    def get(self):
        """Get the list of roles"""
        roles = Role_data.query.all()
        if roles is not None:
            role_schema = RoleSchema(many=True)
            results = role_schema.dump(roles).data
            return {'roles': results}, 200

        api.abort(404)

    @accepts(schema=RoleSchemaPost, api=api)
    @api.response(201, 'Success')
    @api.response(409, 'Error saving the role')
    def post(self):
        """Add a new role."""
        debug_print(__name__)
        new_role = request.parsed_obj
        db.session.add(new_role)
        db.session.commit()
        url = url_for('roles_role', id=new_role.id, _external=True)
        # url = f'/roles/{new_role.id}'
        return {'reference': f'{url}'}, 201


@api.doc('Get an individual role')
@ns.route('/role/<id>')
class Role(Resource):
    def get(self, id):
        """Get role based on id"""
        role = Role_data.query.filter_by(id=id).first()
        if (role):
            role_schema = RoleSchema()
            results = role_schema.dump(role)
            return {'roles': results.data}, 200

        return ['message', 'role not found'], 404

    def delete(self, id):
        """Delete this role based on id"""
        role = Role_data.query.filter_by(id=id).first()
        if (role):
            db.session.delete(role)
            db.session.commit()
            return {'message': f'Role {id}, {role.name} has been removed.'}

        return ['message', 'role not found'], 404


debug_print(__file__)
