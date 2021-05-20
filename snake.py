import tkinter as tk
import random as rd
from tkinter.constants import ALL

WIDTH = 600
HEIGHT = 600
mouvement = 10
vitesse = 60
snake_positions = [[300, 300], [290, 300], [280, 300]]
direction = "Right"
score = 0
coord_serpent = []
demarrage = 1


def creer_pomme():
    """Pour créer la pomme aléatoirement sur le canvas."""
    global food_positions, pomme
    x_pomme = rd.randint(2, 58) * mouvement
    y_pomme = rd.randint(4, 58) * mouvement
    food_positions = [x_pomme, y_pomme]
    pomme = canvas.create_rectangle(food_positions[0] - 5,
                                    food_positions[1] - 5,
                                    food_positions[0] + 5,
                                    food_positions[1] + 5,
                                    fill="red")

def mouvement_snake():
    """Pour faire bouger le serpent dans différentes directions.
        Son mouvement est réalisé en 2 étapes: effacer le serpent puis en
        créer un nouveau avec les nouvelles coordonnées."""
    global snake_positions
    head_x_position, head_y_position = snake_positions[0]
    if direction == "Left":
        new_head_position = [head_x_position - mouvement, head_y_position]
    elif direction == "Right":
        new_head_position = [head_x_position + mouvement, head_y_position]
    elif direction == "Down":
        new_head_position = [head_x_position, head_y_position + mouvement]
    elif direction == "Up":
        new_head_position = [head_x_position, head_y_position - mouvement]
    snake_positions = [new_head_position] + snake_positions[:-1]
    for i in range(len(coord_serpent)):
        canvas.delete(coord_serpent[i])
    for x_positions, y_positions in snake_positions:
        snake = canvas.create_rectangle(x_positions - 5, y_positions - 5,
                                        x_positions + 5, y_positions + 5,
                                        fill="green")
        coord_serpent.remove(coord_serpent[0])
        coord_serpent.append(snake)
    collision_pomme()
    collision_mur()
    collision_serpent()

def collision_pomme():
    """La liste des coordonnées du serpent ajoute un élément à chaque
     collision, le score augmente de 1 et une nouvelle pomme est crée."""
    global score, pomme
    if (snake_positions[0] == food_positions):
        score += 1
        canvas.itemconfig(texte_score, text=f"Score: {score}")
        snake = snake_positions.append(snake_positions[-1])
        coord_serpent.append(snake)
        canvas.delete(pomme)
        creer_pomme()    
 
