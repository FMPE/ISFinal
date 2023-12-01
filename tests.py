import unittest
from app import *


class TestBilletera(unittest.TestCase):
    # Configurar datos para las pruebas
    def setUp(self):
        self.client = app.test_client()

    #caso de exito
    def test_realizar_pago_exitoso(self):
        response = self.client.get('/billetera/pagar?minumero=21345&numerodestino=123&valor=50')

        self.assertEqual(response.status_code, 200)
        self.assertIn('Realizado el', response.get_json())

    #casos de error
    def test_realizar_pago_numero_invalido(self):
        response = self.client.get('/billetera/pagar?minumero=999&numerodestino=123&valor=50')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Numero de cuenta no encontrado', response.get_data(as_text=True))

    def test_obtener_contactos_invalido(self):
        response = self.client.get('/billetera/contactos?minumero=999')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Numero de cuenta no encontrado', response.get_data(as_text=True))

    def test_obtener_historial_numero_invalido(self):
        response = self.client.get('/billetera/historial?minumero=999')

        self.assertEqual(response.status_code, 404)
        self.assertIn('Numero de cuenta no encontrado', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
