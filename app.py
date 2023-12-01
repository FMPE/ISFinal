from flask import Flask, request, jsonify
from datetime import date

app = Flask(__name__)

def Fecha():
    return date.today()

class Operacion:
    def __init__(self, numDest, fecha, valor, recibido=0):
        self.numDest = numDest
        self.fecha = fecha
        self.valor = valor
        self.recibido = recibido
    
    def Num(self):
        return self.numDest

    def Valor(self):
        return self.valor

    def Recib(self):
        return self.recibido
    
    
class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.historial = []

    def Nombre(self):
        return self.nombre

    def Numero(self):
        return self.numero
    
    def Saldo(self):
        return self.saldo

    def Contactos(self):
        c = self.contactos
        return c
    
    def agregarRecibido(self, op):
        self.historial.append(op)
        return

    def Historial(self):
        return self.historial

    def Pagar(self, destino, valor):
        fecha = str(Fecha())
        ntrans = Operacion(destino, fecha, valor, 0)
        self.historial.append(ntrans)
        BD[destino].agregarRecibido(Operacion(destino, fecha, valor, 1))
        return fecha


BD = {21345:Cuenta(21345, "Arnaldo", 200, [123, 456]),
        123:Cuenta(123, "Luisa", 400, [456]),
        456:Cuenta(456, "Andrea", 300, [21345])
    }

@app.route('/billetera/contactos', methods=['GET'])
def obtener_contactos():
    minumero = int(request.args.get('minumero'))
    # Lógica para obtener los contactos
    res = {}
    contacts = BD[minumero].Contactos()
    for c in contacts:
        res[c] = BD[c].Nombre()
    return jsonify(res)


@app.route('/billetera/pagar', methods=['GET'])
def realizar_pago():
    minumero = int(request.args.get('minumero'))
    numerodestino = int(request.args.get('numerodestino'))
    valor = int(request.args.get('valor'))
    # Lógica para realizar el pago
    BD[minumero].Pagar(numerodestino, valor)
    return jsonify('Realizado el {}'.format(str(Fecha())))


@app.route('/billetera/historial', methods=['GET'])
def obtener_historial():
    minumero = int(request.args.get('minumero'))
    # Lógica para obtener el historial
    hist = BD[minumero].Historial()
    res = ""
    res += "saldo de {}: {} \n".format(BD[minumero].Nombre(), BD[minumero].Saldo())
    for h in hist:
        if h.Recib():
            res += "Pago realizado de {} a {}".format(h.Valor(), BD[h.Num()].Nombre())
        else:
            res += "Pago recibido de {} a {}".format(h.Valor(), BD[h.Num()].Nombre())
    return res


def create_app():
    return app

if __name__ == '__main__':
    app.run(debug=True,port=5000)