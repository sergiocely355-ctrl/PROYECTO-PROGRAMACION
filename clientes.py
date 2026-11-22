"""Archivo: clientes.py 

Descripción: 
Ese documento contiene la clase cliente encargada de registrar y administrar la información de los clientes del sistema. 
Nos permite almacenar su nombre correo electrónico teléfono aplicando validaciones para garantizar que todos los datos ingresados sean correctos."""

import re  
# Librería utilizada para validar el formato correcto de correo electrónico

from entidades import Entidad  
# Importa la clase base entidad para aplicar el principio de herencia
from excepciones import DatosInvalidosError, ParametroFaltanteError  
# Importa las excepciones personalizadas para controlar todos los errores
# Cuando faltan datos o cuando la información no es válida


# Aquí se define las clases cliente, que hereda la identidad
# La función es almacenar y validar todos los datos personales de los clientes registrados en el sistema

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
