import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

TASKS_FILE = "tasks.json"

def load_tasks():
    """Charge les tâches depuis le fichier JSON."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    """Sauvegarde les tâches dans le fichier JSON."""
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def add_task():
    """Ajoute une nouvelle tâche."""
    desc = task_entry.get().strip()
    if desc:
        tasks = load_tasks()
        tasks.append({"description": desc, "done": False})
        save_tasks(tasks)
        task_entry.delete(0, tk.END)
        refresh_tasks()
    else:
        messagebox.showwarning("Erreur", "Veuillez entrer une tâche.")

def refresh_tasks():
    """Met à jour l'affichage des tâches."""
    task_list.delete(*task_list.get_children())
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        status = "✔️" if task["done"] else "❌"
        task_list.insert("", tk.END, values=(i+1, task["description"], status))

def mark_done():
    """Marque une tâche comme terminée."""
    try:
        selected_item = task_list.selection()[0]
        index = int(task_list.item(selected_item, "values")[0]) - 1
        tasks = load_tasks()
        tasks[index]["done"] = True
        save_tasks(tasks)
        refresh_tasks()
    except IndexError:
        messagebox.showwarning("Erreur", "Sélectionnez une tâche.")

def delete_task():
    """Supprime une tâche."""
    try:
        selected_item = task_list.selection()[0]
        index = int(task_list.item(selected_item, "values")[0]) - 1
        tasks = load_tasks()
        tasks.pop(index)
        save_tasks(tasks)
        refresh_tasks()
    except IndexError:
        messagebox.showwarning("Erreur", "Sélectionnez une tâche.")

# --- Interface graphique ---
root = tk.Tk()
root.title("📌 Gestionnaire de Tâches")
root.geometry("450x500")
root.configure(bg="#f4f4f4")

# Style ttk
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("Treeview", font=("Arial", 11))
style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

# Zone d'ajout de tâche
frame_top = tk.Frame(root, bg="#f4f4f4")
frame_top.pack(pady=10)

task_entry = ttk.Entry(frame_top, width=40, font=("Arial", 12))
task_entry.pack(side=tk.LEFT, padx=5)

add_button = ttk.Button(frame_top, text="➕ Ajouter", command=add_task)
add_button.pack(side=tk.LEFT)

# Liste des tâches
columns = ("#", "Tâche", "Statut")
task_list = ttk.Treeview(root, columns=columns, show="headings", height=10)
task_list.heading("#", text="#")
task_list.heading("Tâche", text="Tâche")
task_list.heading("Statut", text="Statut")
task_list.column("#", width=30, anchor="center")
task_list.column("Statut", width=80, anchor="center")
task_list.pack(pady=10)

refresh_tasks()

# Boutons d'action
frame_buttons = tk.Frame(root, bg="#f4f4f4")
frame_buttons.pack(pady=10)

done_button = ttk.Button(frame_buttons, text="✔️ Terminé", command=mark_done)
done_button.pack(side=tk.LEFT, padx=5)

delete_button = ttk.Button(frame_buttons, text="🗑️ Supprimer", command=delete_task)
delete_button.pack(side=tk.LEFT, padx=5)

# Lancer l'interface
root.mainloop()
