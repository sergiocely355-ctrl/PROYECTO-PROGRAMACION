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

    """
    Constructor de la clase Cliente.

    Parámetros:
        identificador: código único del cliente.
        nombre: nombre completo del cliente.
        correo: dirección de correo electrónico.
        telefono: número de contacto.

    Comprueba que los datos obligatorios estén presentes,
    inicializa los atributos y utiliza las propiedades
    para validar la información.
    """
    def __init__(self, identificador, nombre, correo, telefono):
        if nombre is None or correo is None or telefono is None:
            raise ParametroFaltanteError("Faltan datos obligatorios del cliente (nombre, correo o teléfono).")
        super().__init__(identificador)
        # Inician los atributos privados
        self._nombre = None
        self._correo = None
        self._telefono = None
        # Se asigna el nombre mediante su propiedad y se valida
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    # Permite consultar el nombre que quedó guardado.
    def nombre(self):
        """Se obtiene el nombre del cliente 

Returns:
str: nombre archivado del cliente
"""

 """ 
Se establece y valida el nombre del cliente 

Se verifica que el valor sea texto y tenga como mínimo dos caracteres 

Si es válido se eliminan los espacios innecesarios y se convierte en el nombre al formato de título
"""
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
    """
    Se obtiene la dirección de correo electrónico almacenada para el cliente 

Returns:
str: correo electrónico del cliente.
"""
"""
Aquí se valida y se establece el correo electrónico. 

Se comprueba que el correo electrónico tenga la misma estructura válida mediante una expresión regular 

Cuando cumple con las condiciones elimina espacios innecesarios y convierte el texto a minúsculas
"""
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
