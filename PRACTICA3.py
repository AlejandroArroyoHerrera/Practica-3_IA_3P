# -*- coding: utf-8 -*-
# Autor: arroy

# Importa la librería tkinter para componentes de GUI
import tkinter as tk
# Importa submódulos de tkinter para diálogos simples y mensajes emergentes
from tkinter import simpledialog, messagebox

# Importa la librería heapq para operaciones de cola de prioridad
import heapq

# Define la clase GraphApp para crear la aplicación GUI
class GraphApp:
    def __init__(self, master):
        # Inicializa la ventana principal
        self.master = master
        self.master.title("Simulador del Algoritmo de Dijkstra")

        # Crea un widget canvas para dibujar nodos y aristas
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack()

        # Inicializa diccionarios para almacenar nodos y aristas
        self.nodes = {}
        self.edges = {}
        self.selected_node = None
        self.start_node = None
        self.end_node = None

        # Asigna eventos de clic del ratón al canvas para agregar y seleccionar nodos
        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-3>", self.select_node)

        # Crea un menú para agregar aristas y calcular el camino más corto
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.menu.add_command(label="Agregar Arista", command=self.add_edge)
        self.menu.add_command(label="Calcular Camino Más Corto", command=self.calculate_shortest_path)

    def add_node(self, event):
        # Solicita al usuario ingresar un nombre para el nodo
        node_id = simpledialog.askstring("Input", "Ingrese el nombre del nodo:")
        
        # Agrega el nodo al canvas y al diccionario de nodos si es un nodo nuevo
        if node_id and node_id not in self.nodes:
            self.nodes[node_id] = (event.x, event.y)
            # Dibuja el nodo en el canvas como un círculo azul
            self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill="blue")
            # Muestra el nombre del nodo en el canvas
            self.canvas.create_text(event.x, event.y, text=node_id, fill="white")

    def select_node(self, event):
        # Encuentra el nodo más cercano a la posición del clic
        nearest_node = None
        min_distance = float("infinity")
        for node, (x, y) in self.nodes.items():
            distance = (x - event.x)**2 + (y - event.y)**2
            if distance < min_distance:
                nearest_node = node
                min_distance = distance

        # Resalta el nodo seleccionado
        if nearest_node:
            # Si ya hay un nodo seleccionado, deseleccionarlo (cambiar color a azul)
            if self.selected_node:
                self.canvas.itemconfig(self.selected_node, fill="blue")
            # Selecciona el nodo más cercano y cambia su color a rojo
            self.selected_node = self.canvas.find_closest(event.x, event.y)[0]
            self.canvas.itemconfig(self.selected_node, fill="red")

    def add_edge(self):
        # Solicita al usuario ingresar los detalles de la arista (from_node, to_node, weight)
        if self.selected_node:
            from_node = simpledialog.askstring("Input", "Ingrese el nodo de origen:")
            to_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:")
            weight = simpledialog.askinteger("Input", "Ingrese el peso de la arista:")

            # Agrega la arista al diccionario de aristas y dibújala en el canvas
            if from_node in self.nodes and to_node in self.nodes and weight:
                self.edges.setdefault(from_node, {})[to_node] = weight
                self.edges.setdefault(to_node, {})[from_node] = weight  # Asume grafo no dirigido

                # Obtiene las coordenadas de los nodos de origen y destino
                x1, y1 = self.nodes[from_node]
                x2, y2 = self.nodes[to_node]
                # Dibuja una línea entre los nodos de origen y destino
                self.canvas.create_line(x1, y1, x2, y2)
                # Muestra el peso de la arista en el canvas
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(weight), fill="black")

    def calculate_shortest_path(self):
        # Asegúrate de que haya nodos y aristas antes de calcular el camino
        if not self.nodes or not self.edges:
            messagebox.showwarning("Advertencia", "Debe agregar nodos y aristas primero.")
            return

        # Solicita al usuario ingresar los nodos de inicio y fin
        self.start_node = simpledialog.askstring("Input", "Ingrese el nodo de inicio:")
        self.end_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:")

        # Ejecuta el algoritmo de Dijkstra si se proporcionan nodos válidos
        if self.start_node in self.nodes and self.end_node in self.nodes:
            distances, path = self.dijkstra(self.edges, self.start_node)
            # Muestra el resultado del cálculo de la distancia más corta
            if self.end_node in distances:
                messagebox.showinfo("Resultado", f"Distancia más corta desde {self.start_node} a {self.end_node}: {distances[self.end_node]}")
                # Muestra el camino más corto en el canvas
                self.show_path(path, self.end_node)
            else:
                messagebox.showinfo("Resultado", "No se encontró un camino.")
        else:
            messagebox.showwarning("Advertencia", "Nodos no válidos.")

    def dijkstra(self, graph, start):
        # Inicializa la cola de prioridad y el diccionario de distancias
        queue = []
        heapq.heappush(queue, (0, start))
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        shortest_path = {}

        # Ejecuta el algoritmo de Dijkstra para encontrar el camino más corto
        while queue:
            current_distance, current_node = heapq.heappop(queue)

            # Continúa si la distancia actual es mayor a la distancia registrada
            if current_distance > distances[current_node]:
                continue

            # Recorre los vecinos del nodo actual
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                # Actualiza la distancia si se encuentra un camino más corto
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    shortest_path[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        # Retorna el diccionario de distancias y el camino más corto
        return distances, shortest_path

    def show_path(self, path, end_node):
        # Resalta el camino más corto en el canvas
        if end_node not in path:
            return

        current_node = end_node
        while current_node in path:
            next_node = path[current_node]
            x1, y1 = self.nodes[current_node]
            x2, y2 = self.nodes[next_node]
            # Dibuja una línea roja y más gruesa entre los nodos del camino más corto
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3)
            current_node = next_node

# Sección principal para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
