import random
from copy import copy
import random as rd
import math
import soporte.runge_kutta as rk


class SistemaColas:
    """
    Clase utilizada para la simulación del sistema de colas de una estación de tren

    Se setean los parámetros configurables con generar_parametros() y se inicia la simulación con simular().
    El método simular() procederá a inicializar un vector de estado con _inicializar_vector_estado(), revisará cual
    es el siguiente evento de la simulación con _obtener_evento() y ejecutará el método correspondiente al evento.
    """

    def __init__(self, semilla):
        """Inicialización del objeto"""

        self._lambda_atencion_interprovincial = None
        self._lambda_atencion_maquina = None
        self._lambda_atencion_cercania = None
        self._lambda_atencion_anticipada = None
        self._media_llegada_pasajero_critico = None
        self._b_llegada_pasajero_moderado = None
        self._a_llegada_pasajero_moderado = None
        self._cte_espera_impaciente = None
        self._hora_inicio_ventanilla_auxiliar = None
        self._total_iteraciones = None
        self._nro_cliente = 0
        self._hora_inicio_critico = 6
        self._hora_inicio_moderado = 15
        self._hora_fin_moderado = 24
        self._cte_llegada_mecanico = 1.5
        self._media_mantenimiento_maquina = 0.05
        self._desv_est_mantenimiento_maquina = 0.01

        self._interrupcion_inicio = 0

        self.bandera = False

        self._tipo_atencion = [
            "En ventanilla salida inmediata cercanía",
            "En ventanilla salida inmediata interprovincial",
            "En ventanilla salida anticipada",
            "En máquina salida inmediata cercanía"
        ]
        self._prob_tipo_atencion_acumulado = [0, 0.5, 0.75, 0.95, 1]

        self._generador = rd.Random(semilla)

    def generar_parametros(self, a_lleg_pasaj_mod, b_lleg_pasaj_mod, media_lleg_pasaj_crit, lamb_cercania,
                           lamb_interprov, lamb_maq, lamb_anticip, cte_impaciente, hora_inicio_auxiliar, total_iter):
        """Configuración de parámetros de acuerdo a lo que decida el usuario"""

        self._a_llegada_pasajero_moderado = a_lleg_pasaj_mod
        self._b_llegada_pasajero_moderado = b_lleg_pasaj_mod
        self._media_llegada_pasajero_critico = media_lleg_pasaj_crit
        self._lambda_atencion_cercania = lamb_cercania
        self._lambda_atencion_interprovincial = lamb_interprov
        self._lambda_atencion_maquina = lamb_maq
        self._lambda_atencion_anticipada = lamb_anticip
        self._cte_espera_impaciente = cte_impaciente
        self._hora_inicio_ventanilla_auxiliar = hora_inicio_auxiliar  # El mismo debe ser un valor >6 y <15
        self._total_iteraciones = total_iter

    def simular(self, ctd_iteraciones, iteracion_a_grabar):
        """Ejecución de la simulación"""

        # Inicialización de parámetros y vector de estado
        self._nro_cliente = 0
        filas_guardadas = []
        vector_anterior = self._inicializar_vector_estado()
        vector_actual = []

        # Ejecución de simulación y anexo de vectores a filas para mostrar
        for i in range(ctd_iteraciones):

            vector_actual = self._siguiente_vector(vector_anterior)

            if iteracion_a_grabar <= (i + 1) < iteracion_a_grabar + self._total_iteraciones:
                filas_guardadas.append(vector_actual)

            if i != (ctd_iteraciones - 1):
                vector_anterior = vector_actual

        # Se anexan los dos últimos vectores en caso de que no hayan sido anexados antes
        if not (iteracion_a_grabar <= (vector_anterior[0]) < iteracion_a_grabar + self._total_iteraciones):
            filas_guardadas.append(vector_anterior)
        if not (iteracion_a_grabar <= (vector_actual[0]) < iteracion_a_grabar + self._total_iteraciones):
            filas_guardadas.append(vector_actual)

        return filas_guardadas

    # Métodos privados principales

    def _inicializar_vector_estado(self):
        """Inicialización del vector estado"""

        vector_estado = [
            0,  # 0. Nro Iteración
            0,  # 1. Reloj (horas transcurridas)
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
            "Deshabilitado",  # 12. Estado ventanilla inmediata 1
            None,  # 13. Próximo fin atención ventanilla inmediata 1
            None,  # 14. Cliente siendo atendido ventanilla inmediata 1
            "Deshabilitado",  # 15. Estado ventanilla inmediata 2
            None,  # 16. Próximo fin atención ventanilla inmediata 2
            None,  # 17. Cliente siendo atendido ventanilla inmediata 2
            "Deshabilitado",  # 18. Estado ventanilla anticipada
            None,  # 19. Random 4
            None,  # 20. Tiempo fin atención ventanilla anticipada
            None,  # 21. Próximo fin atención ventanilla anticipada
            "Deshabilitado",  # 22. Estado ventanilla auxiliar
            None,  # 23. Random 5
            None,  # 24. Tiempo fin atención ventanilla auxiliar
            None,  # 25. Próximo fin atención ventanilla auxiliar
            "Deshabilitado",  # 26. Estado máquina
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
            0,  # 42. Ctd pasajeros anticipada que EMPEZARON a ser atendidos
            0,  # 43. Ctd pasajeros anticipada que perdieron el tren o no fueron atendidos
            0,  # 44. Ctd pasajeros que fueron atendidos en la máquina
            0,  # 45. Ctd pasajeros que fueron interrumpidos en la máquina
            0,  # 46. Acum Tiempo que la ventanilla inmediata 1 estuvo libre
            0,  # 47. Acum Tiempo que la ventanilla inmediata 1 estuvo ocupada
            0,  # 48. Pct ocupación ventanilla inmediata 1 (ocupada / (libre+ocupada))
            0,  # 49. Pct pasajeros anticipada que perdieron el tren (perdieron / (perdieron+atendidos))
            0,  # 50. Pct pasajeros interrumpidos al usar la máquina (interrumpidos / (usaron+interrumpidos))
            [],  # 51. (y más) Pasajeros
            None,  # 52. Cliente siendo atendido en ventanilla auxiliar (Lo añadí tarde, por lo que quedó acá)
            None,  # 53. Cliente siendo atendido en anticipada (idem que 52)
            None,
            # 54. Cliente siendo atendido en maquina (idem que 52 y 53) La idea de estos es facilitar los cálculos

            0,  # "Cont clientes que llegan": i[55],
            None,  # 56 "Demora proxima llegada virus": i[56],
            None,  # 57 "Tiempo proxima llegada virus": i[57],
            None,  # 58 "RND tipo llegada (servidor o llegada)": i[58],
            None,  # 59 "Tipo llegada (servidor o llegada)": i[59],
            None,  # 60 "Tiempo detenido el servicio V1": i[60],
            None,  # 61 "Tiempo servicio V1 normalidad": i[61],
            None,  # 62 Tiempo remanente de cliente interrumpido i[62]
            None,  # 63 "Tiempo detenida la llegada cliente": i[63],
            None,  # 64 "Llegada cliente normalidad": i[64]
            None,  # 65 Valor de B para generar proxima llegada i[65]

            [],   # 66 Cola para clientes despues de llegada virus
            "Normal", # 67 estado sistema [normal, virus]
            0,    # 68 contador de clientes despues de llegada virus.
            0,    # 69 cliente atendido ventanilla 1 que fue interrumpido
        ]

        return vector_estado

    def _siguiente_vector(self, ve):
        """Genera el siguiente vector de estado"""

        # Se instancia un nuevo vector de estado
        nve = copy(ve)

        # Nueva iteración
        nve[0] = ve[0] + 1

        # Cálculo del nuevo evento y tiempo en que sucede
        nve[1], nve[2] = self._obtener_evento(ve)

        # Se mantienen tiempos, estados, clientes atendidos, colas, contadores y acumuladores
        for i in [5, 7, 9, 12, 13, 14, 15, 16, 17, 18, 21, 22, 25, 26, 29, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
                  43, 44, 45, 46, 47, 52, 53, 54, 55, 57, 61, 62, 64, 68, 67]:
            nve[i] = ve[i]

        # Limpieza de cálculos de linea (random + tiempos para realizar sumas con reloj)
        for i in [3, 4, 6, 8, 10, 11, 19, 20, 23, 24, 27, 28, 30, 31, 32, 56, 58, 59, 60, 63, 65]:
            nve[i] = None

        # Se eliminan los pasajeros que ya salieron del sistema
        nve[51] = [copy(i) for i in ve[51] if i.estado != "Destrucción de objeto"]

        #        # Verifico si ya llegue a las 150 llegadas, para generar le inicio de interrupcion

        if nve[55] == 150 and self.bandera == False:
            self._interrupcion_inicio = nve[1]
            b = self._generador.random()
            nve[65] = b
            tablasRK = rk.cuando_detiene(self._interrupcion_inicio, b, 0.001)
            solucion = tablasRK[-1][6]

            tiempo_real = solucion * 1  # pondero el tiempo t = 1 = 30

            nve[56] = tiempo_real
            nve[57] = tiempo_real + nve[1]
            self.bandera = True

        # Ejecución de evento correspondiente al nuevo vector de estado
        match nve[2]:
            case "Llegada pasajero":
                self._llegada_pasajero(nve)
            case "Llegada mecánico":
                self._llegada_mecanico(nve)
            case "Fin atención ventanilla inmediata 1":
                self._fin_atencion_ventanilla_inmediata1(nve)
            case "Fin atención ventanilla inmediata 2":
                self._fin_atencion_ventanilla_inmediata2(nve)
            case "Fin atención ventanilla anticipada":
                self._fin_atencion_ventanilla_anticipada(nve)
            case "Fin atención ventanilla auxiliar":
                self._fin_atencion_ventanilla_auxiliar(nve)
            case "Fin atención máquina":
                self._fin_atencion_o_mantenimiento_maquina(nve)
            case "Fin mantenimiento máquina":
                self._fin_atencion_o_mantenimiento_maquina(nve)
            case "Fin espera impaciente":
                self._fin_espera_impaciente(nve)
            case "Inicio hora crítica":
                self._inicio_hora_critica(nve)
            case "Inicio hora ventanilla auxiliar":
                self._inicio_hora_ventanilla_auxiliar(nve)
            case "Inicio hora moderada":  # El fin de hora ventanilla auxiliar coincide con el inicio de hm
                self._inicio_hora_moderada(nve)
            case "Fin hora moderada":
                self._fin_hora_moderada(nve)

            # nuevos eventos para tp5
            case "Llegada virus":
                self._llegada_virus(nve)
            case "Fin de interrupcion virus servicio":
                self._fin_interrupcion_virus_servicio(nve)
            case "Fin de interrupcion virus cliente":
                self._fin_interrupcion_virus_cliente(nve)
            case _:
                raise ValueError("Se intentó ingresar un evento sin un método correspondiente")

        # Cálculo de acumuladores y métricas:

        nve[46] += nve[1] - ve[1] if ve[12] == "Libre" else 0
        nve[47] += nve[1] - ve[1] if ve[12] == "Ocupado" else 0
        nve[48] = nve[47] / (nve[47] + nve[46]) if (nve[47] + nve[46]) > 0 else 0
        nve[49] = nve[43] / (nve[42] + nve[43]) if (nve[42] + nve[43]) > 0 else 0
        nve[50] = nve[45] / (nve[44] + nve[45]) if (nve[44] + nve[45]) > 0 else 0

        return nve

    def _obtener_evento(self, vector_estado):
        """Devuelve el reloj y evento del próximo vector de estado"""

        horarios = {
            vector_estado[5]: "Llegada pasajero",
            vector_estado[9]: "Llegada mecánico",
            vector_estado[13]: "Fin atención ventanilla inmediata 1",
            vector_estado[16]: "Fin atención ventanilla inmediata 2",
            vector_estado[21]: "Fin atención ventanilla anticipada",
            vector_estado[25]: "Fin atención ventanilla auxiliar",
            vector_estado[29]: "Fin atención máquina",
            vector_estado[33]: "Fin mantenimiento máquina",
            vector_estado[34]: "Fin espera impaciente",
            vector_estado[35]: "Inicio hora crítica",
            vector_estado[36]: "Inicio hora ventanilla auxiliar",
            vector_estado[37]: "Inicio hora moderada",
            # El fin de hora ventanilla auxiliar coincide con el inicio de hm
            vector_estado[38]: "Fin hora moderada",

            # nuevos eventos para tp5
            vector_estado[57]: "Llegada virus",
            vector_estado[61]: "Fin de interrupcion virus servicio",
            vector_estado[64]: "Fin de interrupcion virus cliente",
        }

        minimo_siguiente = min([i for i in list(horarios.keys()) if i is not None and i > vector_estado[1]])

        return minimo_siguiente, horarios[minimo_siguiente]

    # Métodos relacionados a los eventos

    # --------------------------------------------------------------------------
    # Metodo de TP5 relacionadas a los eventos
    def _llegada_virus(self, nve):

        # 1. Ante el evento de llegada de virus genero el tipo de interrupcion.
        rnd_tipo = self._generador.random()
        nve[58] = rnd_tipo

        if rnd_tipo <= 0.35:      # Interrumpo servicio V1.

            nve[59] = "Servicio Ventanilla 1"

            #3. Verifico si esta ocupado, si esta ocupado veo el tiempo remanente
            if nve[12] == "Ocupado":
                nve[62] = nve[13] - nve[1] #calculo remanencia

            nve[12] = "Detenida" # estado ventanilla cambia
            nve[69] = nve[14] #guardo el numero del cliente
            nve[13] = None # elimino fin de atencion cliente
            nve[14] = None

            # 3. genero el tiempo que el servidor esta detenido.
            vectorRK = rk.detencion_servidor(nve[1], 0.001)
            tiempo = vectorRK[-1][6]
            tiempo_real = tiempo * 8  # pondero el tiempo t = 1 = 8
            nve[60] = tiempo_real
            nve[61] = tiempo_real + nve[1]

        else:                   # Interrumpo llegada clientes.

            nve[59] = "Llegada Cliente"

            nve[67] = "virus"

            # 1. genero tiempo que las llegadas estan detenidas
            vectorRk = rk.detencion_cliente(nve[1], 0.001)
            tiempo = vectorRk[-1][6]
            tiempo_real = tiempo * 27  # pondero el tiempo t = 1 =27
            nve[63] = tiempo_real
            nve[64] = tiempo_real + nve[1]

        nve[57] = None


    def _fin_interrupcion_virus_servicio(self, nve):

        '''# atiendo el tiempo restante al cliente que fue interrumpido
        if nve[62] is not None:
            nve[13] = nve[62] + nve[1]  # Genero nuevo fin de atencion
            nve[61] = None #actualizo el valor de fin atencion
        pasajero = self._buscar_pasajero_por_nro(nve[51], nve[14])
        pasajero.estado = "Siendo atendido"'''

        # El cliente que era atendido, ahora va a terminar su atencion

        if nve[62] is not None:
            nve[13] = nve[62] + nve[1] # continuo con el fin de servicio
            nve[14] = nve[69] #pongo el numero del cliente
            nve[62] = None  # elimino el tiempo remanente
        else:
            # Deshabiltiamos la ventanilla si ya se encuentra en el final del día
            if nve[35] < nve[38]:
                nve[12] = "Deshabilitado"

            # Si no hay más pasajeros en cola lo liberamos
            elif nve[39] == 0:
                nve[12] = "Libre"

            # Si hay más pasajeros, lo atendemos
            elif nve[39] > 0:
                nve[39] -= 1

                try:
                    pasajero = self._buscar_primer_pasajero(nve[51], "En cola",
                                                            ["En ventanilla salida inmediata cercanía",
                                                             "En ventanilla salida inmediata interprovincial"])
                except IndexError:
                    print("hjola")
                nve[12], nve[10], nve[11], nve[13], nve[14] = self._atender_pasajero(pasajero, nve[1])

        nve[60] = None # elimino tiempo que estuvo detenido el servico
        nve[61] = None # elimino el tiempo que vuelve servicio a normalidad

        b = self._generador.random()
        nve[65] = b
        tablasRK = rk.cuando_detiene(self._interrupcion_inicio, b, 0.001)
        tiempo_llegada = tablasRK[-1][6]

        tiempo_real = tiempo_llegada * 1  # pondero el tiempo t = 1 = 30

        nve[56] = tiempo_real
        nve[57] = tiempo_real + nve[1]

    def _fin_interrupcion_virus_cliente(self, nve):

        # Genero la proxima detencion de la llegada del cliente.
        b = self._generador.random()
        nve[65] = b
        tablasRK = rk.cuando_detiene(self._interrupcion_inicio, b, 0.001)
        tiempo_llegada = tablasRK[-1][6]
        tiempo_real = tiempo_llegada * 1  # pondero el tiempo t = 1 = 30
        nve[56] = tiempo_real
        nve[57] = tiempo_real + nve[1]

        # Regreso el estado a normal.
        nve[67] = "normal"
        # elimino cuando era el fin de interrupcion del cliente
        nve[64] = None

        nve[51] = nve[51] + nve[66]

        if self._contar_en_cola(nve[51], "En cola",
                                                ["En ventanilla salida inmediata cercanía",
                                                 "En ventanilla salida inmediata interprovincial"]) > 0:

            pasajero_ventanilla = self._buscar_primer_pasajero(nve[51], "En cola",
                                                    ["En ventanilla salida inmediata cercanía",
                                                     "En ventanilla salida inmediata interprovincial"])



            if nve[12] == "Libre":
                nve[12], nve[10], nve[11], nve[13], nve[14] = self._atender_pasajero(pasajero_ventanilla, nve[1])

            elif nve[15] == "Libre":
                nve[15], nve[10], nve[11], nve[16], nve[17] = self._atender_pasajero(pasajero_ventanilla, nve[1])

            elif nve[22] == "Libre":
                nve[22], nve[23], nve[24], nve[25], nve[52] = self._atender_pasajero(pasajero_ventanilla, nve[1])

            else:
                nve[39] += 1


        if self._contar_en_cola(nve[51], "En cola",
                                                           ["En ventanilla salida anticipada"]) > 0:
            pasajero_anticipado = self._buscar_primer_pasajero(nve[51], "En cola",
                                                               ["En ventanilla salida anticipada"])


            if nve[18] == "Libre":
                nve[18], nve[19], nve[20], nve[21], nve[53] = self._atender_pasajero(pasajero_anticipado, nve[1])
                nve[42] += 1

            elif nve[22] == "Libre":
                nve[22], nve[23], nve[24], nve[25], nve[52] = self._atender_pasajero(pasajero_anticipado, nve[1])
                nve[42] += 1

        if self._contar_en_cola(nve[51], "En cola",
                                                           ["En máquina salida inmediata cercanía"])> 0:
            pasajero_maquina = self._buscar_primer_pasajero(nve[51], "En cola",
                                                               ["En máquina salida inmediata cercanía"])

            if nve[26] == "Libre":
                nve[26], nve[27], nve[28], nve[29], nve[54] = self._atender_pasajero(pasajero_maquina, nve[1])
        # Los clientes de la cola de llegada, van a pasar a ser pasajeros

        nve[66] = []
        nve[68] = 0



    # -----------------------------------------------------------------------------
    def _inicio_hora_critica(self, nve):
        """Método que se ejecuta ante el evento Inicio hora crítica"""

        # Nuevo pasajero
        nve[3], nve[4], nve[5], nve[6], nve[7] = self._generar_nueva_llegada_pasajero(nve[1])

        # Nuevo mecánico
        nve[8] = self._cte_llegada_mecanico
        nve[9] = nve[1] + nve[8]

        # Seteamos estados de servidores a Libre
        nve[12] = "Libre"  # Ventanilla 1
        nve[15] = "Libre"  # Ventanilla 2
        nve[18] = "Libre"  # Ventanilla anticipada
        nve[26] = "Libre"  # Máquina


        nve[35] += 24

    def _llegada_pasajero(self, nve):
        """Método que se ejecuta ante el evento Llegada pasajero"""

        # Actualizo el contador del objeto pasajero
        nve[55] += 1

        # Creamos un objeto pasajero
        self._nro_cliente += 1
        pasajero = self._Pasajero(self._nro_cliente, nve[7], "En cola", nve[1])

        # verico que no hay virus en el servidor, Si hay un virus, sumo uno al contador
        # de clientes que llegaron en virus y agrego el cliente a la cola.
        if nve[67] == "virus":
            nve[66].append(pasajero)
            nve[68] += 1
            return True

        # Próxima llegada de pasajero
        nve[3], nve[4], nve[5], nve[6], nve[7] = self._generar_nueva_llegada_pasajero(nve[1])

        # Dependiendo del tipo de atención del pasajero nuevo y si hay lugar, se lo atiende:
        match pasajero.tipo_atencion:
            case "En ventanilla salida inmediata cercanía" | "En ventanilla salida inmediata interprovincial":

                if nve[12] == "Libre":
                    nve[12], nve[10], nve[11], nve[13], nve[14] = self._atender_pasajero(pasajero, nve[1])

                elif nve[15] == "Libre":
                    nve[15], nve[10], nve[11], nve[16], nve[17] = self._atender_pasajero(pasajero, nve[1])

                elif nve[22] == "Libre":
                    nve[22], nve[23], nve[24], nve[25], nve[52] = self._atender_pasajero(pasajero, nve[1])

                else:
                    nve[39] += 1

            case "En ventanilla salida anticipada":

                if nve[18] == "Libre":
                    nve[18], nve[19], nve[20], nve[21], nve[53] = self._atender_pasajero(pasajero, nve[1])
                    nve[42] += 1

                elif nve[22] == "Libre":
                    nve[22], nve[23], nve[24], nve[25], nve[52] = self._atender_pasajero(pasajero, nve[1])
                    nve[42] += 1

                else:
                    # Si no encuentra espacio para ser atendido, se coloca en cola
                    # En el caso de que sea el primero en cola, se calcula el prox fin de impaciencia
                    nve[40] += 1
                    if nve[40] == 1:
                        nve[34] = pasajero.hora_llegada + self._cte_espera_impaciente

            case "En máquina salida inmediata cercanía":

                if nve[26] == "Libre":
                    nve[26], nve[27], nve[28], nve[29], nve[54] = self._atender_pasajero(pasajero, nve[1])
                else:
                    nve[41] += 1

        # Se guarda el nuevo pasajero
        self._guardar_pasajero(nve[51], pasajero)

    def _llegada_mecanico(self, nve):
        """Método que se ejecuta ante el evento Llegada mecánico"""

        # Nuevo mecánico
        nve[8] = self._cte_llegada_mecanico
        nve[9] = nve[1] + nve[8]

        # Se expulsa algún pasajero que esté en máquina
        if nve[26] == "Ocupado":
            nve[29] = None
            nve[41] += 1
            nve[45] += 1

            pasajero = self._buscar_pasajero_por_nro(nve[51], nve[54])
            pasajero.estado = "En cola"
            nve[54] = None

        # Se coloca la máquina en mantenimiento
        nve[26] = "En mantenimiento"

        nve[30] = self._generador.random()
        nve[31] = self._generador.random()
        nve[32] = self._proximo_tiempo_mantenimiento_maquina(nve[30], nve[31])
        nve[33] = nve[32] + nve[1]

    def _contar_en_cola(self, pasajeros, estado, lista_tipo_atencion):
        """Devuelve la cantidad en coladado un estado y una lista de tipos de atención"""

        c = 0
        for pasajero in pasajeros:
            if pasajero.estado == estado and pasajero.tipo_atencion in lista_tipo_atencion:
                c += 1
        # Se levanta un error en caso de que no se haya encontrado ningún pasajero en la lista.
        return c

    def _fin_atencion_ventanilla_inmediata1(self, nve):
        """Método que se ejecuta ante el evento Fin atención ventanilla inmediata 1"""

        # Marcamos al pasajero como atendido
        pasajero = self._buscar_pasajero_por_nro(nve[51], nve[14])
        pasajero.estado = "Destrucción de objeto"
        nve[13] = None
        nve[14] = None

        # Deshabiltiamos la ventanilla si ya se encuentra en el final del día
        if nve[35] < nve[38]:
            nve[12] = "Deshabilitado"

        # Si no hay más pasajeros en cola lo liberamos
        elif nve[39] == 0:
            nve[12] = "Libre"

        # Si hay más pasajeros, lo atendemos
        elif nve[39] > 0:
            nve[39] -= 1

            try:
                pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida inmediata cercanía",
                                                                             "En ventanilla salida inmediata interprovincial"])
            except IndexError:
                print("hjola")
            nve[12], nve[10], nve[11], nve[13], nve[14] = self._atender_pasajero(pasajero, nve[1])

    def _fin_atencion_ventanilla_inmediata2(self, nve):
        """Método que se ejecuta ante el evento Fin atención ventanilla inmediata 2"""

        # Marcamos al pasajero como atendido
        pasajero = self._buscar_pasajero_por_nro(nve[51], nve[17])
        pasajero.estado = "Destrucción de objeto"
        nve[16] = None
        nve[17] = None

        # Deshabilitamos la ventanilla si ya se encuentra en hora moderada
        if nve[37] > nve[35]:
            nve[15] = "Deshabilitado"

        # Si no hay más pasajeros en cola lo liberamos
        elif nve[39] == 0:
            nve[15] = "Libre"

        # Si hay más pasajeros, lo atendemos
        elif nve[39] > 0 and self._contar_en_cola(nve[51], "En cola", ["En ventanilla salida inmediata cercanía",
                                                                "En ventanilla salida inmediata interprovincial"]) > 0:
            nve[39] -= 1
            pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida inmediata cercanía",
                                                                         "En ventanilla salida inmediata interprovincial"])
            nve[15], nve[10], nve[11], nve[16], nve[17] = self._atender_pasajero(pasajero, nve[1])

    def _fin_atencion_ventanilla_anticipada(self, nve):
        """Método que se ejecuta ante el evento Fin atención ventanilla anticipada"""

        # Marcamos al pasajero como atendido:
        pasajero = self._buscar_pasajero_por_nro(nve[51], nve[53])
        pasajero.estado = "Destrucción de objeto"
        nve[53] = None
        nve[21] = None

        # Deshabiltiamos la ventanilla si ya se encuentra en el final del día
        if nve[35] < nve[38]:
            nve[18] = "Deshabilitado"

        # Si no hay más pasajeros en cola lo liberamos
        elif nve[40] == 0:
            nve[18] = "Libre"

        # Si hay más pasajeros, lo asignamos a ventanilla
        else:
            nve[40] -= 1
            nve[34] = None
            pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida anticipada"])
            nve[18], nve[19], nve[20], nve[21], nve[53] = self._atender_pasajero(pasajero, nve[1])
            nve[42] += 1

            # Si quedaron pasajeros en cola, se recalcula el fin de impaciencia
            if nve[40] > 0:
                pasajero_impaciencia = self._buscar_primer_pasajero(nve[51], "En cola",
                                                                    ["En ventanilla salida anticipada"])
                nve[34] = self._cte_espera_impaciente + pasajero_impaciencia.hora_llegada
            else:
                nve[34] = None

    def _fin_atencion_ventanilla_auxiliar(self, nve):
        """Método que se ejecuta ante el evento Fin atención ventanilla auxiliar

        Se acordó en este caso que la ventanilla auxiliar abre teniendo en cuenta un parámetro configurables
        que debe ser mayor que el inicio de hora crítica y menor que el inicio de hora moderada,
        y cierra en el final de la hora crítica.
        """

        # Marcamos al pasajero como atendido:
        pasajero = self._buscar_pasajero_por_nro(nve[51], nve[52])
        pasajero.estado = "Destrucción de objeto"
        nve[25] = None
        nve[52] = None

        # Deshabilitamos la ventanilla si ya se encuentra en hora moderada
        if nve[37] > nve[35]:
            nve[22] = "Deshabilitado"

        # Si no hay más pasajeros en cola lo liberamos
        elif nve[39] == 0 and nve[40] == 0:
            nve[22] = "Libre"

        # Revisamos si hay pasajeros en cola
        # Chequeo en cola inmediata
        elif nve[39] > 0:
            nve[39] -= 1
            pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida inmediata cercanía",
                                                                         "En ventanilla salida inmediata interprovincial"])
            nve[22], nve[23], nve[24], nve[25], nve[52] = self._atender_pasajero(pasajero, nve[1])

        # Chequeo en cola anticipada
        elif nve[40] > 0:

            nve[40] -= 1
            nve[34] = None
            pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida anticipada"])
            nve[22], nve[23], nve[24], nve[25], nve[52] = self._atender_pasajero(pasajero, nve[1])

            # Si quedaron pasajeros en cola, se recalcula el fin de impaciencia
            if nve[40] > 0:
                pasajero_impaciencia = self._buscar_primer_pasajero(nve[51], "En cola",
                                                                    ["En ventanilla salida anticipada"])
                nve[34] = self._cte_espera_impaciente + pasajero_impaciencia.hora_llegada
            else:
                nve[34] = None

    def _fin_atencion_o_mantenimiento_maquina(self, nve):
        """Método que se ejecuta ante el evento Fin atención máquina o Fin mantenimiento máquina"""

        # Si es fin de atencion, entonces tiene un pasajero, y lo sacamos.
        # En el caso contrario, estamos hablando de un mantenimiento.
        if nve[54] is None:
            nve[33] = None
        else:
            # Marcamos al pasajero como atendido:
            pasajero = self._buscar_pasajero_por_nro(nve[51], nve[54])
            pasajero.estado = "Destrucción de objeto"
            nve[29] = None
            nve[54] = None
            nve[44] += 1

        # Deshabiltiamos la máquina si ya se encuentra en el final del día
        if nve[35] < nve[38]:
            nve[26] = "Deshabilitado"

        # Si no hay más pasajeros en cola lo liberamos
        elif nve[41] == 0:
            nve[26] = "Libre"

        # Si hay pasajeros en cola, lo atendemos
        elif nve[41] > 0:
            nve[41] -= 1
            pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En máquina salida inmediata cercanía"])
            nve[26], nve[27], nve[28], nve[29], nve[54] = self._atender_pasajero(pasajero, nve[1])

    def _fin_espera_impaciente(self, nve):
        """Método que se ejecuta ante el evento Fin espera impaciente"""

        # Aclaración: se expulsa al primer pasajero en cola

        # Destruimos objeto del pasajero que se retira
        pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida anticipada"])
        pasajero.estado = "Destrucción de objeto"
        nve[40] -= 1
        nve[43] += 1

        # Si quedaron pasajeros en cola, se recalcula el fin de impaciencia
        if nve[40] > 0:
            pasajero_impaciencia = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida anticipada"])
            nve[34] = self._cte_espera_impaciente + pasajero_impaciencia.hora_llegada
        else:
            nve[34] = None

    def _inicio_hora_moderada(self, nve):
        """Método que se ejecuta ante el evento Inicio hora moderada"""

        # Deshabilitamos la ventanilla inmediata 2 y auxiliar sólo si están libres
        if nve[15] == "Libre":
            nve[15] = "Deshabilitado"
        if nve[22] == "Libre":
            nve[22] = "Deshabilitado"

        nve[37] += 24

    def _inicio_hora_ventanilla_auxiliar(self, nve):
        """Método que se ejecuta ante el evento Inicio hora ventanilla auxiliar"""

        # Habilitamos la ventanilla auxiliar, si hay pasajeros en cola los atiende
        # Revisamos si hay pasajeros en cola
        # Chequeo en cola inmediata
        if nve[39] > 0:
            nve[39] -= 1
            pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida inmediata cercanía",
                                                                         "En ventanilla salida inmediata interprovincial"])
            nve[22], nve[23], nve[24], nve[25], nve[52] = self._atender_pasajero(pasajero, nve[1])

        # Chequeo en cola anticipada
        elif nve[40] > 0:
            nve[40] -= 1
            nve[34] = None
            pasajero = self._buscar_primer_pasajero(nve[51], "En cola", ["En ventanilla salida anticipada"])
            nve[22], nve[23], nve[24], nve[25], nve[52] = self._atender_pasajero(pasajero, nve[1])

            if nve[40] > 0:
                pasajero_impaciencia = self._buscar_primer_pasajero(nve[51], "En cola",
                                                                    ["En ventanilla salida anticipada"])
                nve[34] = nve[1] + pasajero_impaciencia.hora_llegada
            else:
                nve[34] = None

        else:
            nve[22] = "Libre"

        nve[36] += 24

    def _fin_hora_moderada(self, nve):
        """Método que se ejecuta ante el evento Fin hora moderada"""

        # Deshabilitamos las ventanillas y máquinas que estén libres
        if nve[12] == "Libre":
            nve[12] = "Deshabilitado"
        if nve[18] == "Libre":
            nve[18] = "Deshabilitado"
        if nve[26] == "Libre":
            nve[26] = "Deshabilitado"

        # Seteamos a None la próxima llegada de pasajero y mecánico, y fin empaciencia
        nve[5] = None
        nve[7] = None
        nve[9] = None
        nve[34] = None

        # Seteamos las colas a 0
        nve[39] = 0
        nve[43] += nve[40]
        nve[40] = 0
        nve[41] = 0

        # Destrucción de objetos de pasajeros en cola
        for i in nve[51]:
            if i.estado == "En cola":
                i.estado = "Destrucción de objeto"

        nve[38] += 24

    def _proxima_llegada_pasajero(self, rand, reloj):
        """Devuelve el próximo tiempo de llegada de pasajero discriminando si está en hora moderada o crítica"""

        reloj %= 24

        if reloj >= self._hora_inicio_moderado:
            return rand * (
                    self._b_llegada_pasajero_moderado - self._a_llegada_pasajero_moderado) + self._a_llegada_pasajero_moderado

        if reloj < self._hora_inicio_moderado:
            return -self._media_llegada_pasajero_critico * math.log(1 - rand)

    def _proximo_tipo_atencion(self, rand):
        """Devuelve el próximo tipo de atención del pasajero que va a llegar"""

        for j in range(len(self._prob_tipo_atencion_acumulado)):
            if self._prob_tipo_atencion_acumulado[j] <= rand < self._prob_tipo_atencion_acumulado[j + 1]:
                return self._tipo_atencion[j]

    def _proximo_tiempo_atencion(self, rand, tipo_atencion):
        """Devuelve el próximo tiempo de atención discriminando el tipo de atención del pasajero.

        Este método es válido para los siguientes servidores:
        - Atención en ventanilla para salida inmediata (1 y 2)
        - Atención en ventanilla para salida anticipada
        - Atención en ventanilla auxiliar
        - Atención en máquina para salida inmediata cercanía
        """

        match tipo_atencion:
            case "En ventanilla salida inmediata cercanía":
                return -(1 / self._lambda_atencion_cercania) * math.log(1 - rand)
            case "En ventanilla salida inmediata interprovincial":
                return -(1 / self._lambda_atencion_interprovincial) * math.log(1 - rand)
            case "En ventanilla salida anticipada":
                return -(1 / self._lambda_atencion_anticipada) * math.log(1 - rand)
            case "En máquina salida inmediata cercanía":
                return -(1 / self._lambda_atencion_maquina) * math.log(1 - rand)

    def _proximo_tiempo_mantenimiento_maquina(self, rand1, rand2):
        """Devuelve el próximo tiempo de mantenimiento de la máquina"""

        while rand1 == 0:
            rand1 = self._generador.random()

        z = math.sqrt(-2.0 * math.log(rand1)) * math.cos(2 * math.pi * rand2)

        return self._media_mantenimiento_maquina + self._desv_est_mantenimiento_maquina * z

    def _proximo_tiempo_interrupcion(self):
        """Devuelve el próximo tiempo de mantenimiento de la máquina"""
        rand1 = 0
        while rand1 == 0:
            rand1 = self._generador.random()

        return rand1

    def _crear_pasajero(self, tipo_atencion, hora_llegada):
        """Crea un objeto de la clase Pasajero"""

        self._nro_cliente += 1
        return self._Pasajero(self._nro_cliente, tipo_atencion, "En cola", hora_llegada)

    def _guardar_pasajero(self, pasajeros, pasajero):
        """Guarda un objeto de la clase Pasajero en una lista de pasajeros"""

        for i in pasajeros:
            if i.estado == "Destrucción de objeto":
                i.nro = pasajero.nro
                i.estado = pasajero.estado
                i.hora_llegada = pasajero.hora_llegada
                i.tipo_atencion = pasajero.tipo_atencion
                break
        else:
            pasajeros.append(pasajero)

    def _buscar_primer_pasajero(self, pasajeros, estado, lista_tipo_atencion):
        """Devuelve el primer pasajero (en orden de llegada) dado un estado y una lista de tipos de atención"""

        primer_pasajero = None

        for pasajero in pasajeros:
            if pasajero.estado == estado and pasajero.tipo_atencion in lista_tipo_atencion:
                if primer_pasajero is None or primer_pasajero.hora_llegada > pasajero.hora_llegada:
                    primer_pasajero = pasajero

        # Se levanta un error en caso de que no se haya encontrado ningún pasajero en la lista.
        if primer_pasajero is None:
            error = f"No se encontró ningún pasajero de estado: '{estado}' y lista: {lista_tipo_atencion} \n" \
                    f"La lista de pasajeros cuenta con los siguientes clientes: \n"
            for i in pasajeros:
                error += f"{i.nro} - {i.estado} - {i.tipo_atencion} \n"
            raise Exception(error)

        return primer_pasajero

    def _buscar_pasajero_por_nro(self, pasajeros, nro):
        """Devuelve un pasajero dado su número"""

        for i in pasajeros:
            if i.nro == nro:
                return i
        else:
            error = f"No se encontró ningún pasajero de número {nro} \n" \
                    f"La lista de pasajeros cuenta con los siguientes clientes: \n"
            for i in pasajeros:
                error += f"{i.nro} - {i.estado} - {i.tipo_atencion} \n"
            raise Exception(error)

    def _generar_nueva_llegada_pasajero(self, reloj):
        """Genera el proceso del cálculo del próximo tiempo de llegada de pasajero con su correspondiente tipo de atención"""

        rand1 = self._generador.random()
        tiempo_llegada = self._proxima_llegada_pasajero(rand1, reloj)
        prox_llegada = tiempo_llegada + reloj
        rand2 = self._generador.random()
        prox_tipo_atencion = self._proximo_tipo_atencion(rand2)
        return rand1, tiempo_llegada, prox_llegada, rand2, prox_tipo_atencion

    def _atender_pasajero(self, pasajero, reloj):
        """Genera el proceso de atención de un pasajero en un servidor

        Este método es válido para los siguientes servidores:
        - Atención en ventanilla para salida inmediata (1 y 2)
        - Atención en ventanilla para salida anticipada
        - Atención en ventanilla auxiliar
        - Atención en máquina para salida inmediata cercanía
        """

        estado = "Ocupado"
        rand = self._generador.random()
        tiempo_atencion = self._proximo_tiempo_atencion(rand, pasajero.tipo_atencion)
        prox_fin_atencion = reloj + tiempo_atencion
        cliente_atendido = pasajero.nro
        pasajero.estado = "Siendo atendido"
        return estado, rand, tiempo_atencion, prox_fin_atencion, cliente_atendido

    # Clases auxiliares

    class _Pasajero:
        def __init__(self, nro, tipo_atencion, estado, hora_llegada):
            self.nro = nro
            self.tipo_atencion = tipo_atencion
            self.estado = estado
            self.hora_llegada = hora_llegada


# runge kutta para interrupcion de inicio
def runge_kutta_cuarto_orden_interrupcion_inicio(self, A, dt):
    rand1 = 0
    while rand1 == 0:
        rand1 = self._generador.random()

    beta = rand1
    a_inicial = A
    # Lista para almacenar los valores de cada iteración:
    # (tiempo_inicio, A, K1, K2, K3, K4, tiempo_siguiente, A_siguiente)
    iteraciones = [(0, A, 0, 0, 0, 0, 0)]

    tiempo = 0

    while condicion_corte_inicio(a_inicial, A):
        # Calcular los valores de K1, K2, K3 y K4
        K1 = beta * A
        K2 = beta * (A + 0.5 * K1 * dt)
        K3 = beta * (A + 0.5 * K2 * dt)
        K4 = beta * (A + K3 * dt)

        # Calcular el siguiente valor de A utilizando el método de Runge-Kutta de cuarto orden
        A_siguiente = A + (dt / 6) * (K1 + 2 * K2 + 2 * K3 + K4)

        tiempo_siguiente = tiempo + dt

        iteraciones.append(
            (tiempo, A, K1, K2, K3, K4, tiempo_siguiente, A_siguiente))  # Agregar los valores a la lista de iteraciones

        A = A_siguiente  # Actualizar el valor de A para la próxima iteración
        tiempo = tiempo_siguiente

        return iteraciones, tiempo


def condicion_corte_inicio(A_inicial, A_actual):
    return (A_actual < 3 * A_inicial),


# runge kutta para detencion del sistema
def runge_kutta_cuarto_orden_detencion_sistema(L, dt):
    iteraciones = [(0, L, 0, 0, 0, 0,
                    0)]  # Lista para almacenar los valores de cada iteración: (tiempo_inicio, L, K1, K2, K3, K4, tiempo_siguiente, L_siguiente)
    tiempo = 0.01
    iteracion_actual = 0
    L_anterior = 0

    while condicion_corte_detencion_sistema(L, L_anterior):
        # Calcular los valores de K1, K2, K3 y K4
        K1 = - (L / (0.8 * tiempo ** 2)) - L
        K2 = - ((L + 0.5 * K1 * dt) / (0.8 * (tiempo + 0.5 * dt) ** 2)) - (L + 0.5 * K1 * dt)
        K3 = - ((L + 0.5 * K2 * dt) / (0.8 * (tiempo + 0.5 * dt) ** 2)) - (L + 0.5 * K2 * dt)
        K4 = - ((L + K3 * dt) / (0.8 * (tiempo + dt) ** 2)) - (L + K3 * dt)

        # Calcular el siguiente valor de L utilizando el método de Runge-Kutta de cuarto orden
        L_siguiente = L + (dt / 6) * (K1 + 2 * K2 + 2 * K3 + K4)

        tiempo_siguiente = tiempo + dt

        iteraciones.append(
            (tiempo, L, K1, K2, K3, K4, tiempo_siguiente, L_siguiente))  # Agregar los valores a la lista de iteraciones

        L_anterior = L
        L = L_siguiente  # Actualizar el valor de L para la próxima iteración
        tiempo = tiempo_siguiente
        iteracion_actual += 1

    return iteraciones, tiempo


def condicion_corte_detencion_sistema(L, L_siguiente):
    return abs(L - L_siguiente) > 1


def runge_kutta_cuarto_orden_detencion_cliente(S, dt, reloj_actual):
    iteraciones = [(0, S, 0, 0, 0, 0,
                    0)]  # Lista para almacenar los valores de cada iteración: (tiempo_inicio, S, K1, K2, K3, K4, tiempo_siguiente, S_anterior)
    tiempo = 0
    iteracion_actual = 0
    S_anterior = S

    while condicion_corte_detencion_cliente(S, reloj_actual):
        # Calcular los valores de K1, K2, K3 y K4
        K1 = (0.2 * S) + 3 - tiempo
        K2 = (0.2 * (S + 0.5 * K1 * dt)) + 3 - (tiempo + 0.5 * dt)
        K3 = (0.2 * (S + 0.5 * K2 * dt)) + 3 - (tiempo + 0.5 * dt)
        K4 = (0.2 * (S + K3 * dt)) + 3 - (tiempo + dt)

        # Calcular el siguiente valor de S utilizando el método de Runge-Kutta de cuarto orden
        S_siguiente = S + (dt / 6) * (K1 + 2 * K2 + 2 * K3 + K4)

        tiempo_siguiente = tiempo + dt

        iteraciones.append(
            (tiempo, S, K1, K2, K3, K4, tiempo_siguiente, S_siguiente))  # Agregar los valores a la lista de iteraciones

        S_anterior = S  # Almacenar el valor de S en la iteración anterior
        S = S_siguiente  # Actualizar el valor de S para la próxima iteración
        tiempo = tiempo_siguiente
        iteracion_actual += 1

    return iteraciones


def condicion_corte_detencion_cliente(S, reloj):
    return S * 1.50 > reloj  # no se como plantear esta condicion


# =====================================================================================================================
#
# TESTS
#
# =====================================================================================================================


def test_cola():
    from tabulate import tabulate

    a_lleg_pasaj_mod = 0.0063
    b_lleg_pasaj_mod = 0.0292
    media_lleg_pasaj_crit = 0.0106
    lamb_cercania = 80
    lamb_interprov = 40
    lamb_maq = 30
    lamb_anticip = 25
    cte_impaciente = 0.33
    hora_inicio_auxiliar = 12  # Valor entre 6 y 15

    simulador = SistemaColas(semilla=1)
    simulador.generar_parametros(
        a_lleg_pasaj_mod,
        b_lleg_pasaj_mod,
        media_lleg_pasaj_crit,
        lamb_cercania,
        lamb_interprov,
        lamb_maq,
        lamb_anticip,
        cte_impaciente,
        hora_inicio_auxiliar
    )
    filas = simulador.simular(50000, 9500)

    print(tabulate(filas, headers=[str(i) for i in range(len(filas[0]))]))

    print(filas[-1][39])
    print(filas[-1][40])
    print(filas[-1][41])
    print(sum([1 for i in filas[-1][51] if i.estado != "Destrucción de objeto" and i.estado != "Siendo atendido"]))
    for i in filas[-1][51]:
        print(i.nro, "-", i.estado, "-", i.tipo_atencion)


if __name__ == "__main__":
    import time

    print("Ejecución inicializada")
    start = time.time()
    test_cola()
    end = time.time()
    print(f"Tiempo transcurrido: {round(end - start, 2)} segundos")
