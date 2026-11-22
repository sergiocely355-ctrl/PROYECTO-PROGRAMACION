"""Este archivo pone en marcha el programa. Primero muestra unas pruebas de ejemplo y después presenta el menú para el usuario."""

# Se importa la clase Cliente para crear y validar clientes
from clientes import Cliente
# Se importan los tres servicios especializados
from servicios import ServicioSala, ServicioEquipo, ServicioAsesoria
# Se importa la clase Reserva, que une cliente, servicio, duración y estado
from reservas import Reserva
# Se importa el gestor, que guarda las listas de objetos y escribe el log
from gestor import GestorSoftwareFJ
# Se importa la excepción base: con ella se captura cualquier error controlado del sistema
from excepciones import ErrorSistema


# Realiza varios ejemplos para mostrar tanto operaciones correctas como errores que el programa sabe controlar.
def ejecutar_pruebas(gestor):
    # Encabezado visual de la demostración
    print("\n========== DEMOSTRACIÓN DE SOFTWARE FJ ==========")

    # OPERACIÓN 1: registro de un cliente válido.
    # Se crea el Cliente y se guarda en la lista del gestor.
    cliente1 = gestor.registrar_cliente(
        Cliente("C001", "Sergio Cely", "sergio@correo.com", "3001234567")
    )
    # Se muestra el resultado (usa el método __str__ de Cliente)
    print("1. Cliente registrado:", cliente1)

    # OPERACIÓN 2: cliente con correo inválido
    try:
        # El correo "correo-no-valido" no tiene @, así que Cliente lanza una excepción
        Cliente("C002", "Laura Pérez", "correo-no-valido", "3112223344")
    except ErrorSistema as error:
        # El error se guarda en el log y el programa continúa
        gestor.registrar_error("Operación 2: cliente inválido", error)
        # Se informa al usuario sin detener el programa
        print("2. Cliente inválido controlado:", error)

    # OPERACIÓN 3: registro de un segundo cliente válido.
    cliente2 = gestor.registrar_cliente(
        Cliente("C003", "Carlos Gómez", "carlos@correo.com", "3205556677")
    )
    print("3. Segundo cliente registrado:", cliente2)

    # OPERACIÓN 4: creación de un servicio de tipo sala (id, nombre, tarifa por hora, capacidad)
    sala = gestor.registrar_servicio(
        ServicioSala("S001", "Sala de reuniones", 25000, 12)
    )
    # describir() es polimorfismo: cada tipo de servicio lo implementa a su manera
    print("4. Servicio creado:", sala.describir())

    # OPERACIÓN 5: creación de un servicio de alquiler de equipos (id, nombre, tarifa por día, unidades)
    equipo = gestor.registrar_servicio(
        ServicioEquipo("S002", "Video beam", 40000, 3)
    )
    print("5. Servicio creado:", equipo.describir())

    # OPERACIÓN 6: creación de un servicio de asesoría (id, nombre, tarifa por hora, especialidad).
    asesoria = gestor.registrar_servicio(
        ServicioAsesoria("S003", "Asesoría de software", 60000, "Desarrollo de software")
    )
    print("6. Servicio creado:", asesoria.describir())

    # OPERACIÓN 7: servicio con tarifa negativa (debe fallar de forma controlada)
    try:
        ServicioSala("S004", "Sala inválida", -1000, 10)
    except ErrorSistema as error:
        gestor.registrar_error("Operación 7: servicio inválido", error)
        print("7. Servicio inválido controlado:", error)

    # OPERACIÓN 8: reserva exitosa de la sala por 2 horas, con 19 % de impuesto y 10 % de descuento.
    reserva1 = gestor.crear_reserva(
        Reserva("R001", cliente1, sala, 2, impuesto=0.19, descuento=0.10)
    )
    # confirmar() calcula el costo, ocupa el servicio y cambia el estado a Confirmada
    costo = reserva1.confirmar()
    # Se deja constancia del evento en el archivo de log
    gestor.registrar_evento(f"Reserva {reserva1.identificador} confirmada por ${costo}")
    print("8. Reserva confirmada:", reserva1.describir())

    # OPERACIÓN 9: reserva sin cliente (intento de reserva incorrecto).
    try:
        # Se pasa None como cliente, por lo que la reserva no puede crearse
        Reserva("R002", None, equipo, 1)
    except ErrorSistema as error:
        gestor.registrar_error("Operación 9: reserva sin cliente", error)
        print("9. Reserva incorrecta controlada:", error)

    # OPERACIÓN 10: intentar confirmar otra reserva de la misma sala, que ya está ocupada.
    # La reserva se crea en estado Pendiente...
    reserva2 = gestor.crear_reserva(
        Reserva("R003", cliente2, sala, 1)
    )
    try:
        # ...pero al confirmarla falla, porque la sala ya fue tomada por R001
        reserva2.confirmar()
    except ErrorSistema as error:
        gestor.registrar_error("Operación 10: servicio ocupado", error)
        print("10. Servicio no disponible controlado:", error)

    # OPERACIÓN 11: cancelar la primera reserva; esto libera la sala.
    reserva1.cancelar()
    gestor.registrar_evento(f"Reserva {reserva1.identificador} cancelada")
    print("11. Reserva cancelada. Servicio disponible:", sala.disponible)

    # OPERACIÓN 12: ahora sí se puede confirmar la segunda reserva, porque la sala quedó libre.
    reserva2.confirmar()
    gestor.registrar_evento(f"Reserva {reserva2.identificador} confirmada")
    print("12. Segunda reserva confirmada:", reserva2.describir())

    # OPERACIÓN 13: finalizar la segunda reserva (la sala vuelve a quedar libre).
    reserva2.finalizar()
    gestor.registrar_evento(f"Reserva {reserva2.identificador} finalizada")
    print("13. Reserva finalizada:", reserva2.estado.value)

    # OPERACIÓN 14: cliente con un parámetro faltante (teléfono = None).
    try:
        Cliente("C004", "Marta Ríos", "marta@correo.com", None)
    except ErrorSistema as error:
        gestor.registrar_error("Operación 14: parámetro faltante", error)
        print("14. Parámetro faltante controlado:", error)

    # OPERACIÓN 15: cálculo inconsistente. Un descuento del 100 % deja el costo en cero.
    reserva3 = gestor.crear_reserva(
        Reserva("R004", cliente1, equipo, 2, descuento=1)
    )
    try:
        reserva3.confirmar()
    except ErrorSistema as error:
        gestor.registrar_error("Operación 15: cálculo inconsistente", error)
        print("15. Cálculo inconsistente controlado:", error)
        # Encadenamiento de excepciones: __cause__ guarda el error original (raise ... from ...)
        print("    Causa original:", type(error.__cause__).__name__, "-", error.__cause__)

    # EJEMPLO DE try / except / else / finally con el cálculo de una asesoría.
    try:
        # Se calcula el costo de 2 horas de asesoría con 19 % de impuesto y 5 % de descuento
        resultado = asesoria.calcular_costo(2, impuesto=0.19, descuento=0.05)
    except ErrorSistema as error:
        # Solo se ejecuta si ocurrió un error controlado
        gestor.registrar_error("Cálculo de asesoría", error)
        print("No se pudo calcular:", error)
    else:
        # Solo se ejecuta si NO hubo ningún error
        print("Costo de asesoría (2 horas, con ajustes):", resultado)
    finally:
        # Se ejecuta siempre, haya ocurrido un error o no
        print("Demostración terminada; el sistema sigue activo.")

    # Línea de cierre visual de la demostración
    print("=================================================\n")


# Mantiene el menú activo y ejecuta la opción que el usuario seleccione.
def mostrar_menu(gestor):
    # Bucle infinito: el menú se repite hasta que el usuario elija salir (opción 6)
    while True:
        # Opciones disponibles para el usuario
        print("========= MENÚ SOFTWARE FJ =========")
        print("1. Ver clientes")
        print("2. Ver servicios")
        print("3. Ver reservas")
        print("4. Registrar cliente")
        print("5. Crear reserva")
        print("6. Salir")

        try:
            # Se lee la opción y se quitan los espacios sobrantes
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                # Si la lista está vacía se avisa al usuario
                if not gestor.clientes:
                    print("Todavía no hay clientes.")
                # Se recorre la lista y se muestra cada cliente
                for cliente in gestor.clientes:
                    print(cliente.describir())

            elif opcion == "2":
                if not gestor.servicios:
                    print("Todavía no hay servicios.")
                # Se muestra cada servicio junto con su disponibilidad
                for servicio in gestor.servicios:
                    print(servicio.describir(), "| Disponible:", servicio.disponible)

            elif opcion == "3":
                if not gestor.reservas:
                    print("Todavía no hay reservas.")
                # Se muestra cada reserva con su estado y costo
                for reserva in gestor.reservas:
                    print(reserva.describir())

            elif opcion == "4":
                # Se piden los datos del nuevo cliente
                identificador = input("Identificador: ")
                nombre = input("Nombre completo: ")
                correo = input("Correo: ")
                telefono = input("Teléfono: ")
                # La clase Cliente valida los datos; si alguno es incorrecto lanza una excepción
                cliente = Cliente(identificador, nombre, correo, telefono)
                # Se guarda en la lista del gestor (revisa que el identificador no esté repetido)
                gestor.registrar_cliente(cliente)
                print("Cliente registrado correctamente.")

            elif opcion == "5":
                # Se piden los identificadores necesarios para la reserva
                id_reserva = input("Identificador de la reserva: ")
                id_cliente = input("Identificador del cliente: ")
                id_servicio = input("Identificador del servicio: ")
                # Se busca el cliente y el servicio en las listas (devuelven None si no existen)
                cliente = gestor.buscar_cliente(id_cliente)
                servicio = gestor.buscar_servicio(id_servicio)
                # float() lanza ValueError si el usuario escribe texto; se captura más abajo
                duracion = float(input("Duración (horas o días según el servicio): "))
                # Si no se encontró el cliente o el servicio, se lanza un error controlado
                if cliente is None:
                    raise ErrorSistema("No se encontró el cliente indicado.")
                if servicio is None:
                    raise ErrorSistema("No se encontró el servicio indicado.")
                # Se crea la reserva, se registra y se confirma (calcula el costo)
                reserva = Reserva(id_reserva, cliente, servicio, duracion)
                gestor.crear_reserva(reserva)
                costo = reserva.confirmar()
                gestor.registrar_evento(f"Reserva {id_reserva} confirmada desde el menú.")
                print("Reserva confirmada. Costo:", costo)

            elif opcion == "6":
                # Sale del bucle y termina el programa
                print("Gracias por utilizar Software FJ.")
                break

            else:
                # Cualquier otra entrada no es una opción del menú
                print("Opción no válida. Intente nuevamente.")

        except (EOFError, KeyboardInterrupt):
            # EOFError: no hay teclado disponible. KeyboardInterrupt: el usuario pulsó Ctrl+C.
            # Se sale del menú; sin este bloque el bucle se repetiría infinitamente.
            print("\nEntrada finalizada. Cerrando el menú.")
            break

        except (ErrorSistema, ValueError) as error:
            # Errores controlados (propios del sistema o por texto en lugar de número):
            # se registran en el log y el menú continúa
            gestor.registrar_error("Error durante el uso del menú", error)
            print("No se pudo completar la operación:", error)

        except Exception as error:
            # Última protección: evita que un error inesperado cierre el menú
            gestor.registrar_error("Error inesperado en el menú", error)
            print("Ocurrió un problema inesperado. El sistema continúa.")

        finally:
            # Se ejecuta siempre: deja una línea en blanco entre cada repetición del menú
            print()


# Crea el gestor, ejecuta la demostración y después deja disponible el menú.
def main():
    # Se crea el gestor (listas vacías de clientes, servicios y reservas)
    gestor = GestorSoftwareFJ()
    # Primero se corren las 15 operaciones de demostración
    ejecutar_pruebas(gestor)
    # Después se abre el menú interactivo
    mostrar_menu(gestor)


# Solo se ejecuta main() si este archivo se corre directamente (no si otro archivo lo importa)
if __name__ == "__main__":
    main()
