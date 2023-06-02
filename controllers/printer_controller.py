import cups
import asyncio
import tempfile
from unidecode import unidecode
from controllers.printer_constants import printer_constants

PRINTER_STATUS = {
    "ERROR_PRINTER_NOT_CONFIGURED": "ERROR_PRINTER_NOT_CONFIGURED",
    "ERROR_PRINTER_UNAVAILABLE": "ERROR_PRINTER_UNAVAILABLE",
    "PRINTER_OK": "PRINTER_OK"
}


class Printer(object):

    def __init__(self, printer_name=None, printer_manufacturer=None):
        self.conn = cups.Connection()
        self.printer_name = printer_name
        self.printer_manufacturer = printer_manufacturer

    def get_printer_list(self):
        return list(self.conn.getPrinters().keys())

    def get_printer_status(self):
        if not self.printer_name or not self.printer_manufacturer:
            print("Printer not configured")
            return PRINTER_STATUS["ERROR_PRINTER_NOT_CONFIGURED"]
        printers = self.conn.getPrinters()
        if self.printer_name not in printers:
            print(f"A impressora '{self.printer_name}' não foi encontrada.")
            return PRINTER_STATUS["ERROR_PRINTER_UNAVAILABLE"]
        return PRINTER_STATUS["PRINTER_OK"]

    async def get_printable_buffer(self, printable, commands):
        lines = printable['payload'].split("\n")
        buffer_data = []
        for line in lines:
            if len(line.strip()) > 0:
                buffer_data.append(bytes(line, encoding='utf-8'))
            else:
                buffer_data.extend(bytes(command) for command in commands['feed'])
        return buffer_data

    async def get_printer_buffer(self, printables, commands):
        buffer_data = []
        buffer_data.extend(bytes(command) for command in commands['init'])
        printable_buffers = await asyncio.gather(*[self.get_printable_buffer(printable, commands) for printable in printables])
        flat_buffers = [buffer for sublist in printable_buffers for buffer in sublist]
        buffer_data.extend(flat_buffers)
        buffer_data.extend(bytes(command) for command in commands['feed'])
        buffer_data.extend(bytes(command) for command in commands['feed'])
        buffer_data.extend(bytes(command) for command in commands['feed'])
        buffer_data.extend(bytes(command) for command in commands['cut'])
        return b''.join(buffer_data) + (bytes([10]) * 4)

    def print(self, printables):
        commands = printer_constants[self.printer_manufacturer]
        decoded = self.decode_printables(printables)
        buffer = asyncio.run(self.get_printer_buffer(decoded, commands))
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(buffer)
        temp_file.close()
        print_options = {
            'media': 'Custom.80x210mm',
            'columns': decoded[0].get('config')['columns'],
            'cpi': decoded[0].get('config')['cpi'],
            'lpi': '6',
            'number-up': '1',
        }
        job = self.conn.printFile(
            self.printer_name, temp_file.name,
            'Impressão GP iFood',
            print_options)
        return job

    def decode_printables(self, printables):
        decoded = []
        for printable in printables:
            if printable["type"] == "TEXT":
                escaped_text = unidecode(printable["payload"])
                decoded.append({**printable, "payload": escaped_text})
            else:
                decoded.append(printable)
        return decoded
