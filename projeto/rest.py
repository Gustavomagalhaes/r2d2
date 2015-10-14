#!flask/bin/python

from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'solo':
        return 'han'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'message': 'Acesso nao autorizado'}), 403)

filas = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

filas_campos = {
    'protocolo': fields.String,
    'tamanho': fields.String,
    'timestamp': fields.Boolean,
    'uri': fields.Url('fila')
}


class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('protocolo', type=str, required=True,
                                   help='Nenhum protocolo definido',
                                   location='json')
        self.reqparse.add_argument('tamanho', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return {'filas': [marshal(filas, filas_campos) for fila in filas]}

    def post(self):
        args = self.reqparse.parse_args()
        fila = {
            'id': filas[-1]['id'] + 1,
            'protocolo': args['title'],
            'description': args['description'],
            'done': False
        }
        filas.append(fila)
        return {'fila': marshal(fila, filas_campos)}, 201


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        fila = [fila for fila in filas if fila['id'] == id]
        if len(fila) == 0:
            abort(404)
        return {'fila': marshal(fila[0], filas_campos)}

    def put(self, id):
        fila = [fila for fila in filas if fila['id'] == id]
        if len(fila) == 0:
            abort(404)
        fila = fila[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                fila[k] = v
        return {'fila': marshal(fila, filas_campos)}

    def delete(self, id):
        fila = [fila for fila in fila if fila['id'] == id]
        if len(fila) == 0:
            abort(404)
        filas.remove(fila[0])
        return {'result': True}


api.add_resource(TaskListAPI, '/r2d2/api/v1.0/filas', endpoint='filas')
api.add_resource(TaskAPI, '/r2d2/api/v1.0/filas/<int:id>', endpoint='fila')


if __name__ == '__main__':
    app.run(debug=True)