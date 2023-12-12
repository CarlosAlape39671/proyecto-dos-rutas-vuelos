import tkinter as tk
from tkinter import ttk, messagebox
import requests
from client.gui_ver_rutas import FrameViewRutes

class FrameSearchRute(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width=500, height=500)
        self.root = root
        self.pack()
        
        self.id_ruta = None
        self.rutes_form()
        self.rutes_table()
        self.state_fields('disabled')
        
    
    def rutes_form(self):
        # labels for each field
        
        # Aeropuerto A
        self.label_airport_a = tk.Label(self, text='Desde: ')
        self.label_airport_a.config(font=('Arial', 12, 'bold'))
        self.label_airport_a.grid(row=2, column=0, padx=10, pady=10)
        
        # Aeropuerto B
        self.label_airport_b = tk.Label(self, text='Hasta: ')
        self.label_airport_b.config(font=('Arial', 12, 'bold'))
        self.label_airport_b.grid(row=3, column=0, padx=10, pady=10)
        
        # text fields
        
        self.get_airports()
        
        self.airport_a = tk.StringVar()
        self.entry_airport_a = ttk.Combobox(self, values=[aeropuerto["name"] for aeropuerto in self.options_airport_a], textvariable=self.airport_a)
        self.entry_airport_a.config(width=50, font=('Arial', 12))
        self.entry_airport_a.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
        
        self.airport_b = tk.StringVar()
        self.entry_airport_b = ttk.Combobox(self, values=[aeropuerto["name"] for aeropuerto in self.options_airport_b], textvariable=self.airport_b)
        self.entry_airport_b.config(width=50, font=('Arial', 12))
        self.entry_airport_b.grid(row=3, column=1, padx=10, pady=10, columnspan=2)
        
        # Buttons
        # paleta https://paletton.com/#uid=3001c0kkWlSejzzgMrOp5fUrzan
        self.button_new = tk.Button(self, text='Nuevo', command=lambda:self.state_fields('nuevo'))
        self.button_new.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#AEA33C', cursor='hand2', activebackground='#DED269', activeforeground='#FBF6EE')
        self.button_new.grid(row=4, column=0, padx=10, pady=10)
        
        self.button_save = tk.Button(self, text='Buscar', command=self.get_rutes)
        self.button_save.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#37367A', cursor='hand2', activebackground='#57569B', activeforeground='#FBF6EE')
        self.button_save.grid(row=4, column=1, padx=10, pady=10)
        
        self.button_cancel = tk.Button(self, text='Cancelar', command=lambda:self.state_fields('cancelar'))
        self.button_cancel.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#7F1B1B', cursor='hand2', activebackground='#DE6969', activeforeground='#FBF6EE')
        self.button_cancel.grid(row=4, column=2, padx=10, pady=10)
    
    def state_fields(self, state):
        if state == 'nuevo':
            state = 'normal'
            self.id_ruta = None
        elif state == 'cancelar':
            state = 'disabled'
            self.id_ruta = None
        elif state == 'actualizar':
            state = 'normal'
            
        self.airport_a.set('')
        self.airport_b.set('')
        
        self.entry_airport_a.config(state=state)
        self.entry_airport_b.config(state=state)
        
        self.button_save.config(state=state)
        self.button_cancel.config(state=state)
    
    def rutes_table(self):
        self.table = ttk.Treeview(self, columns=('Distancia', 'Tiempo Vuelo', 'Aeropuerto A', 'Aeropuerto B'), height=10)
        self.table.grid(row=5, column=0, padx=(10, 0), pady=10, columnspan=3, sticky='nsew')
        
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.table.yview)
        self.scroll.grid(row=5, column=3, sticky='nsew')
        self.table.configure(yscrollcommand=self.scroll.set)
        
        self.table.heading('#0', text='ID')
        self.table.heading('#1', text='CAMINO')
        self.table.heading('#2', text='DISTANCIA')
        
        # obtiene los datos del api
        # self.get_rutes()
        
    
    def get_airports(self):
        try:
            response = requests.get('http://localhost:8000/aeropuertos/')
            data = response.json()
            if 'data' in data :
                self.options_airport_a = data.get('data')
                self.options_airport_b = data.get('data')
            else :
                title = 'Traer datos'
                menssage = 'Problemas al obtener los datos'
                messagebox.showwarning(title, menssage)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
            
    def get_rutes(self):
        try:
            frameSearchRute = FrameViewRutes(show_graph_view = False)
            frameSearchRute.graph_structure(weight = 'distance')
            data = frameSearchRute.shortest_route(self.airport_a.get(), self.airport_b.get())
            self.delete_rute_table()
            self.insert_rutes_table(data)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
    
    def insert_rutes_table(self, data):
        for rute in range(len(data)):
            self.table.insert('', 'end', text=rute, values=( data[rute].get('camino'), data[rute].get('longitud')))
            
    def delete_rute_table(self):
        for row_id in self.table.get_children():
            self.table.delete(row_id)