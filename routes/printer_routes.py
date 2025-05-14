from flask import Blueprint, jsonify, request
from controllers.printer_controller import Printer
import subprocess

printer_app = Blueprint('printer_app', __name__)
version = "0.0.1"


def print_raw(command):
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error when executing the command: {e}")
        return False


@printer_app.route("/", methods=['GET'])
def index():
    return jsonify(message="ok", version=version)


@printer_app.route("/printers", methods=['GET'])
def get_printers():
    try:
        printer = Printer()
        printers = printer.get_printer_list()
        if len(printers) < 1:
            printers = [
                "Printer Test - Server Node"
            ]
        return jsonify(printers=printers, version=version)
    except Exception as e:
        return jsonify(
            message="For unknown reason it was not possible to get printers list.",
            version=version), 500


@printer_app.route("/print", methods=['POST'])
def print_document():
    data = request.get_json()
    invoice = data['invoice']
    printer_manufacturer = data['printerConfig']['printerManufacturer']
    printer_name = data['printerConfig']['printer']

    if printer_name == "PDF":
        try:
            command = f'echo "{invoice}" | lpr -P {printer_name}'
            if print_raw(command):
                print("Successfully printed")
                return jsonify(message="Successfully printed", version=version)
            else:
                print("For unknown reason it was not possible to print.")
                return jsonify(
                    message="For unknown reason it was not possible to print.",
                    version=version), 500
        except Exception as e:
            print("For unknown reason it was not possible to print.")
            return jsonify(
                message="For unknown reason it was not possible to print.",
                version=version), 500
    else:
        try:
            printer = Printer(printer_name, printer_manufacturer)
            job_id = printer.print([{
                'type': 'TEXT',
                'payload': invoice,
                'config': {
                    "columns": str(data['printerConfig']['numberOfColumns']),
                    "cpi": str(data['printerConfig']['fontSize'])
                }
            }])
            print("Successfully printed")
            return jsonify(message="Successfully printed", jobId=job_id, version=version)
        except Exception as e:
            print("For unknown reason it was not possible to print.")
            return jsonify(
                message="For unknown reason it was not possible to print.",
                version=version), 500
