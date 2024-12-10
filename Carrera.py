import tkinter as tk
from random import randint
from tkinter import messagebox

# Parámetros del juego
MAX_JUGADORES = 6
META = 50

# Lista para almacenar los jugadores
jugadores = []
turno_actual = 0

# Colores asignados a los jugadores
colores = ["red", "blue", "green", "yellow", "purple", "brown"]

# Variables globales
entries_nombres = []
progress_var = []
labels = []
num_jugadores = 0

# Lista de preguntas de verdadero o falso
preguntas_vf = [
    {"pregunta": "En el principio de adición, si un evento A puede ocurrir de m maneras y un evento B puede ocurrir de n maneras, entonces el número total de maneras en que A o B pueden ocurrir es m + n", "respuesta": True},
    {"pregunta": "El principio de multiplicación establece que si un evento A puede ocurrir de m maneras y un evento B puede ocurrir de n maneras, entonces el número total de maneras en que A y B pueden ocurrir es m * n", "respuesta": True},
    {"pregunta": "Una permutación es un arreglo de elementos en el que el orden no importa", "respuesta": False},
    {"pregunta": "Las combinaciones son una forma de selección de elementos en las cuales el orden no importa", "respuesta": True},
    {"pregunta": "El número de combinaciones de n elementos tomados de r en r se denota como C(n, r) o 'n sobre r'", "respuesta": True},
    {"pregunta": "Las permutaciones de n elementos son aquellas en las que el orden de los elementos es irrelevante", "respuesta": False},
    {"pregunta": "La fórmula para calcular el número de permutaciones de n elementos tomados de r en r es P(n, r) = n! / (n-r)!", "respuesta": True},
    {"pregunta": "El principio de inclusión-exclusión se utiliza para contar elementos de manera que se evite contar de más aquellos que cumplen con más de una condición", "respuesta": True},
    {"pregunta": "En las variaciones, el orden de los elementos no tiene relevancia", "respuesta": False},
    {"pregunta": "El número de formas en que se pueden organizar n elementos distintos en un arreglo se calcula como n!", "respuesta": True}
]

# Clase Jugador
class Jugador:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color
        self.posicion = 0

    def avanzar(self, pasos):
        self.posicion += pasos

# Función para lanzar el dado
def lanzar_dado():
    return randint(1, 6)

# Función para manejar el evento en casillas múltiplos de 5
def evento_especial(jugador):
    pregunta = preguntas_vf[randint(0, len(preguntas_vf) - 1)]
    respuesta = messagebox.askquestion("Pregunta especial", pregunta["pregunta"], icon='question', type='yesno')

    if (respuesta == "yes" and pregunta["respuesta"] == True) or (respuesta == "no" and pregunta["respuesta"] == False):
        messagebox.showinfo("Respuesta correcta", f"¡Correcto, {jugador.nombre}! Puedes lanzar el dado nuevamente.")
        return True
    else:
        jugador.posicion -= 3
        if jugador.posicion < 0:
            jugador.posicion = 0
        messagebox.showinfo("Respuesta incorrecta", f"¡Incorrecto, {jugador.nombre}! Retrocederás 3 casillas.")
        return False

# Función para mostrar instrucciones
def mostrar_instrucciones():
    instrucciones = (
        "Instrucciones del Juego de Carreras:\n\n"
        "1. Cada jugador debe tirar el dado.\n"
        "2. Si responde correctamente a una pregunta, puede tirar el dado nuevamente.\n"
        "3. Si responde incorrectamente, retrocede 3 casillas.\n"
        "4. El primero en llegar a la meta gana.\n\n"
        "¡Que comience la diversión!"
    )
    messagebox.showinfo("Instrucciones", instrucciones)

# Función para manejar el turno actual de juego
def turno_juego():
    global turno_actual
    jugador = jugadores[turno_actual]
    pasos = lanzar_dado()
    dado_label.config(text=f"Número del dado: {pasos}")
    ventana.after(1000, mover_ficha, jugador, pasos, 0)

# Función para mover la ficha del jugador después de un breve retraso y de forma progresiva
def mover_ficha(jugador, pasos, paso_actual):
    if paso_actual < pasos:
        jugador.avanzar(1)
        update_positions()
        ventana.after(100, mover_ficha, jugador, pasos, paso_actual + 1)
    else:
        if jugador.posicion >= META:
            messagebox.showinfo("¡Tenemos un ganador!", f"{jugador.nombre} ha ganado la carrera!")
            ventana.quit()
            return
        if jugador.posicion % 5 == 0 and jugador.posicion < META:
            if evento_especial(jugador):
                turno_juego()
                return
        global turno_actual
        turno_actual = (turno_actual + 1) % len(jugadores)
        update_turn_label()

# Actualizar posiciones en la interfaz
def update_positions():
    for i, jugador in enumerate(jugadores):
        progress_var[i].set(jugador.posicion)
        labels[i].config(text=f"{jugador.nombre}: {jugador.posicion} casillas")

# Actualizar la etiqueta de turno con el color del jugador
def update_turn_label():
    jugador = jugadores[turno_actual]
    turno_label.config(text=f"Turno de: {jugador.nombre}", fg=jugador.color)

# Función para manejar el número de jugadores y pasar a la selección de la meta
def pedir_meta(event=None):
    global num_jugadores
    try:
        num_jugadores = int(entry_num_jugadores.get())
        if num_jugadores < 2 or num_jugadores > 6:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido de jugadores (entre 2 y 6).")
        return

    entry_num_jugadores.pack_forget()
    boton_num_jugadores.pack_forget()
    label_num_jugadores.pack_forget()

    label_meta.pack()
    entry_meta.pack()
    boton_meta.pack()

# Función para mostrar los campos de entrada para nombres
def pedir_nombres(event=None):
    try:
        global META
        META = int(entry_meta.get())
        if META <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa un número válido para la meta (un número entero positivo).")
        return

    entry_meta.pack_forget()
    boton_meta.pack_forget()
    label_meta.pack_forget()

    for i in range(num_jugadores):
        tk.Label(frame_inicial, text=f"Nombre del Jugador {i+1}:", font=("Arial", 12)).pack()
        entry_nombre = tk.Entry(frame_inicial, font=("Arial", 12))
        entry_nombre.pack()
        entries_nombres.append(entry_nombre)

    boton_iniciar = tk.Button(frame_inicial, text="Iniciar Juego", command=iniciar_juego, font=("Arial", 14))
    boton_iniciar.pack()

# Función para iniciar el juego después de ingresar nombres
def iniciar_juego():
    for i, entry in enumerate(entries_nombres):
        nombre = entry.get()
        if nombre == "":
            nombre = f"Jugador {len(jugadores)+1}"
        color = colores[i]
        jugador = Jugador(nombre, color)
        jugadores.append(jugador)

        var = tk.IntVar()
        progress_bar = tk.Scale(ventana, variable=var, from_=0, to=META, orient="horizontal", length=400, state='disabled')
        progress_bar.pack()
        progress_var.append(var)

        label = tk.Label(ventana, text=f"{nombre}: 0 casillas", font=("Arial", 12))
        label.pack()
        labels.append(label)

    frame_inicial.pack_forget()
    frame_juego.pack()
    update_positions()
    update_turn_label()

    boton_lanzar = tk.Button(frame_juego, text="Lanzar Dado", command=turno_juego, font=("Arial", 14))
    boton_lanzar.pack()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Juego de Carreras")

# Etiqueta del título del juego
titulo_label = tk.Label(ventana, text="Juego de Carreras", font=("Arial", 18, "bold"), fg="darkblue")
titulo_label.pack()

# Frame de inicio
frame_inicial = tk.Frame(ventana)
frame_inicial.pack()

label_num_jugadores = tk.Label(frame_inicial, text="Número de Jugadores (2-6):", font=("Arial", 12))
label_num_jugadores.pack()
entry_num_jugadores = tk.Entry(frame_inicial, font=("Arial", 12))
entry_num_jugadores.pack()
boton_num_jugadores = tk.Button(frame_inicial, text="Aceptar", command=pedir_meta, font=("Arial", 14))
boton_num_jugadores.pack()

# Frame del juego
frame_juego = tk.Frame(ventana)

turno_label = tk.Label(frame_juego, font=("Arial", 14))
turno_label.pack()

label_meta = tk.Label(frame_inicial, text="Ingresa la meta:", font=("Arial", 12))
entry_meta = tk.Entry(frame_inicial, font=("Arial", 12))
boton_meta = tk.Button(frame_inicial, text="Aceptar", command=pedir_nombres, font=("Arial", 14))

dado_label = tk.Label(frame_juego, font=("Arial", 14))
dado_label.pack()

# Mostrar las instrucciones después de inicializar la ventana
mostrar_instrucciones()

# Iniciar el bucle de eventos
ventana.mainloop()
