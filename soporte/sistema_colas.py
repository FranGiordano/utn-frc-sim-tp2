import random as rd
import math
import enum


class SistemaColas:

    def __init__(self, semilla):
        """Inicialización del objeto"""

        self._lambda_atencion_interprovincial = None
        self._lambda_atencion_maquina = None
        self._lambda_atencion_cercania = None
        self._media_llegada_pasajero_critico = None
        self._b_llegada_pasajero_moderado = None
        self._a_llegada_pasajero_moderado = None
        self._cte_espera_impaciente = None
        self._hora_inicio_ventanilla_auxiliar = None
        self._hora_inicio_critico = 6
        self._hora_inicio_moderado = 15
        self._hora_fin_moderado = 24
        self._cte_llegada_mecanico = 1.5
        self._media_mantenimiento_maquina = 0.1
        self._desv_est_mantenimiento_maquina = 0.

        self._prob_tipo_atencion_acumulado = {
            self._TipoAtencion.VSIC: 0,
            self._TipoAtencion.VSII: 0.5,
            self._TipoAtencion.VSA: 0.75,
            self._TipoAtencion.MSIC: 0.95
        }

        self._generador = rd.Random(semilla)

    def generar_parametros(self, a_lleg_pasaj_mod, b_lleg_pasaj_mod, media_lleg_pasaj_crit, lamb_cercania,
                           lamb_interprov, lamb_maq, cte_impaciente, hora_inicio_auxiliar):
        """Configuración de parámetros de acuerdo a lo que decida el usuario"""

        self._a_llegada_pasajero_moderado = a_lleg_pasaj_mod
        self._b_llegada_pasajero_moderado = b_lleg_pasaj_mod
        self._media_llegada_pasajero_critico = media_lleg_pasaj_crit
        self._lambda_atencion_cercania = lamb_cercania
        self._lambda_atencion_interprovincial = lamb_interprov
        self._lambda_atencion_maquina = lamb_maq
        self._cte_espera_impaciente = cte_impaciente
        self._hora_inicio_ventanilla_auxiliar = hora_inicio_auxiliar  # El mismo debe ser un valor >6 y <15

    def simular(self, ctd_iteraciones):
        """Ejecución de la simulación"""

        vector_estado = self._inicializar_vector_estado()

        for i in range(ctd_iteraciones):
            pass

    def _inicializar_vector_estado(self):
        """Inicialización del vector estado"""

        vector_estado = [
            0,  # 0. Nro Iteración
            0,  # 1. Reloj
            "Inicio simulación",  # 2. Evento
            None,  # 3. Random 1
            None,  # 4. Tiempo entre llegada pasajeros
            None,  # 5. Próxima llegada pasajero
            None,  # 6. Random 2
            None,  # 7. Próximo tipo de atención de pasajero
            None,  # 8. Tiempo entre llegada mecánicos
            None,  # 9. Próxima llegada mecánico
            None,  # 10. Random 3
            None,  # 11. Tiempo fin atención
            None,  # 12. Estado ventanilla inmediata 1
            None,  # 13. Próximo fin atención ventanilla inmediata 1
            None,  # 14. Cliente siendo atendido ventanilla inmediata 1
            None,  # 15. Estado ventanilla inmediata 2
            None,  # 16. Próximo fin atención ventanilla inmediata 2
            None,  # 17. Cliente siendo atendido ventanilla inmediata 2
            None,  # 18. Estado ventanilla anticipada
            None,  # 19. Random 4
            None,  # 20. Tiempo fin atención ventanilla anticipada
            None,  # 21. Próximo fin atención ventanilla anticipada
            None,  # 22. Estado ventanilla auxiliar
            None,  # 23. Random 5
            None,  # 24. Tiempo fin atención ventanilla auxiliar
            None,  # 25. Próximo fin atención ventanilla auxiliar
            None,  # 26. Estado máquina
            None,  # 27. Random 6
            None,  # 28. Tiempo fin atención máquina
            None,  # 29. Próximo fin atención máquina
            None,  # 30. Random 7
            None,  # 31. Random 8
            None,  # 32. Tiempo fin mantenimiento máquina
            None,  # 33. Próximo fin mantenimiento máquina
            None,  # 34. Próximo fin impaciencia
            self._hora_inicio_critico,  # 35. Próximo inicio hora crítica
            self._hora_inicio_ventanilla_auxiliar,  # 36. Próximo inicio hora ventanilla auxiliar
            self._hora_inicio_moderado,  # 37. Próximo inicio hora moderada
            self._hora_fin_moderado,  # 38. Próximo fin hora moderada
            0,  # 39. Cola salida inmediata
            0,  # 40. Cola salida anticipada
            0,  # 41. Cola máquina
            0,  # 42. Ctd pasajeros anticipada que pasaron a ser atendidos
            0,  # 43. Ctd pasajeros anticipada que perdieron el tren
            0,  # 44. Ctd pasajeros que usaron la máquina
            0,  # 45. Ctd pasajeros que fueron interrumpidos en la máquina
            0,  # 46. Acum Tiempo que la ventanilla inmediata 1 estuvo libre
            0,  # 47. Acum Tiempo que la ventanilla inmediata 1 estuvo ocupada
            0,  # 48. Pct ocupación ventanilla inmediata 1 (ocupada / (libre+ocupada))
            0,  # 49. Pct pasajeros anticipada que perdieron el tren (perdieron / (perdieron+atendidos))
            0,  # 50. Pct pasajeros interrumpidos al usar la máquina
            [],  # 51. (y más) Pasajeros
        ]

        return vector_estado

    # Método de selección de evento

    def _siguiente_evento(self, vector_estado):
        """Se chequea cual es el siguiente evento en base al vector de estados y ejecuta el método correspondiente"""

        # Si la simulación recién empieza, lo lógico es que primero suceda el inicio del horario crítico
        if vector_estado[2] == "Inicio simulación":
            return self._inicio_hora_critica(vector_estado)

        # Se procede a buscar el siguiente evento en base al horario
        horarios = {
            vector_estado[5]: self._llegada_pasajero,
            vector_estado[9]: self._llegada_mecanico,
            vector_estado[13]: self._fin_atencion_ventanilla_inmediata1,
            vector_estado[16]: self._fin_atencion_ventanilla_inmediata2,
            vector_estado[21]: self._fin_atencion_ventanilla_anticipada,
            vector_estado[25]: self._fin_atencion_ventanilla_auxiliar,
            vector_estado[29]: self._fin_atencion_maquina,
            vector_estado[33]: self._fin_mantenimiento_maquina,
            vector_estado[34]: self._fin_espera_impaciente,
            vector_estado[35]: self._inicio_hora_critica,
            vector_estado[36]: self._inicio_hora_ventanilla_auxiliar,
            vector_estado[37]: self._inicio_hora_moderada,
            vector_estado[38]: self._fin_hora_moderada
        }

        # Se ejecuta el método correspondiente al evento
        minimo_siguiente = min([i for i in list(horarios.keys()) if i > vector_estado[1]])

        return horarios[minimo_siguiente](vector_estado)

    # Métodos de eventos

    def _inicio_hora_critica(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Iteracion
        nuevo_vector_estado[0] += 1

        # Reloj
        nuevo_vector_estado[1] = vector_estado[35]

        # Evento
        nuevo_vector_estado[2] = "Inicio hora crítica"

        # Nuevo pasajero (para inicio de simulación)
        if nuevo_vector_estado[5] is None:
            nuevo_vector_estado[3] = self._generador.random()
            nuevo_vector_estado[4] = self._proxima_llegada_pasajero(nuevo_vector_estado[3])
            nuevo_vector_estado[5] = nuevo_vector_estado[4] + nuevo_vector_estado[1]
            nuevo_vector_estado[6] = self._generador.random()
            nuevo_vector_estado[7] = self._

    def _llegada_pasajero(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Llegada pasajero"

    def _llegada_mecanico(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Llegada mecánico"

    def _fin_atencion_ventanilla_inmediata1(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Fin atención ventanilla inmediata 1"

    def _fin_atencion_ventanilla_inmediata2(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Fin atención ventanilla inmediata 2"

    def _fin_atencion_ventanilla_anticipada(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Fin atención ventanilla anticipada"

    def _fin_atencion_ventanilla_auxiliar(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Fin atención ventanilla auxiliar"

    def _fin_atencion_maquina(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Fin atención máquina"

    def _fin_mantenimiento_maquina(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Fin mantenimiento máquina"

    def _fin_espera_impaciente(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Fin espera impaciente"

    def _inicio_hora_moderada(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Inicio hora moderada"

    def _inicio_hora_ventanilla_auxiliar(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Inicio hora ventanilla auxiliar"

    def _fin_hora_moderada(self, vector_estado):

        nuevo_vector_estado = [] * len(vector_estado)

        # Evento
        nuevo_vector_estado[2] = "Fin hora moderada"

    # Métodos auxiliares

    def _proxima_llegada_pasajero(self, rand):
        """Devuelve el próximo tiempo de llegada de pasajero en base a un número [0, 1)"""

        n = rand
        n *= (self._b_llegada_pasajero_moderado - self._a_llegada_pasajero_moderado)
        n += self._a_llegada_pasajero_moderado

        return n

    def _proximo_tipo_atencion(self, rand):
        """Devuelve el próximo tipo de atención en base a un número [0, 1)"""

        for i in enumerate(self._prob_tipo_atencion_acumulado):


    # Clases auxiliares

    class _Pasajero:
        def __init__(self, nro, tipo_atencion, estado, hora_inicio):
            self.nro = nro,
            self.tipo_atencion = tipo_atencion,
            self.estado = estado,
            self.hora_inicio = hora_inicio

    class _TipoAtencion(enum.Enum):
        VSIC = "En ventanilla salida inmediata cercanía"
        VSII = "En ventanilla salida inmediata interprovincial"
        VSA = "En ventanilla salida anticipada"
        MSIC = "En máquina salida inmediata cercanía"

    class _EstadoPasajero(enum.Enum):
        C = "En cola",
        A = "Siendo atendido"
        I = "Interrumpido"
        D = "Destrucción de objeto"

    class _EstadoMecanico(enum.Enum):
        M = "Manteniendo máquina"
        D = "Destrucción de objeto"

    class _EstadoVentanilla(enum.Enum):
        O = "Ocupado"
        L = "Libre"
        D = "Deshabilitado"

    class _EstadoMaquina(enum.Enum):
        O = "Ocupado"
        L = "Libre"
        M = "En mantenimiento"
