from app.py import *
import unittest

class TestBilletera(unittest.TestCase):
    # Prueba para obtener contactos
    def test_obtener_contactos(self):
        response = app.test_client().get('/billetera/contactos?minumero=21345')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {123: "Luisa", 456: "Andrea"})

    # Prueba para realizar un pago
    def test_realizar_pago(self):
        response = app.test_client().get('/billetera/pagar?minumero=21345&numerodestino=123&valor=50')
        self.assertEqual(response.status_code, 200)

    # Prueba para obtener el historial
    def test_obtener_historial(self):
        response = app.test_client().get('/billetera/historial?minumero=21345')
        self.assertEqual(response.status_code, 200)

