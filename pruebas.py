import tkinter as tk
from tkinter import messagebox
import random
import time


class Buscaminas:
    def __init__(self, ventana, rows, cols, nbombas, banderas):
        self.ventana = ventana
        self.rows = rows
        self.cols = cols
        self.banderas = banderas
        self.nbombas = nbombas
        self.buttons = {}
        self.bombas = set()
        self.widgets()
        self.random_bombas()
        self.contador()
    
    def widgets(self):
        self.contador()
        
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(self.ventana, text='', width=5, height=2, bg="pale green")
                button.grid(row=row, column=col)
                #button.config(command=lambda r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-1>', lambda event, r=row, c=col: self.verificar_bomba(r, c))
                button.bind('<Button-3>', lambda event, r=row, c=col: self.marcar_bomba(r, c))
                self.buttons[(row, col)] = button
                
    
    
    def random_bombas(self):
        bombas = random.sample(list(self.buttons.keys()), self.nbombas)
        for bomba in bombas:
            self.bombas.add(bomba)
        
    def verificar_bomba(self, row, col):
        if self.buttons[(row, col)]['text'] == 'B':
            return "break"
        elif (row, col) in self.bombas:
            for position, button in self.buttons.items():
                if position in self.bombas:
                    button.config(text='*', bg="tomato")
        else:
            self.buttons[(row, col)].config(text='', bg="bisque")

    def marcar_bomba(self, row, col):
        if self.buttons[(row, col)]['bg'] == "bisque":
            return "break"
        elif self.buttons[(row, col)]['text'] == 'B':
            self.buttons[(row, col)]['text'] = ''
            self.banderas = self.banderas + 1
            self.actualizar_banderas()
        elif self.banderas < 1:
            return "break"
        elif self.buttons[(row, col)]['text'] == '':
            self.buttons[(row, col)]['text'] = 'B'
            self.banderas = self.banderas - 1
            self.actualizar_banderas()
        
        return "break"
    
       
    def contador(self):
        self.s = 0
        self.m = 0
        

        self.label_tiempo = tk.Label(self.ventana, text='', width=10, height=2, bg="white", fg="black")
        self.label_tiempo.grid(row=self.rows, columnspan=2)
        self.label_banderas = tk.Label(self.ventana, text='', width=20, height=2, bg="white", fg="black")


        self.label_banderas.grid(row=self.rows, columnspan=20)
        
        self.actualizar_banderas()
        self.actualizar_tiempo()
        
        
    def actualizar_banderas(self):
        self.label_banderas.config(text=f"Banderas restantes: {self.banderas}")
    
    
    def actualizar_tiempo(self):
        self.s += 1  
        if self.s == 60:
            self.s = 0
            self.m += 1
        tiempo = f"Tiempo: {self.m:02d}:{self.s:02d}"    
        self.label_tiempo.config(text=tiempo)
        
        self.ventana.after(1000, self.actualizar_tiempo)

    

def main():
    root = tk.Tk()
    root.title("Tablero de Buscaminas")
    root.config(bg="SlateBlue2")
    def configurar_eleccion(opcion):
        #global eleccion
        eleccion = opcion
        verificar_nivel(eleccion)
    def verificar_nivel(eleccion):
        if eleccion == "facil":
            row = 10
            col = 10
            nbombas = 10
            banderas = 10 
            enviar_valores(row, col, nbombas, banderas)
        elif eleccion == "medio":
            row = 15
            col = 15
            nbombas = 15
            banderas = 15
            enviar_valores(row, col, nbombas, banderas)         
        elif eleccion == "dificil":
            row = 20
            col = 20
            nbombas = 20
            banderas = 20
            enviar_valores(row, col, nbombas, banderas)
        elif eleccion == "personalizado":
            #root.destroy()
            nueva_ventana = tk.Toplevel()
            nueva_ventana.title("Buscaminas personalizado")
            nueva_ventana.geometry("500x250")

            row1 = tk.Entry(nueva_ventana)
            row1.insert(0, "")
            row_label = tk.Label(nueva_ventana, text="Número de filas:")
            row_label.place(x="90", y="0")
            row1.pack()



            col1 = tk.Entry(nueva_ventana)
            col1.insert(0, "")
            col_label = tk.Label(nueva_ventana, text="Número de columnas:")
            col_label.place(x="60", y="20")
            col1.pack()

            nbombas1 = tk.Entry(nueva_ventana)
            nbombas1.insert(0, "")
            nbombas_label = tk.Label(nueva_ventana, text="Número de bombas:")
            nbombas_label.place(x="70", y="40")
            nbombas1.pack()

            def obtener_valores():
                nbombas = nbombas1.get()
                banderas = nbombas
                col = col1.get()
                row = row1.get()
                try:
                    col = int(col)
                    row = int(row)
                    banderas = int(banderas)
                    nbombas = int(nbombas)
                except ValueError:
                    print("¡Por favor, ingrese un número entero válido!")
                
                # Control de errores: Campo personalizado
                if col and row < 10:
                    messagebox.showwarning(title="Advertencia", message="Dimensiones mínimas: 10x10")
                    return "break"
                elif col or row or nbombas == None:
                    messagebox.showwarning(title="Advertencia", message="Complete todos los campos para jugar")
                    return "break"
                else:
                    nueva_ventana.destroy()
                    enviar_valores(row, col, nbombas, banderas)
            
            boton_confirmar = tk.Button(nueva_ventana, text="Confirmar", command=obtener_valores)
            boton_confirmar.pack()

            nueva_ventana.mainloop()
        else:
            print("Modo de juego no encontrado")



    def enviar_valores(row, col, nbombas, banderas):
        Buscaminas(root, row, col, nbombas, banderas)




    boton_facil = tk.Button(root, text="Fácil", command=lambda: configurar_eleccion("facil"))
    boton_facil.config(cursor="hand2", bg="goldenrod", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_facil.place(x="55", y="0")

    boton_mediano = tk.Button(root, text="Medio", command=lambda: configurar_eleccion("medio"))
    boton_mediano.config(cursor="hand2", bg="goldenrod", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_mediano.place(x="55", y="40")

    boton_dificil = tk.Button(root, text="Dificil", command=lambda: configurar_eleccion("dificil"))
    boton_dificil.config(cursor="hand2", bg="goldenrod", relief="flat", width=8, height=1, font=("Calisto MT", 12, "bold"))
    boton_dificil.place(x="55", y="80")
    
    boton_personalizado = tk.Button(root, text="Personalizado", command=lambda: configurar_eleccion("personalizado"))
    boton_personalizado.config(cursor="hand2", bg="goldenrod", relief="flat", width=12, height=1, font=("Calisto MT", 12, "bold"))
    boton_personalizado.place(x="35", y="120")
    
    root.mainloop()

if __name__ == "__main__":
    main()
