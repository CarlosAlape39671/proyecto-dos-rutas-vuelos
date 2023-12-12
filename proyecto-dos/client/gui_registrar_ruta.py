import tkinter as tk
from tkinter import ttk, messagebox
import requests

class FrameRegisterRute(tk.Frame):
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
        self.label_distance = tk.Label(self, text='Distancia: ')
        self.label_distance.config(font=('Arial', 12, 'bold'))
        self.label_distance.grid(row=0, column=0, padx=10, pady=10)
        
        self.label_flight_time = tk.Label(self, text='Tiempo de vuelo: ')
        self.label_flight_time.config(font=('Arial', 12, 'bold'))
        self.label_flight_time.grid(row=1, column=0, padx=10, pady=10)
        
        # Aeropuerto A
        self.label_airport_a = tk.Label(self, text='Desde: ')
        self.label_airport_a.config(font=('Arial', 12, 'bold'))
        self.label_airport_a.grid(row=2, column=0, padx=10, pady=10)
        
        # Aeropuerto B
        self.label_airport_b = tk.Label(self, text='Hasta: ')
        self.label_airport_b.config(font=('Arial', 12, 'bold'))
        self.label_airport_b.grid(row=3, column=0, padx=10, pady=10)
        
        # text fields
        self.distance = tk.StringVar()
        self.entry_distance = tk.Entry(self, textvariable=self.distance)
        self.entry_distance.config(width=50, font=('Arial', 12))
        self.entry_distance.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        
        self.flight_time = tk.StringVar()
        self.entry_flight_time = tk.Entry(self, textvariable=self.flight_time)
        self.entry_flight_time.config(width=50, font=('Arial', 12))
        self.entry_flight_time.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        
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
        
        self.button_save = tk.Button(self, text='Guardar', command=self.save_rute)
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
            
        self.distance.set('')
        self.flight_time.set('')
        self.airport_a.set('')
        self.airport_b.set('')
        
        self.entry_distance.config(state=state)
        self.entry_flight_time.config(state=state)
        self.entry_airport_a.config(state=state)
        self.entry_airport_b.config(state=state)
        
        self.button_save.config(state=state)
        self.button_cancel.config(state=state)
    
    def rutes_table(self):
        self.table = ttk.Treeview(self, columns=('Distancia', 'Tiempo Vuelo', 'Aeropuerto A', 'Aeropuerto B'), height=10)
        self.table.grid(row=5, column=0, padx=(10, 0), pady=10, columnspan=5, sticky='nsew')
        
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.table.yview)
        self.scroll.grid(row=5, column=5, sticky='nsew')
        self.table.configure(yscrollcommand=self.scroll.set)
        
        self.table.heading('#0', text='ID')
        self.table.heading('#1', text='DISTANCIA')
        self.table.heading('#2', text='TIEMPO VUELO')
        self.table.heading('#3', text='AEROPUERTO A')
        self.table.heading('#4', text='AEROPUERTO B')
        
        # obtiene los datos del api
        self.get_rutes()
        
        self.button_edit = tk.Button(self, text='Editar', command=self.update_rute_get_data)
        self.button_edit.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#AEA33C', cursor='hand2', activebackground='#DED269', activeforeground='#FBF6EE')
        self.button_edit.grid(row=6, column=0, padx=10, pady=10)
        
        self.button_delete = tk.Button(self, text='Eliminar', command=self.delete_rute)
        self.button_delete.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#7F1B1B', cursor='hand2', activebackground='#DE6969', activeforeground='#FBF6EE')
        self.button_delete.grid(row=6, column=2, padx=10, pady=10)
    
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
            response = requests.get('http://localhost:8000/rutas/')
            data = response.json()
            if 'data' in data :
                self.delete_rute_table()
                self.insert_rutes_table(data.get('data'))
            else :
                title = 'Traer datos'
                menssage = 'Problemas al obtener los datos'
                messagebox.showwarning(title, menssage)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
    
    def insert_rutes_table(self, data):
        for rute in range(len(data)):
            self.table.insert('', 'end', text=rute, values=( data[rute].get('distance'), data[rute].get('flight_time'), data[rute].get('airport_a'), data[rute].get('airport_b')))
            
    def delete_rute_table(self):
        for row_id in self.table.get_children():
            self.table.delete(row_id)
            
    def save_rute(self):
        if self.id_ruta:
            self.update_rute()
        else:
            self.create_rute()
        
    def create_rute(self):
        try:
            response = requests.post('http://localhost:8000/rutas/', json={'distance': self.distance.get(), 'flight_time': self.flight_time.get(), 'airport_a': self.airport_a.get(), 'airport_b': self.airport_b.get()})
            data = response.json()
            if 'data' in data :
                title = 'Agregar datos'
                menssage = 'Datos agregados correctamente'
                messagebox.showinfo(title, menssage)
            else :
                title = 'Agregar datos'
                menssage = 'Problemas al agregar los datos'
                messagebox.showwarning(title, menssage)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
        
        self.get_rutes()
        self.state_fields('disabled')
        self.id_ruta = None
        
    
    def update_rute_get_data(self):
        self.id_ruta = self.table.item(self.table.selection())['text']
        distance = self.table.item(self.table.selection())['values'][0]
        flight_time = self.table.item(self.table.selection())['values'][1]
        airport_a = self.table.item(self.table.selection())['values'][2]
        airport_b = self.table.item(self.table.selection())['values'][3]
        
        self.state_fields('actualizar')
        
        self.entry_distance.insert(0, distance)
        self.entry_flight_time.insert(0, flight_time)
        self.entry_airport_a.insert(0, airport_a)
        self.entry_airport_b.insert(0, airport_b)
        
            
    
    def update_rute(self):
        try:
            response = requests.put(f'http://localhost:8000/rutas/{int(self.id_ruta)}', json={'distance': self.distance.get(), 'flight_time': self.flight_time.get(), 'airport_a': self.airport_a.get(), 'airport_b': self.airport_b.get()})
            data = response.json()
            if 'data' in data :
                title = 'Actualizar datos'
                menssage = 'Datos actualizados correctamente'
                messagebox.showinfo(title, menssage)
            else :
                title = 'Actualizar datos'
                menssage = 'Problemas al actualizar los datos'
                messagebox.showwarning(title, menssage)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
        
        self.get_rutes()
        self.state_fields('disabled')
        self.id_ruta = None
    
    def delete_rute(self):
        self.id_ruta = self.table.item(self.table.selection())['text']
        try:
            response = requests.delete(f'http://localhost:8000/rutas/{int(self.id_ruta)}')
            data = response.json()
            if 'data' in data :
                title = 'Eliminar datos'
                menssage = 'Datos eliminados correctamente'
                messagebox.showinfo(title, menssage)
            else :
                title = 'Eliminar datos'
                menssage = 'Problemas al eliminar los datos'
                messagebox.showwarning(title, menssage)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
    
        self.get_rutes()
        self.state_fields('disabled')
        self.id_ruta = None