"""Aquí están los errores propios del proyecto. Tenerlos separados ayuda a identificar qué salió mal en cada operación."""

#Excepciones propias del sistema Software FJ.

#Todas heredan de ErrorSistema, así que el programa puede capturar
#cualquier error controlado con un único bloque except ErrorSistema.



# Es el error principal del proyecto; los demás errores personalizados parten de esta clase.
class ErrorSistema(Exception):
    "Error general controlado dentro de la aplicación"

# Se usa cuando un dato llega con un formato o valor que no se acepta.
class DatosInvalidosError(ErrorSistema):
    "Se presenta cuando un dato no cumple las validaciones"

# Indica que hace falta un dato necesario para continuar.
class ParametroFaltanteError(ErrorSistema):
    "Se presenta cuando falta un parámetro obligatorio"

# Aparece cuando se intenta reservar algo que ya está ocupado.
class ServicioNoDisponibleError(ErrorSistema):
    "Se intenta reservar un servicio que no está disponible"

# Agrupa problemas que impiden crear o procesar una reserva.
class ReservaInvalidaError(ErrorSistema):
    "Se presenta cuando una reserva no puede crearse o procesarse"

# Se usa cuando se intenta cambiar una reserva en un momento que no corresponde.
class OperacionNoPermitidaError(ErrorSistema):
    "Se intenta realizar una operación que no corresponde al estado actual"

# Indica que el resultado de un cálculo no tiene sentido para el sistema.
class CalculoInconsistenteError(ErrorSistema):
    "El cálculo de un costo produjo un resultado imposible"
