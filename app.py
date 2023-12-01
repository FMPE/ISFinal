from flask import Flask, request, jsonify
from datetime import date


app = Flask(__name__)

def Fecha():
    return date.today()

class Operacion:
    def __init__(self, numEmi, numDest, fecha, valor):
        self.numEmi = numEmi
        self.numDest = numDest
        self.fecha = fecha
        self.valor = valor
    
    def NumDest(self):
        return self.numDest
    
    def NumEmi(self):
        return self.numEmi

    def Valor(self):
        return self.valor
    
    
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
        return self.contactos
    
    def agregarRecibido(self, op):
        self.historial.append(op)
    
    def sumarSaldo(self ,valor):
        self.saldo += valor

    def Historial(self):
        return self.historial

    def Pagar(self, destino, valor):
        if destino in self.contactos and valor <= self.saldo:
            fecha = str(Fecha())
            ntrans = Operacion(self.numero, destino, fecha, valor)
            self.saldo -= valor
            self.historial.append(ntrans)
            BD[destino].agregarRecibido(ntrans)
            BD[destino].sumarSaldo(valor)
            return "Realizado el {}".format(fecha)
        else:
            return "Datos no validos"


BD = {21345:Cuenta(21345, "Arnaldo", 200, [123, 456]),
        123:Cuenta(123, "Luisa", 400, [456]),
        456:Cuenta(456, "Andrea", 300, [21345])
    }

@app.route('/billetera/contactos', methods=['GET'])
def obtener_contactos():
    try:
        minumero = int(request.args.get('minumero'))
        res = {}
        contacts = BD[minumero].Contactos()
        for c in contacts:
            res[c] = BD[c].Nombre()
        return jsonify(res), 200
    except Exception as e:
        return jsonify("Numero de cuenta no encontrado"), 404


@app.route('/billetera/pagar', methods=['GET'])
def realizar_pago():
    try:
        minumero = int(request.args.get('minumero'))
        numerodestino = int(request.args.get('numerodestino'))
        valor = int(request.args.get('valor'))
        res = BD[minumero].Pagar(numerodestino, valor)
        return jsonify(res)
    except Exception as e:
        return jsonify("Numero de cuenta no encontrado"), 404


@app.route('/billetera/historial', methods=['GET'])
def obtener_historial():
    try:
        minumero = int(request.args.get('minumero'))
        res = ""
        res += "Saldo de {}: {} \n".format(BD[minumero].Nombre(), BD[minumero].Saldo())
        hist = BD[minumero].Historial()
        res += "Operaciones de {}: \n".format(BD[minumero].Nombre())
        for h in hist:
            if h.NumDest() != BD[minumero].Numero():
                res += "Pago realizado de {} a {} \n".format(h.Valor(), BD[h.NumDest()].Nombre())
            else:
                res += "Pago recibido de {} de {} \n".format(h.Valor(), BD[h.NumEmi()].Nombre())
        return res
    except Exception as e:
        return jsonify("Numero de cuenta no encontrado"), 404


if __name__ == '__main__':
    app.run(debug=True,port=5000)