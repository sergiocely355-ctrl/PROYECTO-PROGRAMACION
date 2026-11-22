"""En este archivo está la clase Cliente. Aquí se guardan los datos de cada persona y se revisa que tengan un formato válido."""

import re  

from entidades import Entidad  
from excepciones import DatosInvalidosError, ParametroFaltanteError  


# Representa a una persona que puede solicitar alguno de los servicios.
class Cliente(Entidad):

    # Al crear el cliente se comprueba que lleguen los datos obligatorios y luego se asignan usando sus propiedades.
    def __init__(self, identificador, nombre, correo, telefono):
        if nombre is None or correo is None or telefono is None:
            raise ParametroFaltanteError("Faltan datos obligatorios del cliente (nombre, correo o teléfono).")
        super().__init__(identificador)
        self._nombre = None
        self._correo = None
        self._telefono = None
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    # Permite consultar el nombre que quedó guardado.
    def nombre(self):
        return self._nombre

    @nombre.setter
    # Permite consultar el nombre que quedó guardado.
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosInvalidosError("El nombre debe tener al menos dos caracteres.")
        self._nombre = valor.strip().title()

    @property
    # Se utiliza para consultar el correo después de validarlo.
    def correo(self):
        return self._correo

    @correo.setter
    # Se utiliza para consultar el correo después de validarlo.
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        self._correo = valor.strip().lower()

    @property
    # Devuelve el teléfono que pasó la validación.
    def telefono(self):
        return self._telefono

    @telefono.setter
    # Devuelve el teléfono que pasó la validación.
    def telefono(self, valor):
        numero = str(valor).strip()
        if not numero.isdigit() or not 7 <= len(numero) <= 15:
            raise DatosInvalidosError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._telefono = numero

    # Prepara un resumen del cliente para mostrarlo en pantalla.
    def describir(self):
        return f"Cliente {self.nombre} | correo: {self.correo} | teléfono: {self.telefono}"

    # Define cómo se muestra el cliente cuando se imprime directamente.
    def __str__(self):
        return f"{self.identificador} - {self.nombre}"
