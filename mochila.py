import random
from deap import base, creator, tools, algorithms
import numpy
import tkinter as tk
from tkinter import ttk

# Datos de entrada
limiteMochila = 0
# (peso, valor)
elementos = []
largoIndividuos = 0


# Función de evaluación (aptitud)
def evaluar_mochila(individual):
    peso_total = 0
    valor_total = 0
    for i in range(len(individual)):
        if individual[i]:
            peso_total += elementos[i][0]
            valor_total += elementos[i][1]
    if peso_total > limiteMochila:
        return (0,)  # Si el peso total excede el límite, la aptitud es 0

    return (valor_total,)  # La aptitud es el valor total de los elementos seleccionados


# Función para generar individuos válidos inicialmente
def crearIndividuo():
    individuo = creator.Individual([random.choice([False, True]) for _ in range(largoIndividuos)])
    return individuo

def main():
    global largoIndividuos
    largoIndividuos = len(elementos)
    # Crear los tipos de individuo y aptitud
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, typecode=bool, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("individual", crearIndividuo)
    # toolbox.register("individual",
    #                  lambda: creator.Individual([random.choice([False, True]) for _ in range(largoIndividuos)]))
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=40)
    toolbox.register("evaluate", evaluar_mochila)

    # Parámetros del algoritmo genético
    tamanoPoblacion = 400
    generaciones = 100

    # Crear la población inicial
    pop = toolbox.population(n=tamanoPoblacion)

    # Configurar las estadísticas y el salón de la fama
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    # Ejecutar el algoritmo genético
    algorithms.eaSimple(pop, toolbox, cxpb=0.7, mutpb=0.2, ngen=generaciones, stats=stats, halloffame=hof)

    return pop, stats, hof

def mostrar_elementos_elegidos(individual):
    print("ELEMENTOS ELEGIDOS:")
    elementos_elegidos = [elementos[i] for i in range(len(individual)) if individual[i]]
    for elemento in elementos_elegidos:
        print("Elemento:", elemento)


# TKINTER
valor_entry = None
peso_entry = None
elementos_text = None
resultado_text = None

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    root.geometry(f"{width}x{height}+{x}+{y}")

def agregar_elemento():
    global valor_entry, peso_entry, elementos_text, elementos
    valor = int(valor_entry.get())
    peso = int(peso_entry.get())
    elementos.append((peso, valor))
    elementos_text.insert(tk.END, f"Valor: {valor} - Peso: {peso}\n")
    valor_entry.delete(0, tk.END)
    peso_entry.delete(0, tk.END)

def mostrar_resultado():
    global mejor_individuo, elementos, limiteMochila

    resultado_window = tk.Tk()
    resultado_window.title("Resultado")
    resultado_window.geometry("400x400")  # Establecer un tamaño inicial

    resultado_text = tk.Text(resultado_window, width=40, height=10, font=("Arial", 12))
    resultado_text.pack(fill=tk.BOTH, expand=True)

    resultado_text.insert(tk.END, f"Elementos: {elementos}\n")
    resultado_text.insert(tk.END, f"Limite establecido: {limiteMochila}\n")
    resultado_text.insert(tk.END, f"Mejor individuo: {mejor_individuo}\n")
    peso_total = sum(elementos[i][0] for i in range(len(mejor_individuo)) if mejor_individuo[i])
    valor_total = sum(elementos[i][1] for i in range(len(mejor_individuo)) if mejor_individuo[i])
    resultado_text.insert(tk.END, f"Peso total: {peso_total}\n")
    resultado_text.insert(tk.END, f"Valor total: {valor_total}\n")
    resultado_text.insert(tk.END, "ELEMENTOS ELEGIDOS:\n")
    elementos_elegidos = [elementos[i] for i in range(len(mejor_individuo)) if mejor_individuo[i]]
    for elemento in elementos_elegidos:
        resultado_text.insert(tk.END, f"Elemento: {elemento}\n")

    resultado_text.configure(state=tk.DISABLED)  # Deshabilitar la edición del texto

    resultado_window.mainloop()

def hecho(root, limite_entry):
    global limiteMochila
    limiteMochila = int(limite_entry.get())
    root.destroy()

def obtenerDatos():
    global valor_entry, peso_entry, elementos_text, elementos

    root = tk.Tk()
    root.title("Obtener Datos")

    center_window(root, 600, 600)

    estilo = ttk.Style()
    estilo.configure(".", font=("Helvetica", 14))

    limite_label = ttk.Label(root, text="Límite de la mochila:")
    limite_label.pack(pady=10)

    limite_entry = ttk.Entry(root, font=("Helvetica", 14))
    limite_entry.pack(pady=5)

    valor_label = ttk.Label(root, text="Valor:")
    valor_label.pack(pady=10)

    valor_entry = ttk.Entry(root, font=("Helvetica", 14))
    valor_entry.pack(pady=5)

    peso_label = ttk.Label(root, text="Peso:")
    peso_label.pack(pady=10)

    peso_entry = ttk.Entry(root, font=("Helvetica", 14))
    peso_entry.pack(pady=5)

    nuevo_elemento_button = ttk.Button(root, text="Nuevo elemento", command=agregar_elemento)
    nuevo_elemento_button.pack(pady=20)

    elementos_text = tk.Text(root, width=40, height=10, font=("Helvetica", 12))
    elementos_text.pack()

    hecho_button = ttk.Button(root, text="Hecho", command=lambda: hecho(root, limite_entry))
    hecho_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    # global limiteMochila
    obtenerDatos()
    pop, stats, hof = main()

    # Imprimir el resultado
    mejor_individuo = hof[0]
    print("Elementos:", elementos)
    print("Limite establecido:", limiteMochila)
    print("Mejor individuo:", mejor_individuo)
    print("Peso total:", sum(elementos[i][0] for i in range(len(mejor_individuo)) if mejor_individuo[i]))
    print("Valor total:", sum(elementos[i][1] for i in range(len(mejor_individuo)) if mejor_individuo[i]))
    mostrar_elementos_elegidos(mejor_individuo)
    mostrar_resultado()
