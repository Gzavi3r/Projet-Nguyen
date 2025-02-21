#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:48:47 2024

@author: bgreffard533
"""

"""
Creation de la map:
    -Creation de la matrisse carré de taille TAILLE_MAP initialiser avec des 0,0
        chaque case a un tuple (type,appartenance) avec type = type de la case et apparetance = a qui appartient cette case:
            0 = neutre
            1 = joueur 
            2  3 = IA
    
    -Creation de patch de taille proportionelle a TAILLE_MAP avec pour valeur:
        -0 = plaine
        -1 = foret
        -2 = montagne
        -3 = lac
        -4 = village
"""
import random as rd


class CreationMap:
    
    def __init__(self, TAILLE_MAP = 16, seed = 0):
        self.TAILLE_MAP = TAILLE_MAP
        rd.seed(seed)
        self.Map = [[[0,0] for _ in range(TAILLE_MAP)] for _ in range(TAILLE_MAP)]
    
    
    def choix_point(self):
        """
        Renvoie un couple x,y qui correspond a un 0 dans Map
        """
        x = rd.randint(0, self.TAILLE_MAP-1)
        y = rd.randint(0, self.TAILLE_MAP-1)
        if self.Map[x][y][0] != 0:
            x = rd.randint(0, self.TAILLE_MAP-1)
            y = rd.randint(0, self.TAILLE_MAP-1)
        return (x,y)
            
    
    def creation_patch(self,L,x,y,taille,categorie):
        """
        Crée un patch de valeur "categorie" et de taille "taille" dans la Map a partir d'un point de coordonné (x,y)
        """
        if taille==0:
            return self.Map
        else:
            self.Map[x][y][0] = categorie
            L = self.check_dispo(L,x,y,categorie)
            if L == []:
                #raise exeption 
                print("erreur liste vide")
            indice = rd.randint(0,len(L)-1)
            x = L[indice][0]
            y = L[indice][1]           
            del L[indice]
            self.creation_patch(L,x,y,taille-1,categorie)
           
    
    def check_dispo(self,L,x,y,categorie):
        """
        Renvoie la liste des cases libre (ne depacent pas le matrice et etant de valeur 0) autour du point (x,y)
        """
        Deplacement = [(x,y-1),(x+1,y),(x,y+1),(x-1,y)]
        for lig,col in Deplacement:
            if 0<=lig<self.TAILLE_MAP and 0<=col<self.TAILLE_MAP and self.Map[lig][col][0] != categorie:
                if (lig,col) not in L:
                    L.append((lig,col))
        return L
    
    
    
    
    def ajouter_joueur(self,nb_joueur):
        angles = [(0, 0),  (self.TAILLE_MAP-1, self.TAILLE_MAP-1),(0, self.TAILLE_MAP-1), (self.TAILLE_MAP-1,0)]
        village = [(1, 1),  (self.TAILLE_MAP-2, self.TAILLE_MAP-2), (1, self.TAILLE_MAP-2), (self.TAILLE_MAP-2,1)]
        for i in range(nb_joueur):
            x, y = angles[i]        
            self.remplire_territoire(x,y,i+1)
            self.Map[village[i][0]][village[i][1]][0] = 4
        
        
    def remplire_territoire(self,x,y,type_joueur):
        tmp = x
        taille_territoire = 5

        if x == 0:
            pasx = 1
        else:
            pasx = -1
            
        if y == 0:
            pasy = 1
        else:
            pasy = -1
            
        for i in range(taille_territoire):
            x = tmp
            for j in range(taille_territoire):
                self.Map[x][y][1] = type_joueur
                x += pasx
            y += pasy
    
    def affiche_map(self):
        """
        Affiche la matrisse ligne par ligne
        """
        for l in self.Map:
            print([m for m in l])
    
    def get_map(self):
        return self.Map
            
    




def Initialisation_Map(TAILLE_MAP = 16,seed = 0, nb_joueur = 2):
    Map = CreationMap(TAILLE_MAP,seed)
    #TODO modifier les valeur si besoin
    #defition du nombre de patch en fonction de la taille de la map
    if TAILLE_MAP == 16:
        nb_foret = 5
        nb_montagne = 5
        nb_lac = 5
        
    elif TAILLE_MAP == 24:
        nb_foret = 15
        nb_montagne = 20
        nb_lac = 12
    elif TAILLE_MAP == 32:
        nb_foret = 20
        nb_montagne = 25
        nb_lac = 16
        
    #creation foret
    for i in range(nb_foret):
        taille = rd.randint(4,10)
        x,y = Map.choix_point()
        Map.creation_patch([],x,y,taille,1)
    
    #creation montagne
    for i in range(nb_montagne):
        taille = rd.randint(1,5)
        x,y = Map.choix_point()
        Map.creation_patch([],x,y,taille,2)
    
    #creation lac
    for i in range(nb_lac):
        taille = rd.randint(3,10)
        x,y = Map.choix_point()
        Map.creation_patch([],x,y,taille,3)
        
   
    Map.ajouter_joueur(nb_joueur)
    
    
    
   
    return Map.get_map()




