from tkinter import *
import numpy as np
import random
import time
from time import sleep


def initB():
    #Initialisation du jeu
    global board
    for i in range(3):
        board[0][i] = i + 1
    r = 7
    for i in range(3):
        board[2][i] = r
        r -= 1
    board[1][2] = 4
    board[1][0] = 8

def heur(boardp):
    #fonction de calcule de l"heurestique
    h = 0
    for i in range(3):
        for j in range(3):
            if boardp[i][j] != winboard[i][j]:
                h += 1#on calcule la différence entre l'état gagnant et l'état courant
    return h

def voisins(i, j):
    #fonction qui retourne les voisins d'une case
    return [(a, b) for (a, b) in
            [(i, j + 1), (i, j - 1), (i - 1, j), (i + 1, j)]
            if a in range(3) and b in range(3)]

def GetZeroPos(boardz):
    #Fonction qui retourne la position du 0 dans le board
    for i in range(3):
        for j in range(3):
            if boardz[i][j] == 0:
                return (i, j)

def Asta():
    #Fonction A Star
    global C, D
    F = 0
    G = 0                                                           #Niveau courant
    open = []                                                       #liste des etat non parcouru
    visited = []                                                     #liste des états parcourus qui sert à la vérification
    closed = []                                                     #liste des états parcourus qui est utilisé pour le traitement
    moves = []                                                      #liste des mouvement a faire
    state = board.copy()                                            #etat initial du board
    F = heur(state) + G
    père = np.zeros((3, 3), dtype=int)                              #on initialise le père de l'état initiale a une matrice de 0 (pour éviter certain cas d'out of range)
    open.append((state, F, G, père))                                #etat, F, G, père
    #print("Calcule en cours")
    #print("Wait....")
    while len(open) > 0:
        open.sort(key=lambda tup: tup[1])           #on trie la liste en fonction de la valeur de F

        state, F, G, father = open[0]               #on prend le 1er état dans la liste puis on le retire de open
        open.remove(open[0])
        closed.append((state.copy(),father))        #on ajoute l'état a closed comme quoi il a déjà été traité
        visited.append(str(state)           )       #on ajoute l'état a visited en tant string pour faciliter la vérification
        G += 1

        if heur(state.copy()) == 0:
            break                                    #si l'heurestique de l'état courant est égale a 0 donc on est arrivé dans l'état victoire et on sort de la boucle

        dad = state.copy()                          #on sauvegarde l'état courant comme père pour les état résultats de cette état
        emptyi, emptyj = GetZeroPos(state.copy())   # on récupère la position du 0 (la case Vide) de l'état courant
        Lvoisins = voisins(emptyi, emptyj)          #on extrait la liste des voisins de la case vide

        fils = state.copy()

        for i in Lvoisins:
            x, y = i                                                                #on prend les coordoné du voisin i
            emptyi, emptyj = GetZeroPos(fils)
            fils[x][y], fils[emptyi][emptyj] = fils[emptyi][emptyj], fils[x][y]          #on inverse les valeur entre la case vide et la case a échanger

            if str(fils) in visited:
                fils[x][y], fils[emptyi][emptyj] = fils[emptyi][emptyj], fils[x][y]        #on reposition la case vide a sa position initial
                continue                                                                   #si l'état a déjà été visité on ignore le reste de l'itération

            F = heur(fils.copy()) + G
            open.append((fils.copy(),F ,G, dad))                                            #on ajoute l'état courant a open
            fils[x][y], fils[emptyi][emptyj] = fils[emptyi][emptyj], fils[x][y]            #on reposition la case vide a sa position initial

    #print("Fin des calcule")
    #print("Début de l'affichage")
    path= Path(closed)                      #on calcule le path
    cmp = len(path) - 1
    while cmp >= 0:
        draw(path[cmp])                     #affichage du pathing
        cmp -= 1
    initB()
    #print(board)

def Equal(boardi, boardf):
    #Fonction qui vérifie si 2 matrice sont égaux
    for i in range(3):
        for j in range(3):
            if boardi[i][j] != boardf[i][j]:
                return False
    return True

def InList(state, liste):
    #Fonction qui trouve le père de l'état state
    for i in range(len(liste)):
        etat, père = liste[i]               #parcours de la liste
        if Equal(state, etat):
            return père                     #si l'état interne de la boucle est égale a l'état en paramètre alors
    return np.zeros((3, 3), dtype=int)

def AllZeros(State):
    #Crée une matrie de 0
    for i in range(3):
        for j in range(3):
            if State[i][j]!= 0:
                return False
    return True

def Path(liste):
    path = []                                       #liste du chemin
    cmp = len(liste) - 1
    State, father = liste[cmp]
                # on initialise la liste avec le 1er état ainsi que son père
    path.append(State)
    path.append(father)
    cmp -= 1
    while cmp >= 0:
        State = InList(father, liste)               #Si state est valide (différent d'une matrice de 0) alors on l'ajoute au chemin sinon on arrête l'execution
        if AllZeros(State):
            break
        path.append(State)
        cmp -= 1
        father = path[len(path) - 1]
    return path

def draw(boardp):
    global items
    cnv.delete('all')                                                       #on efface le canvas
    items = [None]
    items = [None for i in range(9)]
    a, b = GetZeroPos(boardp)                                               #on récupère la position de 0
    for i in range(3):                                                      #on dessine le plateau de jeu
        for j in range(3):
            x, y = 100 * j, 100 * i
            A, B, C = (x, y), (x + 100, y + 100), (x + 50, y + 50)
            rect = cnv.create_rectangle(A, B, fill="gray")
            nro = boardp[i][j]
            txt = cnv.create_text(C, text=nro, fill="black",
                                  font=FONT)
            items[nro] = (rect, txt)
            if i == a and j == b:
                cnv.delete(rect)
                cnv.delete(txt)
    cnv.update()                    #on update le canva
    cnv.after(500)                  #on attend 0.5 secondes

def clic(event):
    global i_empty, j_empty
    i = event.y // 100
    j = event.x // 100
    nro = board[i][j]
    rect, txt = items[nro]
    if j + 1 == j_empty and i == i_empty:
        cnv.move(rect, 100, 0)
        cnv.move(txt, 100, 0)
    elif j - 1 == j_empty and i == i_empty:
        cnv.move(rect, -100, 0)
        cnv.move(txt, -100, 0)
    elif i + 1 == i_empty and j == j_empty:
        cnv.move(rect, 0, 100)
        cnv.move(txt, 0, 100)
    elif i - 1 == i_empty and j == j_empty:
        cnv.move(rect, 0, -100)
        cnv.move(txt, 0, -100)
    else:
        return
    board[i][j], board[i_empty][j_empty] = (
        board[i_empty][j_empty], board[i][j])
    i_empty = i
    j_empty = j


board = np.zeros((3, 3), dtype=int)
initB()
winboard = board.copy()
i_empty, j_empty = 1, 1

FONT = ('Helvetica', 27, 'bold')
master = Tk()
master.title('Jeu Du Taquin')
cnv = Canvas(master, width=300, height=300, bg='gray70')
cnv.pack(side='left')

btn = Button(text="    A*    ", command=Asta)
btn.pack()
# btn1 = Button(text="    aff    ", command=draw(board))
# btn1.pack()

items = [None]
items = [None for i in range(9)]
draw(board)

cnv.bind("<Button-1>", clic)
master.mainloop()