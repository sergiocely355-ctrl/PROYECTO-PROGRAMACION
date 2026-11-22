"""Aquí se definen los servicios que ofrece el sistema. Cada tipo calcula su precio según sus propias condiciones."""

import math
from abc import abstractmethod

from entidades import Entidad
from excepciones import DatosInvalidosError, CalculoInconsistenteError


# Es la clase base de los servicios. Define los datos y los métodos que cada tipo concreto debe completar.
class Servicio(Entidad):

    # Valida el nombre y la tarifa, y deja el servicio disponible al crearlo.
    def __init__(self, identificador, nombre, tarifa_base):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa debe ser un número mayor que cero.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = True

    @property
    # Permite consultar el nombre del servicio.
    def nombre(self):
        return self._nombre

    @property
    # Devuelve la tarifa que se usa como base para calcular el precio.
    def tarifa_base(self):
        return self._tarifa_base

    @property
    # Indica si el servicio se puede reservar en ese momento.
    def disponible(self):
        return self._disponible

    # Actualiza si el servicio está libre u ocupado.
    def cambiar_disponibilidad(self, disponible):
        self._disponible = bool(disponible)

    @abstractmethod
    # Cada tipo de servicio debe revisar aquí los datos que le son propios.
    def validar_parametros(self, **parametros):
        """Cada servicio valida sus propios parámetros específicos."""

    @abstractmethod
    # Cada servicio implementa su manera de calcular el valor según la duración.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        """Calcula el costo total. impuesto y descuento son opcionales (sobrecarga simulada).

        Formas de invocarlo:
            calcular_costo(2)                         -> sin ajustes
            calcular_costo(2, impuesto=0.19)          -> solo impuesto
            calcular_costo(2, descuento=0.10)         -> solo descuento
            calcular_costo(2, 0.19, 0.10)             -> ambos
        """

    @abstractmethod
    # Cada servicio define el texto que se mostrará al consultarlo.
    def describir(self):
        """Devuelve un texto que describe el servicio."""

    # Aplica primero el descuento y después el impuesto, y revisa que el total tenga sentido.
    def _calcular_con_ajustes(self, costo, impuesto=0, descuento=0):
        if not 0 <= impuesto <= 1:
            raise DatosInvalidosError("El impuesto debe expresarse entre 0 y 1.")
        if not 0 <= descuento <= 1:
            raise DatosInvalidosError("El descuento debe expresarse entre 0 y 1.")
        # Primero se resta el descuento y sobre ese valor se suma el impuesto
        total = round(costo * (1 - descuento) * (1 + impuesto), 2)
        if math.isnan(total) or math.isinf(total) or total <= 0:
            raise CalculoInconsistenteError(f"El costo calculado no es válido: {total}.")
        return total


# Representa el alquiler de una sala, cuyo precio depende de las horas y cuya capacidad debe ser positiva.
class ServicioSala(Servicio):

    # Valida el nombre y la tarifa, y deja el servicio disponible al crearlo.
    def __init__(self, identificador, nombre, tarifa_hora, capacidad):
        super().__init__(identificador, nombre, tarifa_hora)
        self.validar_parametros(capacidad=capacidad)
        self._capacidad = capacidad

    # Cada tipo de servicio debe revisar aquí los datos que le son propios.
    def validar_parametros(self, **parametros):
        capacidad = parametros.get("capacidad")
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")

    # Cada servicio implementa su manera de calcular el valor según la duración.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        self._validar_duracion(duracion)  # Primero se valida la duración
        return self._calcular_con_ajustes(self.tarifa_base * duracion, impuesto, descuento)

    def _validar_duracion(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor que cero.")

    # Cada servicio define el texto que se mostrará al consultarlo.
    def describir(self):
        return f"Sala: {self.nombre}, capacidad para {self._capacidad} personas, tarifa por hora ${self.tarifa_base:,.0f}"


# Representa el alquiler de un equipo, cobrado por día y con una cantidad disponible registrada.
class ServicioEquipo(Servicio):

    # Valida el nombre y la tarifa, y deja el servicio disponible al crearlo.
    def __init__(self, identificador, nombre, tarifa_dia, cantidad_disponible):
        super().__init__(identificador, nombre, tarifa_dia)
        self.validar_parametros(cantidad=cantidad_disponible)
        self._cantidad_disponible = cantidad_disponible

    # Cada tipo de servicio debe revisar aquí los datos que le son propios.
    def validar_parametros(self, **parametros):
        cantidad = parametros.get("cantidad")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 0:
            raise DatosInvalidosError("La cantidad disponible debe ser un entero igual o mayor que cero.")

    # Cada servicio implementa su manera de calcular el valor según la duración.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("Los días de alquiler deben ser mayores que cero.")
        return self._calcular_con_ajustes(self.tarifa_base * duracion, impuesto, descuento)

    # Cada servicio define el texto que se mostrará al consultarlo.
    def describir(self):
        return f"Alquiler de equipos: {self.nombre}, unidades disponibles: {self._cantidad_disponible}, tarifa por día ${self.tarifa_base:,.0f}"

    @property
    # Permite consultar cuántas unidades del equipo se registraron como disponibles.
    def cantidad_disponible(self):
        return self._cantidad_disponible

    # Cambia la cantidad de unidades después de revisar que el nuevo valor sea válido.
    def cambiar_cantidad(self, cantidad):
        self.validar_parametros(cantidad=cantidad)
        self._cantidad_disponible = cantidad


# Representa una asesoría. Además de las horas, incluye un cargo fijo de preparación.
class ServicioAsesoria(Servicio):

    CARGO_PREPARACION = 15000

    # Valida el nombre y la tarifa, y deja el servicio disponible al crearlo.
    def __init__(self, identificador, nombre, tarifa_hora, especialidad):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("La especialidad de la asesoría es obligatoria.")
        self._especialidad = especialidad.strip()

    # Cada tipo de servicio debe revisar aquí los datos que le son propios.
    def validar_parametros(self, **parametros):
        tema = parametros.get("tema", self._especialidad)
        if not isinstance(tema, str) or not tema.strip():
            raise DatosInvalidosError("Debe indicar el tema de la asesoría.")

    # Cada servicio implementa su manera de calcular el valor según la duración.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("Las horas de asesoría deben ser mayores que cero.")
        costo = (self.tarifa_base * duracion) + self.CARGO_PREPARACION
        return self._calcular_con_ajustes(costo, impuesto, descuento)

    # Cada servicio define el texto que se mostrará al consultarlo.
    def describir(self):
        return f"Asesoría especializada en {self._especialidad}: {self.nombre}, tarifa por hora ${self.tarifa_base:,.0f}"
