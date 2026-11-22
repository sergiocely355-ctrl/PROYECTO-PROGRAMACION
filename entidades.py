"""Esta clase reúne lo que tienen en común los elementos principales del sistema. Las demás clases pueden heredar de ella."""

from abc import ABC, abstractmethod  
from datetime import datetime  

from excepciones import ParametroFaltanteError  

# Es una clase general y abstracta. Sirve como base para los objetos que tienen identificador y fecha de registro.
class Entidad(ABC):
    # Comprueba que el identificador tenga algún valor y guarda también la fecha de creación.
    def __init__(self, identificador):
        if identificador is None or not str(identificador).strip():
            raise ParametroFaltanteError("El identificador no puede estar vacío.")
        self._identificador = str(identificador).strip()
        self._fecha_registro = datetime.now()
    @property

    # Expone el identificador sin permitir modificarlo desde esta propiedad.
    def identificador(self):
        return self._identificador
    @property

    # Permite consultar cuándo se creó el objeto.
    def fecha_registro(self):
        return self._fecha_registro
    @abstractmethod
    
    # Cada clase hija debe definir su propia forma de describirse.
    def describir(self):
        raise NotImplementedError
