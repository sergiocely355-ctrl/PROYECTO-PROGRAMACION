"""En este archivo se controla el ciclo de vida de una reserva: se crea, se confirma, se cancela o se finaliza."""

from enum import Enum  # Permite definir los estados como valores fijos

from entidades import Entidad
from excepciones import (
    ReservaInvalidaError, ServicioNoDisponibleError,
    OperacionNoPermitidaError, DatosInvalidosError
)


# Enumera los estados posibles de una reserva para evitar escribirlos de distintas maneras.
class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    FINALIZADA = "Finalizada"


# Relaciona un cliente con un servicio y controla el estado y el costo de esa solicitud.
class Reserva(Entidad):

    # Antes de crear la reserva revisa que existan el cliente, el servicio y una duración válida.
    def __init__(self, identificador, cliente, servicio, duracion, impuesto=0, descuento=0):
        super().__init__(identificador) 
        if cliente is None:
            raise ReservaInvalidaError("La reserva necesita un cliente.")
        if servicio is None:
            raise ReservaInvalidaError("La reserva necesita un servicio.")
        if not hasattr(servicio, "calcular_costo"):
            raise ReservaInvalidaError("El objeto seleccionado no es un servicio válido.")
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise DatosInvalidosError("La duración debe ser un número mayor que cero.")

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._impuesto = impuesto
        self._descuento = descuento
        self._estado = EstadoReserva.PENDIENTE
        self._costo = None

    @property
    # Permite consultar qué cliente está asociado a la reserva.
    def cliente(self):
        return self._cliente

    @property
    # Permite consultar cuál es el servicio reservado.
    def servicio(self):
        return self._servicio

    @property
    # Muestra el estado actual de la reserva.
    def estado(self):
        return self._estado

    @property
    # Devuelve el costo calculado; mientras no se confirme, su valor es None.
    def costo(self):
        return self._costo

    # Confirma solo si la reserva está pendiente y el servicio sigue libre; después calcula el costo y ocupa el servicio.
    def confirmar(self):
        if self._estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
        if not self._servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' no está disponible.")

        try:
            costo = self._servicio.calcular_costo(
                self._duracion, self._impuesto, self._descuento
            )
        except Exception as error:
            raise ReservaInvalidaError("No fue posible calcular el costo de la reserva.") from error
        else:
            self._costo = costo
            self._servicio.cambiar_disponibilidad(False)
            self._estado = EstadoReserva.CONFIRMADA
            return self._costo

    # Cancela una reserva pendiente o confirmada. Si ya estaba confirmada, deja libre el servicio.
    def cancelar(self):
        if self._estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise OperacionNoPermitidaError("La reserva no se puede cancelar en su estado actual.")
        if self._estado == EstadoReserva.CONFIRMADA:
            self._servicio.cambiar_disponibilidad(True)
        self._estado = EstadoReserva.CANCELADA

    # Cierra una reserva confirmada y vuelve a dejar disponible el servicio.
    def finalizar(self):
        if self._estado != EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError("Solo se puede finalizar una reserva confirmada.")
        self._estado = EstadoReserva.FINALIZADA
        self._servicio.cambiar_disponibilidad(True)

    # Arma un resumen con el cliente, el servicio, la duración, el estado y el costo.
    def describir(self):
        valor = f"${self._costo:,.2f}" if self._costo is not None else "Pendiente de cálculo"
        return (
            f"Reserva {self.identificador} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | Duración: {self._duracion} | "
            f"Estado: {self._estado.value} | Costo: {valor}"
        )
