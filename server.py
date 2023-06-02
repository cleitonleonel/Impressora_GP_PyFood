from flask import Flask
from routes.printer_routes import printer_app
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(printer_app)

CORS(app, origins=[
    "https://gestordepedidos.ifood.com.br",
    "https://gestordepedidos-homologation.ifood.com.br",
    "http://localhost:4200"
])

if __name__ == '__main__':
    app.run(host='localhost', port=4013, debug=False)
