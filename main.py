"""Starting point for our Flask Website"""
from HomeServer import app, api
from flask_restplus import Resource, fields
from .models import User, Role, Board, BoardComponent, Manufacturer, Vendor, RawData

ns = api.namespace('api', description='API for Home based IOT Server')
iot = api.model('experiment', {
    'id': fields.Integer(readOnly=True, description="Primary Identifier"),
    'second': fields.String(required=True, description="A second field.")
})


class Experiment(object):
    def __init__(self):
        self.counter = 0
        self.iots = []

    def get(self, id):
        for iot in self.iots:
            if iot[id] == id:
                return iot
        api.abort(404, "Experimental value {} does not exist".format(id))

    def create(self, data):
        iot = data
        iot['id'] = self.counter = self.counter + 1
        self.iots.append(iot)
        return iot

    def update(self, id, data):
        iot = self.get(id)
        iot.update(data)
        return iot

    def delete(self, id):
        iot = self.get(id)
        self.iot.remove(iot)


fIOT = Experiment()
fIOT.create({'second': "Build an API"})
fIOT.create({'second': "Second object"})
fIOT.create({'second': "Third object"})
fIOT.create({'second': "Fourth object"})
fIOT.create({'second': "Fifth object"})


@ns.route('/')
class ExperimentalList(Resource):
    '''Shows a list of experimental stuff'''

    @ns.doc('List the experimental stuff')
    @ns.marshal_list_with(iot)
    def get(self):
        '''List all the experimental stuff'''
        return fIOT.iots

    @ns.doc('Create an experimental iot')
    @ns.expect(iot)
    @ns.marshal_with(iot, code=201)
    def post(self):
        '''Create a new IOT object'''
        return fIOT.create(api.payload), 201


print(__name__)
if __name__ == 'main':
    print('-' * 25 + ' ...Starting... ' + '-' * 25)
    app.run(host="0.0.0.0", port=5000, debug=True)
