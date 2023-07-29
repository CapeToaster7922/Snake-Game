import tkinter as tk
import random

# Dimensions de la grille
GRID_WIDTH = 50
GRID_HEIGHT = 30
CELL_SIZE = 15

# Créer une grille vide
def create_empty_grid():
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Calculer la prochaine génération de la grille
def next_generation(grid):
    new_grid = create_empty_grid()

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = sum(grid[(y+i) % GRID_HEIGHT][(x+j) % GRID_WIDTH] for i in (-1, 0, 1) for j in (-1, 0, 1)) - grid[y][x]
            if grid[y][x] == 1 and neighbors in (2, 3):
                new_grid[y][x] = 1
            elif grid[y][x] == 0 and neighbors == 3:
                new_grid[y][x] = 1

    return new_grid

# Mettre à jour la grille affichée
def update_grid():
    global grid, is_running
    if is_running:
        grid = next_generation(grid)
        draw_grid()
    app.after(100, update_grid)

# Dessiner la grille sur le canvas
def draw_grid():
    canvas.delete("all")
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x+1) * CELL_SIZE, (y+1) * CELL_SIZE, fill="black")

# Gestionnaire d'événement pour poser/supprimer une cellule sur la grille
def on_canvas_click(event):
    x = event.x // CELL_SIZE
    y = event.y // CELL_SIZE
    if grid[y][x] == 1:
        grid[y][x] = 0
    else:
        grid[y][x] = 1
    draw_grid()

# Gestionnaire d'événement pour démarrer/arrêter la mise à jour de la grille
def toggle_game():
    global is_running
    is_running = not is_running
    if is_running:
        start_stop_button.config(text="Arrêter")
        update_grid()
    else:
        start_stop_button.config(text="Démarrer")

# Créer une fenêtre
app = tk.Tk()
app.title("Jeu de la vie de Conway")

# Créer une grille vide initiale
grid = create_empty_grid()

# Créer un canvas pour dessiner la grille et ajouter l'interaction souris
canvas = tk.Canvas(app, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE, bg="white")
canvas.pack()
canvas.bind("<Button-1>", on_canvas_click)

# Créer le bouton "Démarrer/Arrêter"
is_running = False
start_stop_button = tk.Button(app, text="Démarrer", command=toggle_game)
start_stop_button.pack(pady=5)

# Dessiner la grille initiale
draw_grid()

# Lancer la boucle principale de l'application
app.mainloop()