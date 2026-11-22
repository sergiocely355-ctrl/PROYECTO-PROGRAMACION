"""Este archivo pone en marcha el programa. Primero muestra unas pruebas de ejemplo y después presenta el menú para el usuario."""

from clientes import Cliente
from servicios import ServicioSala, ServicioEquipo, ServicioAsesoria
from reservas import Reserva
from gestor import GestorSoftwareFJ
from excepciones import ErrorSistema


# Realiza varios ejemplos para mostrar tanto operaciones correctas como errores que el programa sabe controlar.
def ejecutar_pruebas(gestor):
    print("\n========== DEMOSTRACIÓN DE SOFTWARE FJ ==========")

    cliente1 = gestor.registrar_cliente(
        Cliente("C001", "Sergio Cely", "sergio@correo.com", "3001234567")
    )
    print("1. Cliente registrado:", cliente1)

    try:
        Cliente("C002", "Laura Pérez", "correo-no-valido", "3112223344")
    except ErrorSistema as error:
        # El error se guarda en el log y el programa continúa
        gestor.registrar_error("Operación 2: cliente inválido", error)
        print("2. Cliente inválido controlado:", error)

    cliente2 = gestor.registrar_cliente(
        Cliente("C003", "Carlos Gómez", "carlos@correo.com", "3205556677")
    )
    print("3. Segundo cliente registrado:", cliente2)

    sala = gestor.registrar_servicio(
        ServicioSala("S001", "Sala de reuniones", 25000, 12)
    )
    print("4. Servicio creado:", sala.describir())

    equipo = gestor.registrar_servicio(
        ServicioEquipo("S002", "Video beam", 40000, 3)
    )
    print("5. Servicio creado:", equipo.describir())

    asesoria = gestor.registrar_servicio(
        ServicioAsesoria("S003", "Asesoría de software", 60000, "Desarrollo de software")
    )
    print("6. Servicio creado:", asesoria.describir())

    try:
        ServicioSala("S004", "Sala inválida", -1000, 10)
    except ErrorSistema as error:
        gestor.registrar_error("Operación 7: servicio inválido", error)
        print("7. Servicio inválido controlado:", error)

    reserva1 = gestor.crear_reserva(
        Reserva("R001", cliente1, sala, 2, impuesto=0.19, descuento=0.10)
    )
    costo = reserva1.confirmar()
    gestor.registrar_evento(f"Reserva {reserva1.identificador} confirmada por ${costo}")
    print("8. Reserva confirmada:", reserva1.describir())

    try:
        Reserva("R002", None, equipo, 1)
    except ErrorSistema as error:
        gestor.registrar_error("Operación 9: reserva sin cliente", error)
        print("9. Reserva incorrecta controlada:", error)

    reserva2 = gestor.crear_reserva(
        Reserva("R003", cliente2, sala, 1)
    )
    try:
        reserva2.confirmar()
    except ErrorSistema as error:
        gestor.registrar_error("Operación 10: servicio ocupado", error)
        print("10. Servicio no disponible controlado:", error)

    reserva1.cancelar()
    gestor.registrar_evento(f"Reserva {reserva1.identificador} cancelada")
    print("11. Reserva cancelada. Servicio disponible:", sala.disponible)

    reserva2.confirmar()
    gestor.registrar_evento(f"Reserva {reserva2.identificador} confirmada")
    print("12. Segunda reserva confirmada:", reserva2.describir())

    reserva2.finalizar()
    gestor.registrar_evento(f"Reserva {reserva2.identificador} finalizada")
    print("13. Reserva finalizada:", reserva2.estado.value)

    try:
        Cliente("C004", "Marta Ríos", "marta@correo.com", None)
    except ErrorSistema as error:
        gestor.registrar_error("Operación 14: parámetro faltante", error)
        print("14. Parámetro faltante controlado:", error)

    reserva3 = gestor.crear_reserva(
        Reserva("R004", cliente1, equipo, 2, descuento=1)
    )
    try:
        reserva3.confirmar()
    except ErrorSistema as error:
        gestor.registrar_error("Operación 15: cálculo inconsistente", error)
        print("15. Cálculo inconsistente controlado:", error)
        print("    Causa original:", type(error.__cause__).__name__, "-", error.__cause__)

    try:
        resultado = asesoria.calcular_costo(2, impuesto=0.19, descuento=0.05)
    except ErrorSistema as error:
        gestor.registrar_error("Cálculo de asesoría", error)
        print("No se pudo calcular:", error)
    else:
        print("Costo de asesoría (2 horas, con ajustes):", resultado)
    finally:
        print("Demostración terminada; el sistema sigue activo.")

    print("=================================================\n")


# Mantiene el menú activo y ejecuta la opción que el usuario seleccione.
def mostrar_menu(gestor):
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
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                if not gestor.clientes:
                    print("Todavía no hay clientes.")
                for cliente in gestor.clientes:
                    print(cliente.describir())

            elif opcion == "2":
                if not gestor.servicios:
                    print("Todavía no hay servicios.")
                for servicio in gestor.servicios:
                    print(servicio.describir(), "| Disponible:", servicio.disponible)

            elif opcion == "3":
                if not gestor.reservas:
                    print("Todavía no hay reservas.")
                for reserva in gestor.reservas:
                    print(reserva.describir())

            elif opcion == "4":
                identificador = input("Identificador: ")
                nombre = input("Nombre completo: ")
                correo = input("Correo: ")
                telefono = input("Teléfono: ")
                cliente = Cliente(identificador, nombre, correo, telefono)
                gestor.registrar_cliente(cliente)
                print("Cliente registrado correctamente.")

            elif opcion == "5":
                id_reserva = input("Identificador de la reserva: ")
                id_cliente = input("Identificador del cliente: ")
                id_servicio = input("Identificador del servicio: ")
                cliente = gestor.buscar_cliente(id_cliente)
                servicio = gestor.buscar_servicio(id_servicio)
                duracion = float(input("Duración (horas o días según el servicio): "))
                if cliente is None:
                    raise ErrorSistema("No se encontró el cliente indicado.")
                if servicio is None:
                    raise ErrorSistema("No se encontró el servicio indicado.")
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
                print("Opción no válida. Intente nuevamente.")

        except (EOFError, KeyboardInterrupt):
            print("\nEntrada finalizada. Cerrando el menú.")
            break

        except (ErrorSistema, ValueError) as error:
            gestor.registrar_error("Error durante el uso del menú", error)
            print("No se pudo completar la operación:", error)

        except Exception as error:
            gestor.registrar_error("Error inesperado en el menú", error)
            print("Ocurrió un problema inesperado. El sistema continúa.")

        finally:
            print()


# Crea el gestor, ejecuta la demostración y después deja disponible el menú.
def main():
    gestor = GestorSoftwareFJ()
    ejecutar_pruebas(gestor)
    mostrar_menu(gestor)

if __name__ == "__main__":
    main()
