# algoritmo_prim.py
import heapq
import random


class Grafo:
    def __init__(self, numeroNodos):
        self.numeroNodos = numeroNodos
        self.listaAdyacencia = {i: [] for i in range(numeroNodos)}

    def agregarArista(self, u, v, peso):
        self.listaAdyacencia[u].append((v, peso))
        self.listaAdyacencia[v].append((u, peso))

    def generarGrafoAleatorio(self, pesoMaximo=10):
        #  conteo de conexiones de cada nodo
        conexionesPorNodo = {i: 0 for i in range(self.numeroNodos)}

        for i in range(self.numeroNodos):
            for j in range(i + 1, self.numeroNodos):
                # controlar vertices
                if conexionesPorNodo[i] < 7 and conexionesPorNodo[j] < random.randint(2, 3):
                    peso = random.randint(1, pesoMaximo)
                    self.agregarArista(i, j, peso)
                    conexionesPorNodo[i] += 1
                    conexionesPorNodo[j] += 1

    def mostrarGrafo(self):
        print("Grafo:")
        for nodo, adyacentes in self.listaAdyacencia.items():
            for vecino, peso in adyacentes:
                print(f"{nodo} --({peso})-- {vecino}")

    def calcularMSTPrim(self):
        nodoInicial = 0
        visitados = set([nodoInicial])
        minHeap = []
        aristasMST = []
        pesoTotal = 0

        # Añadir todas las aristas
        for vecino, peso in self.listaAdyacencia[nodoInicial]:
            heapq.heappush(minHeap, (peso, nodoInicial, vecino))

        # Construcción del MST
        while minHeap and len(visitados) < self.numeroNodos:
            peso, u, v = heapq.heappop(minHeap)
            if v in visitados:
                continue

            # Agregar la arista al MST
            visitados.add(v)
            aristasMST.append((u, v, peso))
            pesoTotal += peso

            # Añadir nuevas aristas al heap
            for vecino, pesoArista in self.listaAdyacencia[v]:
                if vecino not in visitados:
                    heapq.heappush(minHeap, (pesoArista, v, vecino))

        return pesoTotal, aristasMST
