# principal.py
import sys
import time
from PyQt5.QtWidgets import QApplication
from prim import Grafo
from animacion import VisualizadorMST

def main(numeroNodos):

    grafo = Grafo(numeroNodos)
    grafo.generarGrafoAleatorio()
    conexionesIniciales = set()
    for nodo, adyacentes in grafo.listaAdyacencia.items():
        for vecino, peso in adyacentes:
            conexionesIniciales.add((min(nodo, vecino), max(nodo, vecino), peso))

    tiempoInicio = time.time()
    pesoTotal, aristasMST = grafo.calcularMSTPrim()
    tiempoFin = time.time()

    print(f"Tiempo de procesamiento para {numeroNodos} nodos: {tiempoFin - tiempoInicio:.5f} segundos")
    print(f"Peso total del MST: {pesoTotal}")
    print("Ruta del MST:", aristasMST)

    # Visualizar con PyQt5
    app = QApplication(sys.argv)
    ventana = VisualizadorMST(list(range(numeroNodos)), aristasMST, list(conexionesIniciales))
    ventana.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    numeroNodos =2000

    main(numeroNodos)
