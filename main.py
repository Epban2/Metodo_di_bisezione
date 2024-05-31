# RICCARDO LA ROCCA 4C INF
# Analisi numerica, metodo di bisezione con grafica
# per il 31.5.2024

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox


def my_bisection(f, a, b, tol):
    midpoints = []
    root = 0

    def recursive_bisection(f, a, b, tol):
        m = (a + b) / 2
        midpoints.append(m)

        if np.abs(f(m)) < tol:
            return m
        elif np.sign(f(a)) == np.sign(f(m)):
            return recursive_bisection(f, m, b, tol)
        elif np.sign(f(b)) == np.sign(f(m)):
            return recursive_bisection(f, a, m, tol)

    # termine funzione ricorsiva

    # try catch per il controllo del segno, se non vi è una radice (segni concordi), imposta la root a "error" per il controllo successivo
    try:
        if np.sign(f(a)) == np.sign(f(b)):
            root = "error"
    except:
        print("Non ci sono zeri nell'intervallo")

    # se root non è error (al primo giro è 0), la calcola richiamando la ricorsione
    if root != "error":
        root = recursive_bisection(f, a, b, tol)

    return root, midpoints  # root è un valore decimale oppure una stringa con "error"


def eval_function(expr, x):
    return eval(expr)


def get_user_input():
    root = tk.Tk()
    root.withdraw()  # Nasconde la finestra principale (sarebbe una schermata bianca vuota)
    input_valido = True
    try:
        function_input = simpledialog.askstring("Inserimento funzione",
                                                "Inserisci la funzione f(x): es. x**3 - x**2 - 2*x + 1")
        a = float(simpledialog.askstring("Inserimento limite a", "Inserisci il limite inferiore a:"))
        b = float(simpledialog.askstring("Inserimento limite b", "Inserisci il limite superiore b:"))
        tol = float(simpledialog.askstring("Inserimento tolleranza", "Inserisci la tolleranza (es. 0.01):"))
        function = lambda x: eval_function(function_input, x)
    except:
        messagebox.showerror("Errore input", "Non inserire lettere in input")
        input_valido = False
        return  # se qualche input non va a buon fine (lettere in input) interrompe il l'esecuzione
    return function_input, function, a, b, tol, input_valido  # ritorno della funzione stringa e funzione (tutto a buon fine)


def check_limits(a, b):
    while a >= b:  # Controllo dei limiti, eventualmente ripete input
        a = float(simpledialog.askstring("Inserimento limite ", "limite a dev'essere minore del limite b:"))
        b = float(simpledialog.askstring("Inserimento limite ", "limite b dev'essere maggiore del limite a:"))
    return a, b


def funzione(x, f):
    return f(x)


# main
function_input, f, a, b, tol, input_valido = get_user_input()

while input_valido is False or a > b:
    if input is False:
        function_input, f, a, b, tol, input_valido = get_user_input()
    if a > b:
        a, b = check_limits(a, b)

allarme = tk.Tk()  # istanzio l'oggetto per le finestre di notifica
allarme.withdraw()

# Trova le radici usando il metodo di bisezione
root, midpoints = my_bisection(f, a, b, tol)

# Derivate
valori_di_x = np.linspace(a, b, 1000)  # array con tutti i valori assunti nell'intervallo

y = funzione(valori_di_x, f)  # y e' un array di tutti i valori che la funzione assume nell'intervallo (a,b,1000)

derivata_prima = np.gradient(y, valori_di_x)
derivata_seconda = np.gradient(derivata_prima, valori_di_x)
print(derivata_seconda)

if root == "error":  # se non viene trovato lo zero (my_bisection), la fuzione ritorna error
    messagebox.showerror("Calcolo radici", "Non c'è alcuno zero nell'intervallo sottoposto")
elif np.all(derivata_prima == 0): # derivata prima non si annulla 
    if np.all(derivata_seconda > 0) or np.all(derivata_seconda < 0):  #la derivata seconda non cambia segno
        x = np.linspace(-5, 5, 100)  # Intervallo per il grafico
        y = f(x)
        plt.switch_backend('TkAgg')

        # Traccia il grafico
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x, y, label=f'f(x) = {function_input}')
        ax.axhline(0, color='black', linewidth=1.5)  # asse x
        ax.axvline(0, color='black', linewidth=1.5)  # asse y
        ax.scatter([a, b], [0, 0], color="brown", zorder=3, label=f"Limiti dell'intervallo [{a} , {b}]")
        ax.axvline(root, color='red', linestyle=':', label=f'Radice con tol={tol} ≈ {root:.5f}')
        ax.scatter(midpoints[:-1], [f(m) for m in midpoints[:-1]], color='blue', marker='x',
                label='Punti medi')  # tutti i punti medi tranne la radice

        ax.set_title('Metodo di Bisezione')
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.legend()
        ax.grid(True)

        plt.show()
    else:
        messagebox.showerror("Derivata seconda", "Non soddisfa il secondo teorema di unicita' degli zeri")        
else:
    messagebox.showerror("Derivata prima", "La derivata prima si annulla nell'intervallo sottoposto")