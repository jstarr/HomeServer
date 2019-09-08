"""Create, Read, Update, Delete data from the model for vendor data."""

from homeserver.core.utility import debug_print
from flask import request, url_for
from homeserver.models import Vendor as Vendor_data
from flask_restplus import Resource
from flask_marshmallow import Marshmallow
from marshmallow import validates, ValidationError
from validate_email import validate_email
from flask_accepts import accepts
from homeserver.apis import api, db
debug_print(__file__, '<')


ns = api.namespace('vendor', description='Vendor maintenance')
ma = Marshmallow()


class VendorSchema(ma.ModelSchema):

    class Meta:
        model = Vendor_data

        # Fields to expose
        fields = ("id", "name", "street1", "street2", "city", "state", "zip",
                  "country", "phone", "url")

    @validates("name")
    def name_validator(self, value):
        if not value:
            raise ValidationError(f"Name cannot be empty.")        


class VendorSchemaPost(ma.ModelSchema):

    class Meta:
        model = Vendor_data

        # Fields to expose
        fields = ("name", "street", "street1", "street2", "city",
                  "state", "zip", "country", "phone", "url")

    @validates("name")
    def name_validator(self, value):
        debug_print(__name__)
        print(f"")
        if not value and value != 'string':
            raise ValidationError(f"Name cannot be empty.")


@api.doc('List the vendors.')
@ns.route('/')
class VendorList(Resource):
    def get(self):
        """List all the vendors information"""
        vendors = Vendor_data.query.all()
        if vendors is not None:
            n = 0
            for vendor in vendors:
                n += 1
            vendor_schema = VendorSchema(many=True)
            result = vendor_schema.dump(vendors)
            debug_print(__name__)
            return {'vendors': result.data}, 200

        return {'status': 'success'}, 201

    @accepts(schema=VendorSchemaPost, api=api)
    @api.response(201, 'Success')
    @api.response(409, 'Error saving the vendor')
    def post(self):
        """Add a new vendor."""
        debug_print(__name__)

        new_vendor = request.parsed_obj

        #   Check if we already have this vendor
        test_vendor = Vendor_data.query.filter_by(name=new_vendor.name).first()
        if test_vendor is None:
            try:
                db.session.add(new_vendor)
                db.session.commit()
            except Exception as err:
                error_msg = f'Error saving Vendor - {new_vendor.name}/n{err.__cause__}'
                print(error_msg)
                return {'message': error_msg}, 409

            vendor_schema = VendorSchemaPost()
            msg = vendor_schema.dump(new_vendor)
            http_response = 201
            link = url_for("vendor_vendor", name=new_vendor.name, _external=True)
            return {'message': msg, 'reference': link}, http_response

        #   This vendor already exists.  Return the reference
        msg = f'Vendor {new_vendor.name} already exists.'
        http_response = 409
        link = url_for("vendor_vendor", name=new_vendor.name, _external=True)
        return {'message': msg, 'reference': link}, http_response


@ns.route('/<name>/')
@api.doc(params={'name': 'Name of an individual vendor'})
class Vendor(Resource):
    @api.doc('View the data for a single vendor.')
    def get(self, name):
        """Get the vendor information"""
        vendor = Vendor_data.query.filter_by(name=name).first()
        if (vendor):
            vendor_schema = VendorSchema()
            result = vendor_schema.dump(vendor).data
            return {'vendors': result}, 200

        return {'message': 'Vendor not found.'}, 404

        api.abort(404)

    @accepts(schema=VendorSchemaPost, api=api)
    def put(self, name):
        #   Check vendor exists
        if name:
            vendor_to_update = Vendor_data.query.filter_by(name=name).first()
            if vendor_to_update:
                return {'message': f'Vendor {name} has been updated.'}

        #   No vendor by that name
        return {'message': 'Vendor not found.'}, 404

    def delete(self, name):
        #   Check vendor exists
        if name:
            vendor_to_delete = Vendor_data.query.filter_by(name=name).first()
            if vendor_to_delete:
                db.session.delete(vendor_to_delete)
                db.session.commit()
                return {'message': f'Vendor {name} has been removed.'}

        #   No vendor by that name
        return {'message': 'Vendor not found.'}, 404


debug_print(__file__)
