import tkinter as tk
from tkinter import ttk, messagebox
import requests
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FrameViewRutes(tk.Frame):
    def __init__(self, root = None, show_graph_view = True):
        super().__init__(root, width=500, height=500)
        self.airports = {}
        self.show_graph_view = show_graph_view
        
        self.get_rutes()        
        self.get_airports()
        if self.show_graph_view:
            self.root = root
            self.pack()
            self.graph_structure()
            self.show_graph()
        
    def add_edge(self, graph, weight, node1, node2, directed=True):
        graph.add_edge(node1, node2, weight=weight)
        
        # directed graph
        if not directed:
            graph.add_edge(node2, node1, weight=weight)
    
    def graph_structure(self, weight = 'distance'):
        # labels for each field
        self.graph = nx.DiGraph()
        
        for rute in self.rutes:
            airport_a = self.airports[rute['airport_a']]['code']
            airport_b = self.airports[rute['airport_b']]['code']
            distance = rute[weight]
            self.add_edge(self.graph, distance, airport_a, airport_b)
        
        # print(self.shortest_route('MZL', 'ABA'))
        
    def show_graph(self):
        figure, ax = plt.subplots()
        pos = nx.layout.planar_layout(self.graph)
        nx.draw_networkx(self.graph, pos)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        ax.set_title('Rutas de vuelo')
        
        canvas = FigureCanvasTkAgg(figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def get_rutes(self):
        try:
            response = requests.get('http://localhost:8000/rutas/')
            data = response.json()
            if 'data' in data :
                self.rutes = data['data']
            else :
                title = 'Traer datos'
                menssage = 'Problemas al obtener los datos'
                messagebox.showwarning(title, menssage)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
    
    def get_airports(self):
        try:
            response = requests.get('http://localhost:8000/aeropuertos/')
            data = response.json()
            if 'data' in data :
                for airport in data['data']:
                    self.airports[airport['name']] = airport
                
            else :
                title = 'Traer datos'
                menssage = 'Problemas al obtener los datos'
                messagebox.showwarning(title, menssage)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
    
    def shortest_route(self, node1, node2):
        try:
            airport_a = self.airports[node1]['code']
            airport_b = self.airports[node2]['code']
            
            # Encuentra todos los caminos posibles entre los nodos
            # all_paths = list(nx.all_simple_paths(self.graph, source=node1, target=node2))
            all_paths = list(nx.all_simple_paths(self.graph, source=airport_a, target=airport_b))

            # print(graph[all_paths[0][0]][all_paths[0][1]]['weight'])
            # Calcula las longitudes de los caminos
            path_lengths = [sum(float(self.graph[path[i]][path[i + 1]]['weight']) for i in range(len(path) - 1)) for path in all_paths]

            # Combina los caminos y sus longitudes
            paths_and_lengths = list(zip(all_paths, path_lengths))

            # Ordena la lista de caminos y longitudes por longitud
            sorted_paths_and_lengths = sorted(paths_and_lengths, key=lambda x: x[1])

            # Imprime los caminos ordenados
            caminos = []
            for path, length in sorted_paths_and_lengths:
                complete_path = ""
                for element in range(len(path)) :
                    if element == len(path) - 1 :
                        complete_path += path[element]
                    else:
                        complete_path += path[element] + " -> "
                camino = {'camino': complete_path, 'longitud': str(length)}
                caminos.append(camino)
            return caminos        
        except :
            title = 'Ruta inexistente'
            menssage = 'Error al intetar obtener la ruta más corta'
            return messagebox.showerror(title, menssage)
        

    