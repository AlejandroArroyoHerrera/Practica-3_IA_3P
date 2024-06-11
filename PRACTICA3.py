# -*- coding: utf-8 -*-
@author: arroy
"""
import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq

class GraphApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Simulador del Algoritmo de Dijkstra")
        self.canvas = tk.Canvas(self.master, width=800, height=600, bg="white")
        self.canvas.pack()

        self.nodes = {}
        self.edges = {}
        self.selected_node = None
        self.start_node = None
        self.end_node = None

        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-3>", self.select_node)

        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        self.menu.add_command(label="Agregar Arista", command=self.add_edge)
        self.menu.add_command(label="Calcular Camino Más Corto", command=self.calculate_shortest_path)

    def add_node(self, event):
        node_id = simpledialog.askstring("Input", "Ingrese el nombre del nodo:")
        if node_id and node_id not in self.nodes:
            self.nodes[node_id] = (event.x, event.y)
            self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill="blue")
            self.canvas.create_text(event.x, event.y, text=node_id, fill="white")

    def select_node(self, event):
        nearest_node = None
        min_distance = float("infinity")
        for node, (x, y) in self.nodes.items():
            distance = (x - event.x)**2 + (y - event.y)**2
            if distance < min_distance:
                nearest_node = node
                min_distance = distance

        if nearest_node:
            if self.selected_node:
                self.canvas.itemconfig(self.selected_node, fill="blue")
            self.selected_node = self.canvas.find_closest(event.x, event.y)[0]
            self.canvas.itemconfig(self.selected_node, fill="red")

    def add_edge(self):
        if self.selected_node:
            from_node = simpledialog.askstring("Input", "Ingrese el nodo de origen:")
            to_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:")
            weight = simpledialog.askinteger("Input", "Ingrese el peso de la arista:")

            if from_node in self.nodes and to_node in self.nodes and weight:
                self.edges.setdefault(from_node, {})[to_node] = weight
                self.edges.setdefault(to_node, {})[from_node] = weight  # Asumimos grafo no dirigido

                x1, y1 = self.nodes[from_node]
                x2, y2 = self.nodes[to_node]
                self.canvas.create_line(x1, y1, x2, y2)
                self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(weight), fill="black")

    def calculate_shortest_path(self):
        if not self.nodes or not self.edges:
            messagebox.showwarning("Advertencia", "Debe agregar nodos y aristas primero.")
            return

        self.start_node = simpledialog.askstring("Input", "Ingrese el nodo de inicio:")
        self.end_node = simpledialog.askstring("Input", "Ingrese el nodo de destino:")

        if self.start_node in self.nodes and self.end_node in self.nodes:
            distances, path = self.dijkstra(self.edges, self.start_node)
            if self.end_node in distances:
                messagebox.showinfo("Resultado", f"Distancia más corta desde {self.start_node} a {self.end_node}: {distances[self.end_node]}")
                self.show_path(path, self.end_node)
            else:
                messagebox.showinfo("Resultado", "No se encontró un camino.")
        else:
            messagebox.showwarning("Advertencia", "Nodos no válidos.")

    def dijkstra(self, graph, start):
        queue = []
        heapq.heappush(queue, (0, start))
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        shortest_path = {}

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    shortest_path[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        return distances, shortest_path

    def show_path(self, path, end_node):
        if end_node not in path:
            return

        current_node = end_node
        while current_node in path:
            next_node = path[current_node]
            x1, y1 = self.nodes[current_node]
            x2, y2 = self.nodes[next_node]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=3)
            current_node = next_node

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
