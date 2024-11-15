import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox
import sys
import time
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  

def obtener_grafo_adjacencia():
    center = (-12.104671062938884, -76.96161737561454)  
    road_graph = ox.graph_from_point(center, dist=1000, network_type='drive')
    
    adjacency_list = {}
    for node in road_graph.nodes(data=True):
        node_id = node[0]
        node_lat = node[1]['y']
        node_lon = node[1]['x']
        adjacency_list[node_id] = []

        for neighbor in road_graph.neighbors(node_id):
            neighbor_data = road_graph.nodes[neighbor]
            neighbor_lat = neighbor_data['y']
            neighbor_lon = neighbor_data['x']
            
            distance = haversine(node_lat, node_lon, neighbor_lat, neighbor_lon)
            
            adjacency_list[node_id].append((neighbor, distance))
    
    return road_graph, adjacency_list

def init_plot(graph):
    pos = {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)}
    fig, ax = plt.subplots(figsize=(12, 12))  # Aumentar el tamaño de la figura a 12x12 pulgadas
    nx.draw(graph, pos, ax=ax, node_color="grey", edge_color="grey", node_size=30, width=0.5, with_labels=False)
    return fig, ax, pos

def animate_bfs(graph, start_node, filename="bfs_animation.mp4"):
    fig, ax, pos = init_plot(graph)
    visited = set()
    queue = [start_node]
    edges = []
    frame_interval = 5  

    def update(frame):
        if queue:
            for _ in range(frame_interval):  
                if queue:
                    node = queue.pop(0)
                    visited.add(node)
                    nx.draw_networkx_nodes(graph, pos, nodelist=[node], node_color="blue", ax=ax, node_size=50)
                    
                    for neighbor in graph.neighbors(node):
                        if neighbor not in visited:
                            queue.append(neighbor)
                            edges.append((node, neighbor))
                            nx.draw_networkx_edges(graph, pos, edgelist=[(node, neighbor)], edge_color="red", ax=ax, width=2)

    ani = FuncAnimation(fig, update, frames=range(0, len(graph.nodes), frame_interval), repeat=False, blit=False)
    ani.save(filename, writer='ffmpeg', fps=5, bitrate=5000)  
def animate_dfs(graph, start_node, filename="dfs_animation.mp4"):
    fig, ax, pos = init_plot(graph)
    visited = set()
    stack = [start_node]
    edges = []
    frame_interval = 5  

    def update(frame):
        if stack:
            for _ in range(frame_interval): 
                if stack:
                    node = stack.pop()
                    visited.add(node)
                    nx.draw_networkx_nodes(graph, pos, nodelist=[node], node_color="blue", ax=ax, node_size=50)
                    
                    for neighbor in graph.neighbors(node):
                        if neighbor not in visited:
                            stack.append(neighbor)
                            edges.append((node, neighbor))
                            nx.draw_networkx_edges(graph, pos, edgelist=[(node, neighbor)], edge_color="red", ax=ax, width=2)

    ani = FuncAnimation(fig, update, frames=range(0, len(graph.nodes), frame_interval), repeat=False, blit=False)
    ani.save(filename, writer='ffmpeg', fps=5, bitrate=5000) 
class GraphApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Grafo de Búsqueda en Perú')
        self.layout = QtWidgets.QVBoxLayout(self)
        
        self.bfs_button = QtWidgets.QPushButton("Ejecutar BFS Animado y Guardar Video")
        self.dfs_button = QtWidgets.QPushButton("Ejecutar DFS Animado y Guardar Video")
        self.plot_button = QtWidgets.QPushButton("Mostrar Grafo")
        self.print_adj_list_button = QtWidgets.QPushButton("Imprimir Lista de Adyacencia")
        
        self.layout.addWidget(self.bfs_button)
        self.layout.addWidget(self.dfs_button)
        self.layout.addWidget(self.plot_button)
        self.layout.addWidget(self.print_adj_list_button)
        
        self.bfs_button.clicked.connect(self.run_bfs)
        self.dfs_button.clicked.connect(self.run_dfs)
        self.plot_button.clicked.connect(self.show_graph)
        self.print_adj_list_button.clicked.connect(self.print_adjacency_list)
        
        self.graph, self.adjacency_list = obtener_grafo_adjacencia()
        self.start_node = list(self.graph.nodes())[0] 

    def run_bfs(self):
        start_time = time.time()
        filename = "bfs_animation.mp4"
        animate_bfs(self.graph, self.start_node, filename)
        end_time = time.time()  
        duration = end_time - start_time
        self.show_message("BFS", filename, duration)

    def run_dfs(self):
        start_time = time.time()
        filename = "dfs_animation.mp4"
        animate_dfs(self.graph, self.start_node, filename)
        end_time = time.time() 
        duration = end_time - start_time
        self.show_message("DFS", filename, duration)

    def show_graph(self):
        ox.plot_graph(self.graph)

    def print_adjacency_list(self):
        for node, neighbors in self.adjacency_list.items():
            print(f"Nodo {node}: {[(neighbor, f'{dist:.2f} m') for neighbor, dist in neighbors]}")

    def show_message(self, algorithm, filename, duration):
        msg = QMessageBox()
        msg.setWindowTitle(f"{algorithm} - Video Guardado")
        msg.setText(f"El video {filename} ha sido guardado.\nTiempo de duración: {duration:.2f} segundos")
        msg.exec_()

    def closeEvent(self, event):
        plt.close('all') 
        event.accept()  

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GraphApp()
    window.show()
    sys.exit(app.exec_())
