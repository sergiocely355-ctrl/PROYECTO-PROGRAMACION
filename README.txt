PROYECTO: SISTEMA INTEGRAL SOFTWARE FJ
======================================

¿DE QUÉ TRATA?
Software FJ permite registrar clientes, ofrecer distintos servicios y
gestionar reservas. El programa valida los datos, calcula los costos y
controla que no se reserve un servicio que ya esté ocupado.

¿QUÉ SE NECESITA?
- Python 3.9 o una versión más reciente.
- No hace falta instalar paquetes externos, porque se utilizan módulos
  que vienen con Python.

ARCHIVOS DEL PROYECTO
- main.py: inicia el programa, muestra unos ejemplos y abre el menú.
- entidades.py: contiene la clase base Entidad.
- clientes.py: contiene la clase Cliente y sus validaciones.
- servicios.py: define los servicios de salas, equipos y asesorías.
- reservas.py: controla la creación, confirmación, cancelación y cierre
  de las reservas.
- excepciones.py: reúne los errores que se pueden presentar en el sistema.
- gestor.py: administra las listas de clientes, servicios y reservas.
- logs/: carpeta donde se guarda el registro de actividad.

¿CÓMO SE EJECUTA?
1. Descomprimir la carpeta del proyecto.
2. Abrir esa carpeta en Visual Studio Code o en una terminal.
3. Ejecutar el siguiente comando:

   python main.py

   Si el comando anterior no funciona en Windows, se puede probar:

   py main.py

¿QUÉ PASA CUANDO SE INICIA?
Primero aparece una demostración con ejemplos de registro de clientes,
creación de servicios y manejo de reservas. También se prueban algunos
datos incorrectos para comprobar que el programa controle los errores.
Al terminar esa parte, aparece un menú desde el que se pueden consultar
los registros, agregar clientes y crear reservas.

CONCEPTOS DE PROGRAMACIÓN ORIENTADA A OBJETOS
- Abstracción: Entidad y Servicio sirven como clases base.
- Herencia: Cliente y los tipos de servicio aprovechan características
  definidas en sus clases principales.
- Encapsulamiento: se usan atributos internos y propiedades para
  consultar o validar la información.
- Polimorfismo: los diferentes servicios tienen su propia versión de
  calcular_costo() y describir().
- Excepciones: se definieron errores propios para controlar situaciones
  que pueden ocurrir durante el uso del programa.
- Colecciones: el gestor utiliza listas para mantener los objetos
  mientras la aplicación está abierta.

SOBRE EL ALMACENAMIENTO
Los clientes, servicios y reservas se mantienen en memoria. Por eso,
cuando se cierra el programa, esos datos no quedan guardados para la
siguiente ejecución. El archivo sistema.log sí permanece y conserva
un registro de eventos y errores. Este archivo no funciona como una
base de datos.
