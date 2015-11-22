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
    
global listaFluxos
listaFluxos = {}


class FilaAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('protocolo', type=str, help='Nenhum protocolo definido', location='json')
        self.reqparse.add_argument('tamanho', type=str, location='json')
        #super(TaskListAPI, self).__init__()

    def get(self, fluxo):
        #return {'filas': [marshal(filas, filas_campos) for fila in filas]}
        if fluxo in listaFluxos:
            porcent = float(listaFluxos[fluxo]) / float(listaFluxos['todos']) *100
            return str(listaFluxos[fluxo]) + "   " + str(porcent) + "%"         

api.add_resource(FilaAPI, '/r2d2/api/v1.0/filas/s<string:fluxo>', endpoint='fila')


if __name__ == '__main__':
    app.run(host='http://172.17.25.80', port=500)