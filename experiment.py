from flask import Flask, request
from flask_restplus import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}


@api.route('/<string:todo_id>')
class TodoSimple(Resource):
    def get(self, todo_id):
        if todo_id in todos:
            return {todo_id: todos[todo_id]}
        return {'message': 'There is no todo by that id.'}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


if __name__ == '__main__':
    app.run(debug=True)
