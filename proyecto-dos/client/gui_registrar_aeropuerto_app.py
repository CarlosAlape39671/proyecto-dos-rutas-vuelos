import tkinter as tk
from tkinter import ttk, messagebox
import requests

class FrameRegisterAirport(tk.Frame):
    def __init__(self, root = None):
        super().__init__(root, width=500, height=500)
        self.root = root
        self.pack()
        
        self.id_aeropuerto = None
        self.airports_form()
        self.airports_table()
        self.state_fields('disabled')
        
    
    def airports_form(self):
        # labels for each field
        self.label_airport_name = tk.Label(self, text='Nombre: ')
        self.label_airport_name.config(font=('Arial', 12, 'bold'))
        self.label_airport_name.grid(row=0, column=0, padx=10, pady=10)
        
        self.label_airport_location = tk.Label(self, text='Ubicación: ')
        self.label_airport_location.config(font=('Arial', 12, 'bold'))
        self.label_airport_location.grid(row=1, column=0, padx=10, pady=10)
        
        self.label_airport_code = tk.Label(self, text='Código: ')
        self.label_airport_code.config(font=('Arial', 12, 'bold'))
        self.label_airport_code.grid(row=2, column=0, padx=10, pady=10)
        
        # text fields
        self.airport_name = tk.StringVar()
        self.entry_airport_name = tk.Entry(self, textvariable=self.airport_name)
        self.entry_airport_name.config(width=50, font=('Arial', 12))
        self.entry_airport_name.grid(row=0, column=1, padx=10, pady=10, columnspan=2)
        
        self.airport_location = tk.StringVar()
        self.entry_airport_location = tk.Entry(self, textvariable=self.airport_location)
        self.entry_airport_location.config(width=50, font=('Arial', 12))
        self.entry_airport_location.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
        
        self.airport_code = tk.StringVar()
        self.entry_airport_code = tk.Entry(self, textvariable=self.airport_code)
        self.entry_airport_code.config(width=50, font=('Arial', 12))
        self.entry_airport_code.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
        
        # Buttons
        # paleta https://paletton.com/#uid=3001c0kkWlSejzzgMrOp5fUrzan
        self.button_new = tk.Button(self, text='Nuevo', command=lambda:self.state_fields('nuevo'))
        self.button_new.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#AEA33C', cursor='hand2', activebackground='#DED269', activeforeground='#FBF6EE')
        self.button_new.grid(row=3, column=0, padx=10, pady=10)
        
        self.button_save = tk.Button(self, text='Guardar', command=self.save_airport)
        self.button_save.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#37367A', cursor='hand2', activebackground='#57569B', activeforeground='#FBF6EE')
        self.button_save.grid(row=3, column=1, padx=10, pady=10)
        
        self.button_cancel = tk.Button(self, text='Cancelar', command=lambda:self.state_fields('cancelar'))
        self.button_cancel.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#7F1B1B', cursor='hand2', activebackground='#DE6969', activeforeground='#FBF6EE')
        self.button_cancel.grid(row=3, column=2, padx=10, pady=10)
    
    def state_fields(self, state):
        if state == 'nuevo':
            state = 'normal'
            self.id_aeropuerto = None
        elif state == 'cancelar':
            state = 'disabled'
            self.id_aeropuerto = None
        elif state == 'actualizar':
            state = 'normal'
            
        self.airport_name.set('')
        self.airport_location.set('')
        self.airport_code.set('')
        
        self.entry_airport_name.config(state=state)
        self.entry_airport_location.config(state=state)
        self.entry_airport_code.config(state=state)
        
        self.button_save.config(state=state)
        self.button_cancel.config(state=state)
    
    def airports_table(self):
        self.table = ttk.Treeview(self, columns=('Nombre', 'Ubicacion', 'Codigo'), height=10)
        self.table.grid(row=4, column=0, padx=(10, 0), pady=10, columnspan=4, sticky='nsew')
        
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.table.yview)
        self.scroll.grid(row=4, column=4, sticky='nsew')
        self.table.configure(yscrollcommand=self.scroll.set)
        
        self.table.heading('#0', text='ID')
        self.table.heading('#1', text='NOMBRE')
        self.table.heading('#2', text='UBICACIÓN')
        self.table.heading('#3', text='CÓDIGO')
        
        # obtiene los datos del api
        self.get_airports()
        
        self.button_edit = tk.Button(self, text='Editar', command=self.update_airport_get_data)
        self.button_edit.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#AEA33C', cursor='hand2', activebackground='#DED269', activeforeground='#FBF6EE')
        self.button_edit.grid(row=5, column=0, padx=10, pady=10)
        
        self.button_delete = tk.Button(self, text='Eliminar', command=self.delete_airport)
        self.button_delete.config(width=20, font=('Arial', 12, 'bold'), fg='#FBF6EE', bg='#7F1B1B', cursor='hand2', activebackground='#DE6969', activeforeground='#FBF6EE')
        self.button_delete.grid(row=5, column=2, padx=10, pady=10)
    
    def get_airports(self):
        try:
            response = requests.get('http://localhost:8000/aeropuertos/')
            data = response.json()
            if 'data' in data :
                self.delete_airport_table()
                self.insert_airports_table(data.get('data'))
            else :
                title = 'Traer datos'
                menssage = 'Problemas al obtener los datos'
                messagebox.showwarning(title, menssage)
        except:
            title = 'Error en la petición'
            menssage = 'Problemas en la petición'
            messagebox.showerror(title, menssage)
    
    def insert_airports_table(self, data):
        for airport in range(len(data)):
            self.table.insert('', 'end', text=airport, values=( data[airport].get('name'), data[airport].get('location'), data[airport].get('code')))
            
    def delete_airport_table(self):
        for row_id in self.table.get_children():
            self.table.delete(row_id)
            
    def save_airport(self):
        if self.id_aeropuerto:
            self.update_airport()
        else:
            self.create_airport()
        
    def create_airport(self):
        try:
            response = requests.post('http://localhost:8000/aeropuertos/', json={'name': self.airport_name.get(), 'location': self.airport_location.get(), 'code': self.airport_code.get()})
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
        
        self.get_airports()
        self.state_fields('disabled')
        self.id_aeropuerto = None
    
    def update_airport_get_data(self):
        self.id_aeropuerto = self.table.item(self.table.selection())['text']
        airport_name = self.table.item(self.table.selection())['values'][0]
        airport_location = self.table.item(self.table.selection())['values'][1]
        airport_code = self.table.item(self.table.selection())['values'][2]
        
        self.state_fields('actualizar')
        
        self.entry_airport_name.insert(0, airport_name)
        self.entry_airport_location.insert(0, airport_location)
        self.entry_airport_code.insert(0, airport_code)
            
    
    def update_airport(self):
        try:
            response = requests.put(f'http://localhost:8000/aeropuertos/{int(self.id_aeropuerto)}', json={'name': self.airport_name.get(), 'location': self.airport_location.get(), 'code': self.airport_code.get()})
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
        
        self.get_airports()
        self.state_fields('disabled')
        self.id_aeropuerto = None
    
    def delete_airport(self):
        self.id_aeropuerto = self.table.item(self.table.selection())['text']
        try:
            response = requests.delete(f'http://localhost:8000/aeropuertos/{int(self.id_aeropuerto)}')
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
    
        self.get_airports()
        self.state_fields('disabled')
        self.id_aeropuerto = None