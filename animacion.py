# animacion.py
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsEllipseItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPen, QBrush, QColor
import math
import random

class VisualizadorMST(QMainWindow):
    def __init__(self, nodos, aristas, conexionesIniciales):
        super().__init__()
        self.nodos = nodos
        self.aristas = aristas
        self.aristaActual = 0
        self.conexionesIniciales = conexionesIniciales

        # Configuración de la ventana con tamaño
        self.setWindowTitle("Visualizador de MST")
        self.setGeometry(100, 100, 1520, 950)  # Tamaño de ventana

        # Configuración de la escena
        self.escena = QGraphicsScene()
        self.escena.setBackgroundBrush(QColor(20, 20, 20))  # Fondo oscuro
        self.vista = QGraphicsView(self.escena, self)
        self.vista.setGeometry(20, 20, 1470, 900)  # Area de visualización
        self.setCentralWidget(self.vista)

        # Calcular el grado de cada nodo para la distribución
        self.gradosNodos = self.calcularGradosNodos()

        # Generar posiciones en forma de telaraña optimizada
        self.posicionesNodos = {}
        self.generarPosicionesTelarañaOptimizada()

        # Asignar posiciones aleatorias a nodos sin ubicación asignada
        self.asignarPosicionesAleatorias()

        # Dibujar nodos sin etiquetas
        self.graficosNodos = {}
        for nodo, pos in self.posicionesNodos.items():
            # Tamaño de nodo aumentado a 25x25 y color fluorescente
            circulo = QGraphicsEllipseItem(pos[0] - 12.5, pos[1] - 12.5, 25, 25)
            circulo.setBrush(QBrush(QColor(102, 255, 102)))  # Verde fluorescente
            circulo.setPen(QPen(Qt.black))
            self.escena.addItem(circulo)
            self.graficosNodos[nodo] = circulo

        # Dibujar las conexiones iniciales en blanco y almacenar las líneas en un diccionario
        self.lineasIniciales = {}
        for u, v, peso in self.conexionesIniciales:
            posU = self.posicionesNodos[u]
            posV = self.posicionesNodos[v]
            lineaInicial = self.crearLineaDesdeBorde(posU, posV)
            lineaInicial.setPen(QPen(QColor(255, 255, 255), 1))  # Blanco para conexiones iniciales
            self.escena.addItem(lineaInicial)
            # Guardar la referencia de la línea usando el par (u, v) ordenado
            self.lineasIniciales[(min(u, v), max(u, v))] = lineaInicial

        # Temporizador para la animación del MST
        self.temporizador = QTimer()
        self.temporizador.timeout.connect(self.dibujarSiguienteArista)
        self.temporizador.start(300)  # Ajuste del tiempo para una animación más suave

    def calcularGradosNodos(self):
        grados = {nodo: 0 for nodo in self.nodos}
        for u, v, _ in self.conexionesIniciales:
            grados[u] += 1
            grados[v] += 1
        return grados

    def generarPosicionesTelarañaOptimizada(self):
        centroX, centroY = 760, 475  # Centro dventana
        radioInicial = 100  # Radio del primer círculo
        nodosPorNivelInicial = 8  # Número en el primer nivel
        nivelesMaximos = 5
        incrementoRadio = (425 - radioInicial) / nivelesMaximos  # Ajuste dinámico  de radio

        # Ordenar nodos por grado (de mayor a menor) y distribuir en niveles
        nodosOrdenados = sorted(self.gradosNodos.keys(), key=lambda x: -self.gradosNodos[x])

        nivelActual = 0
        i = 0
        nodosRestantes = len(nodosOrdenados)

        while i < nodosRestantes and nivelActual < nivelesMaximos:
            # Ajustar el número de nodos por nivel según el nivel actual y la cantidad restante
            nodosPorNivel = min(nodosPorNivelInicial + (nivelActual * 4), nodosRestantes - i)
            radio = radioInicial + nivelActual * incrementoRadio

            for j in range(nodosPorNivel):
                ángulo = (2 * math.pi / nodosPorNivel) * j
                x = centroX + int(radio * math.cos(ángulo))
                y = centroY + int(radio * math.sin(ángulo))
                self.posicionesNodos[nodosOrdenados[i]] = (x, y)
                i += 1

            nivelActual += 1  # Pasar al siguiente nivel

    def asignarPosicionesAleatorias(self):
        # Asignar posiciones aleatorias a cualquier nodo faltante
        nodosFaltantes = set(self.nodos) - set(self.posicionesNodos.keys())
        for nodo in nodosFaltantes:
            x = random.randint(50, 1470)  # Limites  de la ventana
            y = random.randint(50, 900)   # Limites  de la ventana
            self.posicionesNodos[nodo] = (x, y)

    def crearLineaDesdeBorde(self, posU, posV):
        # Radio del nodo
        radioNodo = 12.5  #  tamaño del nodo

        # Calcular el ángulo entre los dos nodos
        deltaX = posV[0] - posU[0]
        deltaY = posV[1] - posU[1]
        distancia = math.sqrt(deltaX ** 2 + deltaY ** 2)
        if distancia == 0:
            return QGraphicsLineItem(posU[0], posU[1], posV[0], posV[1])

        # Calcular desplazamiento
        offsetX = (deltaX / distancia) * radioNodo
        offsetY = (deltaY / distancia) * radioNodo

        # Crear línea desde el borde de los círculos de los nodos
        x1 = posU[0] + offsetX
        y1 = posU[1] + offsetY
        x2 = posV[0] - offsetX
        y2 = posV[1] - offsetY

        return QGraphicsLineItem(x1, y1, x2, y2)

    def dibujarSiguienteArista(self):
        if self.aristaActual < len(self.aristas):
            u, v, peso = self.aristas[self.aristaActual]
            linea = self.lineasIniciales[(min(u, v), max(u, v))]
            # Cambiar el color de la arista en el MST de blanco a magenta
            linea.setPen(QPen(QColor(255, 20, 147), 2))  # Magenta

            # Cambiar el color
            colorVisitado = QColor(0, 255, 255)  # Azul
            self.graficosNodos[u].setBrush(QBrush(colorVisitado))
            self.graficosNodos[v].setBrush(QBrush(colorVisitado))

            self.aristaActual += 1
        else:
            self.temporizador.stop()
            print("Animación completada")
