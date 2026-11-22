"""El gestor reúne las operaciones principales: registra clientes, servicios y reservas, y también deja constancia de lo que ocurre."""

import logging  # Módulo estándar para escribir el archivo de logs
from pathlib import Path  # Manejo de rutas independiente del sistema operativo

from clientes import Cliente
from reservas import Reserva
from excepciones import DatosInvalidosError


RUTA_LOG = Path(__file__).resolve().parent / "logs" / "sistema.log"
RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta si no existe


logging.basicConfig(
    filename=RUTA_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True
)
logger = logging.getLogger("SoftwareFJ")

# Es el encargado de mantener organizados los clientes, servicios y reservas mientras el programa está abierto.
class GestorSoftwareFJ:

    # Al iniciar el gestor se crean las tres listas donde se van guardando los objetos.
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    # Devuelve los clientes como una tupla para evitar que desde fuera se modifique la lista original.
    def clientes(self):
        return tuple(self._clientes)

    @property
    # Permite consultar los servicios registrados sin entregar la lista interna.
    def servicios(self):
        return tuple(self._servicios)

    @property
    # Permite consultar las reservas guardadas.
    def reservas(self):
        return tuple(self._reservas)

    # Revisa el tipo de objeto y que no exista otro cliente con el mismo código antes de guardarlo.
    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("Solo se pueden registrar objetos Cliente.")
        if any(c.identificador == cliente.identificador for c in self._clientes):
            raise DatosInvalidosError("Ya existe un cliente con ese identificador.")
        self._clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    # Comprueba que el objeto tenga los métodos necesarios y que su identificador no esté repetido.
    def registrar_servicio(self, servicio):
        if not hasattr(servicio, "calcular_costo") or not hasattr(servicio, "describir"):
            raise DatosInvalidosError("El objeto no cumple con la estructura de un servicio.")
        if any(s.identificador == servicio.identificador for s in self._servicios):
            raise DatosInvalidosError("Ya existe un servicio con ese identificador.")
        self._servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio.identificador)
        return servicio

    # Verifica la reserva y comprueba que el cliente y el servicio ya estén registrados.
    def crear_reserva(self, reserva):
        if not isinstance(reserva, Reserva):
            raise DatosInvalidosError("Debe proporcionar un objeto Reserva.")
        if any(r.identificador == reserva.identificador for r in self._reservas):
            raise DatosInvalidosError("Ya existe una reserva con ese identificador.")
        if reserva.cliente not in self._clientes:
            raise DatosInvalidosError("El cliente no está registrado en el sistema.")
        if reserva.servicio not in self._servicios:
            raise DatosInvalidosError("El servicio no está registrado en el sistema.")
        self._reservas.append(reserva)
        logger.info("Reserva creada: %s", reserva.identificador)
        return reserva

    # Guarda en el archivo de log una actividad normal del sistema.
    def registrar_evento(self, mensaje):
        logger.info("%s", mensaje)

    # Guarda el contexto y los detalles del error para poder revisarlos después.
    def registrar_error(self, contexto, error):
        logger.exception("%s: %s", contexto, error)

    # Busca un cliente por su identificador; si no lo encuentra devuelve None.
    def buscar_cliente(self, identificador):
        return next((c for c in self._clientes if c.identificador == str(identificador)), None)

    # Busca un servicio por su identificador; si no existe devuelve None.
    def buscar_servicio(self, identificador):
        return next((s for s in self._servicios if s.identificador == str(identificador)), None)
