"""Archivo: clientes.py

Descripción:
Este documento contiene la clase Cliente, encargada de registrar y administrar la información de los clientes del sistema.
Permite almacenar su nombre, correo electrónico y teléfono, aplicando validaciones para garantizar que todos los datos ingresados sean correctos."""

import re
# Librería utilizada para validar el formato correcto del correo electrónico

from entidades import Entidad
# Importa la clase base Entidad para aplicar el principio de herencia
from excepciones import DatosInvalidosError, ParametroFaltanteError
# Importa las excepciones personalizadas para controlar los errores
# cuando faltan datos o cuando la información no es válida


# Aquí se define la clase Cliente, que hereda de Entidad.
# Su función es almacenar y validar todos los datos personales de los clientes registrados en el sistema.

class Cliente(Entidad):

    def __init__(self, identificador, nombre, correo, telefono):
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
        # Si falta algún dato obligatorio se lanza un error específico
        if nombre is None or correo is None or telefono is None:
            raise ParametroFaltanteError("Faltan datos obligatorios del cliente (nombre, correo o teléfono).")
        super().__init__(identificador)
        # Inician los atributos privados
        self._nombre = None
        self._correo = None
        self._telefono = None
        # Se asignan mediante las propiedades, que validan cada dato
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    # Permite consultar el nombre que quedó guardado.
    def nombre(self):
        """Se obtiene el nombre del cliente.

        Returns:
            str: nombre almacenado del cliente.
        """
        return self._nombre

    @nombre.setter
    # Permite modificar y validar el nombre.
    def nombre(self, valor):
        """Se establece y valida el nombre del cliente.

        Se verifica que el valor sea texto y tenga como mínimo dos caracteres.
        Si es válido, se eliminan los espacios innecesarios y se convierte
        el nombre al formato de título.
        """
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosInvalidosError("El nombre debe tener al menos dos caracteres.")
        self._nombre = valor.strip().title()

    @property
    # Permite consultar el correo electrónico guardado.
    def correo(self):
        """Se obtiene la dirección de correo electrónico almacenada para el cliente.

        Returns:
            str: correo electrónico del cliente.
        """
        return self._correo

    @correo.setter
    # Permite modificar y validar el correo electrónico.
    def correo(self, valor):
        """Aquí se valida y se establece el correo electrónico.

        Se comprueba que tenga una estructura válida mediante una expresión regular.
        Cuando cumple las condiciones, se eliminan espacios innecesarios y
        se convierte el texto a minúsculas.
        """
        if not isinstance(valor, str) or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor.strip()):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")
        self._correo = valor.strip().lower()

    @property
    # Permite consultar el teléfono guardado.
    def telefono(self):
        """Obtiene el número telefónico del cliente.

        Returns:
            str: número de teléfono almacenado en el sistema.
        """
        return self._telefono

    @telefono.setter
    # Permite modificar y validar el teléfono.
    def telefono(self, valor):
        """Aquí se valida y se establece el número telefónico.

        Debe contener solo dígitos y tener entre 7 y 15 caracteres.
        """
        numero = str(valor).strip()
        if not numero.isdigit() or not 7 <= len(numero) <= 15:
            raise DatosInvalidosError("El teléfono debe contener entre 7 y 15 dígitos.")
        self._telefono = numero

    # Prepara un resumen del cliente para mostrarlo en pantalla.
    def describir(self):
        """Genera una descripción con los datos principales del cliente.

        Returns:
            str: información del cliente (nombre, correo electrónico y teléfono).
        """
        return f"Cliente {self.nombre} | correo: {self.correo} | teléfono: {self.telefono}"

    # Define cómo se muestra el cliente cuando se imprime directamente.
    def __str__(self):
        """Define la representación en texto del objeto Cliente.

        Returns:
            str: identificador y nombre del cliente.

        Muestra la información resumida cuando se usa print().
        """
        return f"{self.identificador} - {self.nombre}"
