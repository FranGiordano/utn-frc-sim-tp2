import random as rd


class MonteCarloLavarropa:
    def __init__(self, semilla=None):
        """Inicializa una instancia, debiendo especificar la semilla del generador"""

        self.semilla = semilla
        self._generador_nros_aleatorios = rd.Random(semilla)
        self.costo_pedido = None
        self.costo_mantenimiento = None
        self.costo_sobrepaso = None
        self.stock_inicial = None
        self.capacidad_maxima = None
        self.consumos_demanda = None
        self.prob_acum_demanda = None
        self.tamanios_pedido = None
        self.prob_acum_pedido = None

    def establecer_tabla_demanda(self, lista_consumos_demanda, lista_probabilidades_demanda):
        """Establece los datos de la tabla de probabilidad de demanda"""

        self.consumos_demanda = lista_consumos_demanda
        self.prob_acum_demanda = [0]
        for i in range(len(lista_probabilidades_demanda)):
            self.prob_acum_demanda.append(self.prob_acum_demanda[i] + lista_probabilidades_demanda[i])

    def establecer_tabla_pedido(self, lista_tamanios_pedido, lista_probabilidades_pedido):
        """Establece los datos de la tabla de probabilidad de pedidos"""

        self.tamanios_pedido = lista_tamanios_pedido
        self.prob_acum_pedido = [0]
        for i in range(len(lista_probabilidades_pedido)):
            self.prob_acum_pedido.append(self.prob_acum_pedido[i] + lista_probabilidades_pedido[i])

    def establecer_parametros_negocio(self, costo_pedido, costo_mantenimiento, costo_sobrepaso, stock_inicial,
                                      capacidad_maxima):
        """Establece los parámetros del negocio"""

        self.costo_pedido = costo_pedido
        self.costo_mantenimiento = costo_mantenimiento
        self.costo_sobrepaso = costo_sobrepaso
        self.stock_inicial = stock_inicial
        self.capacidad_maxima = capacidad_maxima

    def simular(self, cantidad_simulaciones, semana_a_grabar):
        """Realiza la simulación"""

        # Inicialización de variables
        filas_guardadas = []
        fila_actual = []

        # Cálculos de costos de mantenimientos y de sobrepaso iniciales en caso de existir un stock inicial
        costo_mantenimiento_inicial = self._calcular_costo_mantenimiento(self.stock_inicial)
        costo_sobrepaso_inicial = self._calcular_costo_sobrepaso(self.stock_inicial)
        costo_total_inicial = self.costo_pedido + costo_mantenimiento_inicial + costo_sobrepaso_inicial

        # Para la semana 0, se encarga un pedido de tal forma que exista uno para la semana 1
        fila_anterior = [
            0,                              # 0) Semana
            0,                              # 1) Probabilidad de consumo
            0,                              # 2) Consumo semanal
            0,                              # 3) Probabilidad de pedido
            0,                              # 4) Tamaño de pedido
            self.stock_inicial,             # 5) Stock
            self.costo_pedido,              # 6) Costo de pedido
            costo_mantenimiento_inicial,    # 7) Costo de mantenimiento
            costo_sobrepaso_inicial,        # 8) Costo de sobrepaso
            costo_total_inicial,            # 9) Costo total
            costo_total_inicial             # 10) Costo total acumulado
        ]

        # Ejecución de simulación por semana
        for i in range(cantidad_simulaciones):

            fila_actual = self._calcular_siguiente_fila(fila_anterior)

            # En el caso de que la semana esté dentro del rango a grabar, se lo adjunta en una lista
            if semana_a_grabar <= (i + 1) < semana_a_grabar + 500:
                filas_guardadas.append(fila_actual)

            if i != (cantidad_simulaciones - 1):
                fila_anterior = fila_actual

        return filas_guardadas, fila_actual, fila_anterior

    def _obtener_tamanio_pedido(self, prob_pedido):
        """Devuelve el tamaño de un pedido dada una probabilidad ingresada como parámetro"""

        for i in range(len(self.tamanios_pedido)):
            if self.prob_acum_pedido[i] <= prob_pedido < self.prob_acum_pedido[i+1]:
                return self.tamanios_pedido[i]

    def _obtener_consumo_demanda(self, prob_demanda):
        """Devuelve el consumo de una semana dada una probabilidad ingresada como parámetro"""

        for i in range(len(self.consumos_demanda)):
            if self.prob_acum_demanda[i] <= prob_demanda < self.prob_acum_demanda[i + 1]:
                return self.consumos_demanda[i]

    def _calcular_costo_mantenimiento(self, stock):
        """Devuelve el costo de mantenimiento dado un stock"""
        if stock > self.capacidad_maxima:
            km = (self.capacidad_maxima * self.costo_mantenimiento)
        elif 0 < stock <= self.capacidad_maxima:
            km = (stock * self.costo_mantenimiento)
        else:
            km = 0
        return km

    def _calcular_costo_sobrepaso(self, stock):
        """Devuelve el costo de sobrepaso dado un stock"""
        if stock > self.capacidad_maxima:
            ks = (stock - self.capacidad_maxima) * self.costo_sobrepaso
        else:
            ks = 0
        return ks

    def _calcular_siguiente_fila(self, fila_anterior):

        # Cálculo del nuevo vector de estado
        semana = fila_anterior[0] + 1
        prob_consumo = self._generador_nros_aleatorios.random()
        consumo = self._obtener_consumo_demanda(prob_consumo)
        prob_pedido = self._generador_nros_aleatorios.random()
        pedido = self._obtener_tamanio_pedido(prob_pedido)
        stock = pedido + fila_anterior[5] - consumo
        k0 = self.costo_pedido
        km = self._calcular_costo_mantenimiento(stock)
        ks = self._calcular_costo_sobrepaso(stock)
        costo_total = k0 + km + ks
        costo_total_acumulado = fila_anterior[10] + costo_total

        return [semana, prob_consumo, consumo, prob_pedido, pedido, stock, k0, km, ks, costo_total,
                costo_total_acumulado]


def test():

    inventario = 25000
    stock = 0
    c_sobrepaso = 15000
    c_mantenimiento = 6000
    c_pedido = 550000
    simulacion = 10 ** 7
    semana = 0
    semilla = -1
    consumo_demanda = [6000, 7000, 8000, 9000, 10000, 11000]
    prob_demanda = [0.05, 0.15, 0.2, 0.3, 0.2, 0.1]
    tamanio_pedido = [8000, 11000]
    prob_pedido = [0.55, 0.45]

    simulador = MonteCarloLavarropa(semilla)
    simulador.establecer_tabla_demanda(consumo_demanda, prob_demanda)
    simulador.establecer_tabla_pedido(tamanio_pedido, prob_pedido)
    simulador.establecer_parametros_negocio(c_pedido, c_mantenimiento, c_sobrepaso, stock, inventario)
    filas_guardadas, fila_actual, fila_anterior = simulador.simular(simulacion, semana)

    print(f'Penúltima fila: {fila_anterior}')
    print(f'Última fila: {fila_actual}')
    print(f'Simulaciones: {simulacion}')


if __name__ == "__main__":
    import time
    start = time.time()
    test()
    end = time.time()
    print(f"Tiempo transcurrido: {round(end - start, 2)} segundos")


