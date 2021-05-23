#########################################
# groupe MPCI 6
# Amine Karmouh
# Mohamed Krimi
# Jeremy Morcos Doueihy
# MANA Ahmed Iacob Essallami
# Ramzy Bouziane
# https://github.com/uvsq21913784/snake
#########################################
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


def create_objects():
    """Pour creer le serpent initial, le bord et le score en haut à gauche."""
    global coord_serpent, texte_score
    texte_score = canvas.create_text(60, 10, text=f"Score: {score}",
                                     fill="white", font=8)
    for x_positions, y_positions in snake_positions:
        snake = canvas.create_rectangle(x_positions - 5, y_positions - 5,
                                        x_positions + 5, y_positions + 5,
                                        fill="green")
        coord_serpent.append(snake)
    creer_pomme()
    canvas.create_rectangle(10, 30, 590, 590, outline="grey")


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


def collision_mur():
    """Si la tête du serpent dépasse les limites du bord, le jeu s'arrête et
        un bouton restart apparait."""
    global demarrage
    if (snake_positions[0][0] - 5 < 10 or snake_positions[0][1] - 5 < 30 or
       snake_positions[0][0] + 5 > 590 or snake_positions[0][1] + 5 > 590):
        demarrage = 0
        canvas.create_text(WIDTH/2, HEIGHT/2, text="Game Over", fill="red",
                           font=('Times', 20, 'bold'))
        bouton_start['text'] = "Restart"
        bouton_start['command'] = restart


def collision_serpent():
    """Si les coordonnées de la tête du serpent et ceux d'un carré du corps
        sont égaux, le jeu s'arrête et un bouton restart apparait."""
    global demarrage
    for i in range(1, len(snake_positions)):
        if snake_positions[0] == snake_positions[i]:
            demarrage = 0
            canvas.create_text(WIDTH/2, HEIGHT/2, text="Game Over", fill="red",
                               font=('Times', 20, 'bold'))
            bouton_start['text'] = "Restart"
            bouton_start['command'] = restart


def keypress(event):
    global direction
    if event.char == "q":
        direction = "Left"
    if event.char == "d":
        direction = "Right"
    if event.char == "z":
        direction = "Up"
    if event.char == "s":
        direction = "Down"


def start():
    if demarrage == 1:
        mouvement_snake()
        canvas.after(vitesse, start)
    elif demarrage == 0:
        canvas.after_cancel(start)
    if bouton_start['text'] == "Start":
        bouton_start['text'] = "Pause"
        bouton_start['command'] = pause


def pause():
    global demarrage
    demarrage = 0
    bouton_start['text'] = "Resume"
    bouton_start['command'] = resume


def resume():
    global demarrage
    demarrage = 1
    bouton_start['text'] = "Pause"
    bouton_start['command'] = pause
    start()


def restart():
    """Permet de recommencer le jeu en effacant tout sur le canvas puis en
        recreant les variables initiales."""
    global snake_positions, direction, score, coord_serpent, demarrage
    canvas.delete(ALL)
    snake_positions = [[300, 300], [290, 300], [280, 300]]
    direction = "Right"
    score = 0
    coord_serpent = []
    demarrage = 1
    create_objects()
    bouton_start['text'] = "Start"
    bouton_start['command'] = start


def quitter():
    root.destroy()


def sauvegarder():
    """Permet de sauvegarder le score dand in fichier."""
    fic = open("Records_Snake.txt", "a")
    Name = input("Write a Name to save your score: ")
    full_score = Name + ": " + str(score)
    fic.write(full_score + "\n")
    fic.close()
    print("Your score has been succesfully saved.")


def records():
    """Permet de voir tout les scores sauvegarder."""
    fic = open("Records_Snake.txt", "r")
    for ligne in fic:
        print(ligne)
    fic.close()


root = tk.Tk()
root.title("Snake")

canvas = tk.Canvas(width=WIDTH, height=HEIGHT, background="black",
                   highlightthickness=0)

bouton_start = tk.Button(root, text="Start", command=start,
                         cursor="hand2")
bouton_quitter = tk.Button(root, text="Quitter", command=quitter,
                           cursor="hand2")
bouton_sauvegarde = tk.Button(root, text="Sauvegarder", command=sauvegarder,
                              cursor="hand2")
bouton_records = tk.Button(root, text="Records", command=records,
                           cursor="hand2")

create_objects()

root.bind("<Key>", keypress)

canvas.grid(columnspan=4)
bouton_start.grid(row=1, column=0)
bouton_sauvegarde.grid(row=1, column=1)
bouton_records.grid(row=1, column=2)
bouton_quitter.grid(row=1, column=3)
root.mainloop()
