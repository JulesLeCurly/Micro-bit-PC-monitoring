import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors
import multiprocessing

def creer_fenetre_noire(monitor):
    # Fenêtre noire sur un écran donné
    root = tk.Tk()
    root.configure(bg='black')
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
    root.bind("<Key>", lambda e: root.destroy())
    root.bind("<Button-1>", lambda e: root.destroy())
    root.mainloop()

def lancer_noirs(selection, moniteurs):
    # Lance un processus par écran sélectionné
    for index in selection:
        moniteur = moniteurs[index]
        p = multiprocessing.Process(target=creer_fenetre_noire, args=(moniteur,))
        p.start()

def interface_selection():
    moniteurs = get_monitors()

    root = tk.Tk()
    root.title("Sélection des écrans à noircir")
    root.geometry("400x300")

    label = ttk.Label(root, text="Sélectionne les écrans à plonger dans le noir :")
    label.pack(pady=10)

    # Liste de cases à cocher
    selections = []
    for i, moniteur in enumerate(moniteurs):
        var = tk.IntVar()
        chk = ttk.Checkbutton(root, text=f"Écran {i+1} - {moniteur.width}x{moniteur.height}", variable=var)
        chk.pack(anchor='w', padx=20)
        selections.append(var)

    def on_valider():
        indices = [i for i, var in enumerate(selections) if var.get() == 1]
        lancer_noirs(indices, moniteurs)

    bouton = ttk.Button(root, text="Plonger dans le noir", command=on_valider)
    bouton.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Important pour Windows
    interface_selection()
