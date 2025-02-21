# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 21:55:31 2024

@author: Brice
"""

import tkinter as tk
from PIL import Image, ImageTk
import random as rd
import WidgetCustom

#utiliser pour faire les tooltip des boutons
from idlelib.tooltip import Hovertip

class Initialisation_Guerre:
    """
    Pour faire la gerre on a 3 type d'unité:
        les fantassin sont de tier 0 , les plus faibles
        les soldat sont sont de tier 1 ,intermediaire 
        les chevaliers sont sont de tier 2 ,les plus fort
    
    Pour obtenir les unités:
        -les fantassin sont des villageois, ils sont recrutablent dans vos villages(ou caserne) mais vous perder un villageois
        -les soldat sont:
            soit des fantassins ameliorés dans une caserne(prent 1 tour)
            soit ils sont acheter directemnt comme les fantassin (moins rentable que de former un fantassin)
        -les chevaliers sont le Joueur et ses vassaux
        
    Deroulement d'une guerre :
        chaque unité a: 
            50% chance de gagner contre une unité du meme tier , 
            25% chance de gagner contre une unité du tier directement supperieur (tier 0 vs tier 1,tier 1 vs tier 2), 
            5% de chance de gagner contre une unité 2 tier supperieur (tier 0 vs tier 2)
            
        attaque(un joueur attaque qlq/ l'attaquant est a gauche):
            -on choisit la quantité d'unité que l'ont veux envoyer
            -on paie le cout de la guerre
            -chaque unité se bat, l'unité gagnante reste pour combattre la prochaine unité ennemie
            -Le premier qui n'a plus d'unité perd
            
        defense(un joueur se fait attaquer/ le defenseur est a droite):
            on se defend avec toutes nos unitées 
            
    Apres la guerre:
        -Si l'attaquant gagne il remporte ce pour quoi il a attaqué
        -Si l'attaquant perd les deux camps on des blésser et des mort, l'attaquant ne gagne rien , le defenseur gagne une partie de ce que l'attaquant avait payer pour faire la guerre'
        -Les unités qui n'ont pas combatue n'on rien
        -une partie des unités qui ont combatue et perdu sont blésser et reviennent au prochain tour , l'autre partie meurt et dissparait
        
            
    """
    def __init__(self, root, seed, Menu, canvas_map, canvas_menu,barre_menu, dico_village, dico_joueurs,images_tk,custom_font):
        
        """
        Tout les dico et les info necessaire au methode 
        """
        self.root = root
        rd.seed(seed)
        self.Menu = Menu
        self.canvas_map = canvas_map
        self.canvas_menu = canvas_menu
        self.barre_menu = barre_menu
        self.dico_village = dico_village
        self.dico_joueurs = dico_joueurs
        self.images_tk = images_tk
        self.custom_font = custom_font
        
        self.gif_en_cours = False
        self.guerre_en_cours = False
        self.resultat_guerre = False #la variable qui va servir a communiquer les resultat avec le Menu
        
        self.dico_tier_unit = {
            0: "fantassin",
            1: "soldat",
            2: "chavalier",
            }
        
        self.dico_gif = {
            "001": "Images/guerre/fvf.gif",
            "002": "Images/guerre/fvf_i.gif",
            "011": "Images/guerre/fvk.gif",
            "012": "Images/guerre/fvk_i.gif",
            "021": "Images/guerre/fvc.gif",
            "022": "Images/guerre/fvc_i.gif",
            "101": "Images/guerre/kvf.gif",
            "102": "Images/guerre/kvf_i.gif",
            "111": "Images/guerre/kvk.gif",
            "112": "Images/guerre/kvk_i.gif",
            "121": "Images/guerre/kvc.gif",
            "122": "Images/guerre/kvc_i.gif",
            "201": "Images/guerre/cvf.gif",
            "202": "Images/guerre/cvf_i.gif",
            "211": "Images/guerre/cvk.gif",
            "212": "Images/guerre/cvk_i.gif",
            "221": "Images/guerre/cvc.gif",
            "222": "Images/guerre/cvc_i.gif"
        }

        
        #TODO exemple
        #self.simuler_guerre("Joueur",[5,0,5],"Ennemi 1",[5,0,5],10)
        #self.selection_type_guerre("Joueur","Ennemi 1")

        
    
    def selection_type_guerre(self,joueur1,joueur2,list_unite = None):
        """
        Permet de lancer la bonne methode en fonction du type de joueur:
            Joueur vs IA
            IA vs IA
            IA vs Joueur
            Revolte (les revoltes sont quand les villageois sont de mauvaise humeur)
        """
        self.resultat_guerre = False
        if joueur1 == "Joueur": #Joueur vs IA ou revolte 
            if type(joueur2) != str: #revolte
                self.fenetre_selection_revolte(joueur1,joueur2,list_unite)
            else: #guerre
                self.fenetre_selection_armee(joueur1,joueur2)
            
        
        elif joueur1[0:6] == "Ennemi": #Revolte contre IA
            #L'IA se defend toujours avec toutes ces unités
            joueur1_class = self.dico_joueurs[joueur1]
            list_unite_joueur1 = [joueur1_class.get_fantassin(),joueur1_class.get_soldat(),joueur1_class.get_chevalier()] 
            self.simuler_revolte(joueur1,list_unite_joueur1,joueur2, list_unite)
            

        return self.resultat_guerre

    
    def fenetre_selection_armee(self,joueur1_nom: str, joueur2_nom: str):
        """
        Prend le nom de deux joueur
        Ouvre une nouvelle fenetre pour le Joueur:
            dans cette fenetre il peut choisir combient d'unité il envoie a la guerre 
            il y'aura aussi un une partie de la fenetre dediée au rapport des unitées adverse
            apres avoir fait ses choix il aura deux Bouttons :
                -Guerre rapide: change la fenetre et affiche juste le reslultatat de la guerre
                -Guerre annimé: une petite animation avec des gif pour voir la guerre en "temps réel" 
        """
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Gestion de la Guerre")
        fenetre.geometry("800x600")  # Taille de la fenêtre
        fenetre.resizable(False, False)
        fenetre.grab_set()

        # Label en haut
        label_selection = tk.Label(fenetre, text="Sélection des unités", font = self.custom_font)
        label_selection.pack(pady=10)
        
        self.custom_font.config(size=15)

        # Cadre principal pour les deux frames
        main_frame = tk.Frame(fenetre)
        main_frame.pack(fill="both", expand=True)

        # Frame gauche
        frame1 = tk.Frame(main_frame, bg="lightgrey", width=370, height=350,relief="sunken", bd=2)
        frame1.pack(side="left", fill="both", expand=True,padx=1) 
        frame1.grid_propagate(False)
        label = tk.Label(frame1, text="Vos unités", bg="lightgrey", width=15,font = self.custom_font)
        label.grid(row=0, column=0)

        # Frame droite
        frame2 = tk.Frame(main_frame, bg="lightblue", width=230, height=350,relief="sunken", bd=2)
        frame2.pack(side="right", fill="both", expand=True,padx=1) 
        frame2.grid_propagate(False)
        label = tk.Label(frame2, text="Unités Ennemi", bg="lightblue", width=15,font = self.custom_font)
        label.grid(row=0, column=1)

        

        #TODO 
        joueur1_class = self.dico_joueurs[joueur1_nom]
        
        nb_chevalier = joueur1_class.get_chevalier()
        list_vassal = list(joueur1_class.get_vassal().values())
        for vassal in list_vassal:
            nb_chevalier += vassal.get_chevalier()
            
        unite_joueur = (joueur1_class.get_fantassin(),joueur1_class.get_soldat(),nb_chevalier)
        argent_joueur1 = joueur1_class.get_argent()
        ressource_joueur1 = joueur1_class.get_ressource()
        
        self.cout_argent = 30
        self.cout_ressource = 30

        def update_cout():
            # Calcul du coût total

            cout_argent_chevalier = int(spinbox_chevalier.get()) *20 
            cout_argent_soldat = int(spinbox_soldat.get()) * 10
            cout_argent_fantassin = int(spinbox_fantassin.get()) * 5
            self.cout_argent = cout_argent_chevalier + cout_argent_soldat + cout_argent_fantassin +30
            cout_ressource_chevalier = int(spinbox_chevalier.get()) *20 
            cout_ressource_soldat = int(spinbox_soldat.get()) * 10
            cout_ressource_fantassin = int(spinbox_fantassin.get()) * 5
            self.cout_ressource = cout_ressource_chevalier + cout_ressource_soldat + cout_ressource_fantassin +30
            
            
            # Mise à jour du texte du label
            label_cout.config(text=f"Coût de la guerre :{self.cout_argent} argents, {self.cout_ressource} ressources")
            if self.cout_argent>argent_joueur1 or self.cout_ressource>ressource_joueur1 or spinbox_chevalier.get() == 0 and spinbox_soldat.get() == 0 and spinbox_fantassin.get() == 0:
                button_rapide.config(state=tk.DISABLED)
                button_animer.config(state=tk.DISABLED)
            else:
                button_rapide.config(state=tk.NORMAL)
                button_animer.config(state=tk.NORMAL)

                
        # Ajout des éléments dans la frame gauche
        # Chargement de l'image (utilisez un chemin d'image valide)
        img_fantassin = self.images_tk["fantassin"]
        image_label = tk.Label(frame1, image=img_fantassin, bg="lightgrey")
        image_label.grid(row=1, column=0,sticky="w")

        # Label sous l'image
        text_label = tk.Label(frame1, text="Fantassin(Cout :5/5)", bg="lightgrey", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=2, column=0,sticky="w")

        # Spinbox à droite de l'image
        spinbox_fantassin = WidgetCustom.Spinbox_Custom(frame1, from_=0, to=unite_joueur[0], width=5,font = self.custom_font,command=update_cout)
        spinbox_fantassin.grid(row=1, column=1,sticky="w")
        
        text_label = tk.Label(frame1, text=f"/ {unite_joueur[0]} ", bg="lightgrey", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=1, column=2,sticky="w")
        
        img_soldat = self.images_tk["soldat"]
        image_label = tk.Label(frame1, image=img_soldat, bg="lightgrey")
        image_label.grid(row=4, column=0,sticky="w")


        # Label sous l'image
        text_label = tk.Label(frame1, text="Soldat(Cout :10/10)", bg="lightgrey", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=5, column=0,sticky="w")

        # Spinbox à droite de l'image
        spinbox_soldat = WidgetCustom.Spinbox_Custom(frame1, from_=0, to=unite_joueur[1], width=5,font = self.custom_font,command=update_cout)
        spinbox_soldat.grid(row=4, column=1,sticky="w")
        
        text_label = tk.Label(frame1, text=f"/ {unite_joueur[1]} ", bg="lightgrey", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=4, column=2,sticky="w")
        
        img_chevalier = self.images_tk["chevalier"]
        image_label = tk.Label(frame1, image=img_chevalier, bg="lightgrey")
        image_label.grid(row=7, column=0,sticky="w")


        # Label sous l'image
        text_label = tk.Label(frame1, text="Chevalier(Cout :20/20)", bg="lightgrey", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=8, column=0,sticky="w")

        # Spinbox à droite de l'image
        spinbox_chevalier = WidgetCustom.Spinbox_Custom(frame1, from_=0, to=unite_joueur[2], width=5,font = self.custom_font,command=update_cout)
        spinbox_chevalier.grid(row=7, column=1,sticky="w")
        
        text_label = tk.Label(frame1, text=f"/ {unite_joueur[2]} ", bg="lightgrey", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=7, column=2,sticky="w")

        #-------------Frame2-------------------------------
        joueur2_class = self.dico_joueurs[joueur2_nom]
        #le tuple (fantassin, soldat, chevalier)
        unite_ennemi = (joueur2_class.get_fantassin(),joueur2_class.get_soldat(),joueur2_class.get_chevalier())
        
        img_fantassin_mirroir = self.images_tk["fantassin_m"]


        image_label2 = tk.Label(frame2, image=img_fantassin_mirroir, bg="lightblue")
        image_label2.grid(row=1, column=1, sticky="e")


        text_label2 = tk.Label(frame2, text="Fantassin", bg="lightblue", anchor="e", width=10,font = self.custom_font)
        text_label2.grid(row=2, column=1, sticky="e")

        text_label2 = tk.Label(frame2, text=f"{unite_ennemi[0]}", bg="lightblue", anchor="e", width=10,font = self.custom_font)
        text_label2.grid(row=1, column=0, sticky="e")

        img_soldat_mirroir = self.images_tk["soldat_m"]

        image_label2 = tk.Label(frame2, image=img_soldat_mirroir, bg="lightblue")
        image_label2.grid(row=3, column=1, sticky="e")


        text_label2 = tk.Label(frame2, text="Soldat", bg="lightblue", anchor="e", width=10,font = self.custom_font)
        text_label2.grid(row=4, column=1, sticky="e")

        text_label2 = tk.Label(frame2, text=f"{unite_ennemi[1]}", bg="lightblue", anchor="e", width=10,font = self.custom_font)
        text_label2.grid(row=3, column=0, sticky="e")
        
        img_chevalier_mirroir = self.images_tk["chevalier_m"]

        image_label2 = tk.Label(frame2, image=img_chevalier_mirroir, bg="lightblue")
        image_label2.grid(row=5, column=1, sticky="e")


        text_label2 = tk.Label(frame2, text="Chevalier", bg="lightblue", anchor="e", width=10,font = self.custom_font)
        text_label2.grid(row=6, column=1, sticky="e")

        text_label2 = tk.Label(frame2, text=f"{unite_ennemi[2]}", bg="lightblue", anchor="e", width=10,font = self.custom_font)
        text_label2.grid(row=5, column=0, sticky="e")

        label_cout = tk.Label(fenetre, text=f"Coût de la guerre : {self.cout_argent} argent {self.cout_ressource} ressource", font = self.custom_font)
        label_cout.pack(pady=10)



        # Cadre pour les boutons
        button_frame = tk.Frame(fenetre)
        button_frame.pack(pady=10)
        
        def get_unite_joueur1():
            """recupere les valeurs des spinbox custom et les renvoie sous forme de list"""
            return [spinbox_fantassin.get(),spinbox_soldat.get(),spinbox_chevalier.get()]
        
        
        button_rapide = tk.Button(
            button_frame, text="Guerre rapide", width=15,state=tk.DISABLED,
            command=lambda : self.fenetre_fin_guerre(fenetre,joueur1_nom,get_unite_joueur1(),joueur2_nom,list(unite_ennemi),self.cout_argent,self.cout_ressource)
            )
        button_rapide.pack(side="left", padx=5)
        Hovertip(button_rapide, "Vous permet de voire directement le résutltat de la guerre.")


        button_animer = tk.Button(
            button_frame, text="Guerre animée", width=15, state=tk.DISABLED,
            command=lambda : self.fenetre_guerre_anime(fenetre,joueur1_nom,get_unite_joueur1(),joueur2_nom,list(unite_ennemi),self.cout_argent,self.cout_ressource)
            )
        button_animer.pack(side="left", padx=5)
        Hovertip(button_animer, "Vous permet de voire la guerre en temps réel.\nAttention : Peut être long si beaucoup (>30) d'unitées sont utilisées")


        button_annuler = tk.Button(button_frame, text="Annuler", width=15,command=fenetre.destroy)
        button_annuler.pack(side="left", padx=5)
        self.root.wait_window(fenetre)
        
    def fenetre_selection_revolte(self,joueur1_nom, village, dico_revolte):
        """
        Prend le nom d'un joueur et une instance de Village et un dico avec des indice et des instances de Roturier
        Ouvre une nouvelle fenetre pour le Joueur:
            dans cette fenetre il peut choisir combient d'unité il envoie pour gerer la revolte
            il y'aura aussi un une partie de la fenetre dediée au rapport des unitées adverse
            apres avoir fait ses choix il aura deux Bouttons :
                -Mater la revolte: change la fenetre et affiche juste le reslultat de la revolte
                -Laisser faire: Le village est detruit
        """
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Révolte")
        fenetre.geometry("800x600")  # Taille de la fenêtre
        fenetre.resizable(False, False)
        fenetre.grab_set()

        # Label en haut
        label_selection = tk.Label(fenetre, text=f"Révolte à {village.get_nom()}\nSélection des unités pour defendre le village", font = self.custom_font)
        label_selection.pack(pady=10)

        # Cadre principal pour les deux frames
        main_frame = tk.Frame(fenetre)
        main_frame.pack(fill="both", expand=True)

        # Frame gauche
        frame1 = tk.Frame(main_frame, bg="lightgrey", width=230, height=350,relief="sunken", bd=2)
        frame1.pack(side="left", fill="both", expand=True,padx=1) 
        frame1.grid_propagate(False)
        label = tk.Label(frame1, text="Villageois révoltés", bg="lightgrey", width=15,font = self.custom_font)
        label.grid(row=0, column=0)

        # Frame droite
        frame2 = tk.Frame(main_frame, bg="lightblue", width=370, height=350,relief="sunken", bd=2)
        frame2.pack(side="right", fill="both", expand=True,padx=1) 
        frame2.grid_propagate(False)
        label = tk.Label(frame2, text="Vos unité", bg="lightblue", width=15,font = self.custom_font)
        label.grid(row=0, column=1)

        
        #----Frame gauche----------------------------
        nb_fantassin = len(dico_revolte)
        
        img_fantassin = self.images_tk["fantassin"]


        image_label2 = tk.Label(frame1, image=img_fantassin, bg="lightgrey")
        image_label2.grid(row=1, column=0, sticky="w")


        text_label2 = tk.Label(frame1, text="Villageois", bg="lightgrey", anchor="w", width=10,font = self.custom_font)
        text_label2.grid(row=2, column=0, sticky="w")

        text_label2 = tk.Label(frame1, text=f"{nb_fantassin}", bg="lightgrey", anchor="w", width=10,font = self.custom_font)
        text_label2.grid(row=1, column=1, sticky="w")


        #-------------Frame droite-------------------------------
        
        joueur1_class = self.dico_joueurs[joueur1_nom]
        
        nb_chevalier = joueur1_class.get_chevalier()
        list_vassal = list(joueur1_class.get_vassal().values())
        for vassal in list_vassal:
            nb_chevalier += vassal.get_chevalier()
            
        unite_joueur = (joueur1_class.get_fantassin(),joueur1_class.get_soldat(),nb_chevalier)
        
        
                
        # Ajout des éléments dans la frame gauche
        img_fantassin_mirroir = self.images_tk["fantassin_m"]
        image_label = tk.Label(frame2, image=img_fantassin_mirroir, bg="lightblue")
        image_label.grid(row=1, column=2,sticky="w")

        # Label sous l'image
        text_label = tk.Label(frame2, text="Fantassin", bg="lightblue", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=2, column=2,sticky="e")

        # Spinbox à droite de l'image
        spinbox_fantassin = WidgetCustom.Spinbox_Custom(frame2, from_=0, to=unite_joueur[0], width=5,font = self.custom_font)
        spinbox_fantassin.grid(row=1, column=0,sticky="e")
        
        text_label = tk.Label(frame2, text=f"/ {unite_joueur[0]} ", bg="lightblue", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=1, column=1,sticky="e")
        
        img_soldat_mirroir = self.images_tk["soldat_m"]
        image_label = tk.Label(frame2, image=img_soldat_mirroir, bg="lightblue")
        image_label.grid(row=4, column=2,sticky="w")


        # Label sous l'image
        text_label = tk.Label(frame2, text="Soldat", bg="lightblue", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=5, column=2,sticky="e")

        # Spinbox à droite de l'image
        spinbox_soldat = WidgetCustom.Spinbox_Custom(frame2, from_=0, to=unite_joueur[1], width=5,font = self.custom_font)
        spinbox_soldat.grid(row=4, column=0,sticky="e")
        
        text_label = tk.Label(frame2, text=f"/ {unite_joueur[1]} ", bg="lightblue", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=4, column=1,sticky="e")
        
        img_chevalier_mirroir = self.images_tk["chevalier_m"]
        image_label = tk.Label(frame2, image=img_chevalier_mirroir, bg="lightblue")
        image_label.grid(row=7, column=2,sticky="w")


        # Label sous l'image
        text_label = tk.Label(frame2, text="Chevalier", bg="lightblue", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=8, column=2,sticky="e")

        # Spinbox à droite de l'image
        spinbox_chevalier = WidgetCustom.Spinbox_Custom(frame2, from_=0, to=unite_joueur[2], width=5,font = self.custom_font)
        spinbox_chevalier.grid(row=7, column=0,sticky="w")
        
        text_label = tk.Label(frame2, text=f"/ {unite_joueur[2]} ", bg="lightblue", width=20,font = self.custom_font,anchor=tk.W)
        text_label.grid(row=7, column=1,sticky="e")
        

        # Cadre pour les boutons
        button_frame = tk.Frame(fenetre)
        button_frame.pack(pady=10)
        
        def get_unite_joueur1():
            """recupere les valeurs des spinbox custom et les renvoie sous forme de list"""
            return [spinbox_fantassin.get(),spinbox_soldat.get(),spinbox_chevalier.get()]
        
        
        button_rapide = tk.Button(
            button_frame, text="Calmer la Revolte",font = self.custom_font, width=15,
            command=lambda : self.fenetre_fin_revolte(fenetre,joueur1_nom,get_unite_joueur1(),village,dico_revolte)
            )
        button_rapide.pack(side="left", padx=5)
        Hovertip(button_rapide, "Envoyer votre armée pour tenter de mater la révolte\nAttention : Si vous échoué le village sera détruit.\nSi vous reussissez, tous les villageois révoltés retournerons au travail avec une humeur basse")

        
        button_rapide = tk.Button( 
            button_frame, text="Laisser faire\n(Le village sera détruit)",font = self.custom_font, width=17,
            command=lambda : self.fenetre_fin_revolte(fenetre,joueur1_nom,[0,0,0],village,dico_revolte)
            )
        button_rapide.pack(side="left", padx=5)

   
    
    def simuler_bataille(self,unite_joueur1, unite_joueur2):
        """
        Simule une bataille entre deux unités et retourne le vainqueur.
        """
        
        if unite_joueur1 == unite_joueur2:  # Même tier
            chance_unite_joueur1 = 50
        elif unite_joueur1 == unite_joueur2 - 1:  # Tier inférieur d'un niveau
            chance_unite_joueur1 = 25
        elif unite_joueur1 == unite_joueur2 - 2:  # Tier inférieur de deux niveaux
            chance_unite_joueur1 = 5
        elif unite_joueur1 == unite_joueur2 + 1:  # Tier supérieur d'un niveau
            chance_unite_joueur1 = 75
        elif unite_joueur1 == unite_joueur2 + 2:  # Tier supérieur de deux niveaux
            chance_unite_joueur1 = 95
        else:
            print("Erreur dans simuler_bataille() tier d'unité inconnu")

        if rd.randint(1, 100) <= chance_unite_joueur1:
            return 1  # unite_joueur1 gagne
        else:
            return 2  # unite_joueur2 gagne

    


    def duel_perdu(self,unite_joueur):
        """
        Fait un jet de dé qui depend du tier de l'unité pour savoir si une unité meurt 
        Revoie True si l'unité meurt 
        """
        if unite_joueur == 0:
            chance_mourrir = 50
        elif unite_joueur == 1:
            chance_mourrir = 35
        else:
            chance_mourrir = 15
            
        if rd.randint(1, 100) <= chance_mourrir: #return rd.randint(1, 100) <= chance_mourrir
            return True
        else:
            return False


    def simuler_guerre(self,joueur1,list_unite_joueur1,joueur2,list_unite_joueur2,cout_argent,cout_ressource):
        """
        Simule la guerre entre les deux joueurs et met à jour le label avec le résultat.
        """
        
        
        joueur1_class = self.dico_joueurs[joueur1]
        joueur2_class = self.dico_joueurs[joueur2]
        
        joueur1_class.modifier_argent(-cout_argent)
        joueur1_class.modifier_ressource(-cout_ressource)
        self.barre_menu.update_stats()
    
        
        #on enleve les unité utilisées lors de cette guerre a chaque joueur
        joueur1_class.modifier_fantassin(-list_unite_joueur1[0])
        joueur1_class.modifier_soldat(-list_unite_joueur1[1])
        joueur1_class.modifier_chevalier(-list_unite_joueur1[2])
        
        joueur2_class.modifier_fantassin(-list_unite_joueur2[0])
        joueur2_class.modifier_soldat(-list_unite_joueur2[1])
        joueur2_class.modifier_chevalier(-list_unite_joueur2[2])
        
        
        
        list_blesser_joueur1 = [0,0,0]
        list_mort_joueur1 = [0,0,0]
        
        list_blesser_joueur2 = [0,0,0]
        list_mort_joueur2 = [0,0,0]
        

        def unite_suivante(list_unite):
            """Retourne la prochaine unité disponible et la supprime de la liste."""
            for tier,unite in enumerate(list_unite):
                if unite > 0:
                    list_unite[tier] -= 1
                    return tier
            return None

        unite_joueur1 = unite_suivante(list_unite_joueur1)
        unite_joueur2 = unite_suivante(list_unite_joueur2)
        
        
        
        tour = 0
        while unite_joueur1 != None and unite_joueur2 != None: #TQ les deux joueurs on une unité
            reslultat = self.simuler_bataille(unite_joueur1, unite_joueur2)
            print(f"le joueur {reslultat} gagne au tour {tour}")
            if reslultat == 1: #joueur 1 gagne joueur 2 perd son unité
                if self.duel_perdu(unite_joueur2):
                    list_mort_joueur2[unite_joueur2] += 1
                else:
                    list_blesser_joueur2[unite_joueur2] += 1
                unite_joueur2 = unite_suivante(list_unite_joueur2)  # joueur2 change d'unité
            else: #joueur 2 gagne joueur 1 perd son unité
                if self.duel_perdu(unite_joueur1):
                    list_mort_joueur1[unite_joueur1] += 1
                else:
                    list_blesser_joueur1[unite_joueur1] += 1
                unite_joueur1 = unite_suivante(list_unite_joueur1)  # unite_joueur1 perd
                
            tour += 1

        if unite_joueur1 != None:
            print("Joueur 1 gagne la guerre !")
            victoire =  joueur1
            
            list_unite_joueur1[unite_joueur1] += 1 #remet la dernierre unité qui a gagne son duel dans la liste
        else:
            print("Joueur 2 gagne la guerre !")
            joueur2_class.modifier_argent(cout_argent//2)
            joueur2_class.modifier_ressource(cout_ressource//2)
            self.barre_menu.update_stats()
            victoire =  joueur2
            if unite_joueur2 != None:
                list_unite_joueur2[unite_joueur2] += 1
        
        
        #on remet au joueur les soldats qui sont on vie apres la guerre  
        joueur1_class.modifier_fantassin(list_unite_joueur1[0])
        joueur1_class.modifier_soldat(list_unite_joueur1[1])
        if list_unite_joueur1[2] >= 1: #si il reste au moins 1 chevalier en vie
            joueur1_class.modifier_chevalier(1) #on remet le chevalier au joueur 
            if list_unite_joueur1[2] >1: #puis les vassaux recuppere leur chevalier
                list_vassal = list(joueur1_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier(1)
            
        
        joueur2_class.modifier_fantassin(list_unite_joueur2[0])
        joueur2_class.modifier_soldat(list_unite_joueur2[1])
        if list_unite_joueur2[2] >= 1:
            joueur2_class.modifier_chevalier(1)
            if list_unite_joueur2[2] >1:
                list_vassal = list(joueur2_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier(1)
        
        list_capture1 = []#garde les noms des Noble capturé
        if list_mort_joueur1[2] != 0: #si un chevalier est mort on va considérer qu'il est capturer
            list_vassal_class = list(joueur1_class.get_vassal().values())
            nb_chevalier_capturer = list_mort_joueur1[2]
            nb_chevalier_total = list_mort_joueur1[2]+list_blesser_joueur1[2]+list_unite_joueur1[2] 
            while nb_chevalier_capturer != 0: #on veut que les vassault du joueur soit capturer avant je joueur
                if nb_chevalier_total == 1:
                    joueur1_class.capturer_par(joueur2)
                    list_capture1 += [joueur1_class.get_nom()]
                    nb_chevalier_capturer -= 1
                    nb_chevalier_total -= 1
                else :
                    list_vassal_class[nb_chevalier_capturer-2].capturer_par(joueur2)
                    list_capture1 += [list_vassal_class[nb_chevalier_capturer-2].get_nom()]
                    nb_chevalier_capturer -= 1
                    nb_chevalier_total -= 1
         
        list_capture2 = []
        #de meme avec l'autre joueur
        if list_mort_joueur2[2] != 0: #si un chevalier est mort on va considérer qu'il est capturer
            list_vassal_class = list(joueur2_class.get_vassal().values())
            nb_chevalier_capturer = list_mort_joueur2[2]
            nb_chevalier_total = list_mort_joueur2[2]+list_blesser_joueur2[2]+list_unite_joueur2[2] 
            while nb_chevalier_capturer != 0: #on veut que les vassault du joueur soit capturer avant je joueur
                if nb_chevalier_total == 1:
                    joueur2_class.capturer_par(joueur1)
                    list_capture2 += [joueur2_class.get_nom()]
                    nb_chevalier_capturer -= 1
                    nb_chevalier_total -= 1
                else :
                    list_vassal_class[nb_chevalier_capturer-2].capturer_par(joueur1)
                    list_capture2 += [list_vassal_class[nb_chevalier_capturer-2].get_nom()]
                    nb_chevalier_capturer -= 1
                    nb_chevalier_total -= 1
                               
        
        #on rajoute les blesser a la leur liste d'attente resspective, il seron de nouveau disponnible au prochain tour 
        joueur1_class.modifier_fantassin_en_attente(list_blesser_joueur1[0])
        joueur1_class.modifier_soldat_en_attente(list_blesser_joueur1[1]) 
        if list_blesser_joueur1[2]>= 1:
            joueur1_class.modifier_chevalier_en_attente(1)
            if list_blesser_joueur1[2] >1:
                list_vassal = list(joueur1_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier_en_attente(1)
        
        
        joueur2_class.modifier_fantassin_en_attente(list_blesser_joueur2[0])
        joueur2_class.modifier_soldat_en_attente(list_blesser_joueur2[1])
        if list_blesser_joueur2[2] >= 1:
            joueur2_class.modifier_chevalier_en_attente(1)
            if list_blesser_joueur2[2] >1:
                list_vassal = list(joueur2_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier_en_attente(1)
        self.barre_menu.update_unite()
        self.resultat_guerre = victoire == joueur1
        self.rapport = (joueur1,list_unite_joueur1,list_blesser_joueur1,list_mort_joueur1,list_capture1,joueur2,list_unite_joueur2,list_blesser_joueur2,list_mort_joueur2,list_capture2,victoire,cout_argent,cout_ressource)
        if joueur1 != "Joueur":
            self.guerre_en_cours = False
        return (joueur1,list_unite_joueur1,list_blesser_joueur1,list_mort_joueur1,list_capture1,joueur2,list_unite_joueur2,list_blesser_joueur2,list_mort_joueur2,list_capture2,victoire,cout_argent,cout_ressource)
        
    def simuler_revolte(self,joueur1,list_unite_joueur1,village, dico_revolte):
        
        joueur1_class = self.dico_joueurs[joueur1]
        
        #on enleve les unité utilisées lors de cette guerre a chaque joueur
        joueur1_class.modifier_fantassin(-list_unite_joueur1[0])
        joueur1_class.modifier_soldat(-list_unite_joueur1[1])
        joueur1_class.modifier_chevalier(-list_unite_joueur1[2])
        
        list_blesser_joueur1 = [0,0,0]
        list_mort_joueur1 = [0,0,0]
        
        def unite_suivante(list_unite):
            """Retourne la prochaine unité disponible et la supprime de la liste."""
            for tier,unite in enumerate(list_unite):
                if unite > 0:
                    list_unite[tier] -= 1
                    return tier
            return None
        unite_joueur1 = unite_suivante(list_unite_joueur1)
        # Récupérer et supprimer le premier élément
        
        list_villageois = list(dico_revolte.items())
        tour = 0    
        nb_mort = 0
        while unite_joueur1 != None and list_villageois != []: 
            reslultat = self.simuler_bataille(unite_joueur1, 0)
            print(f"le joueur {reslultat} gagne au tour {tour}")
            if reslultat == 1: #joueur 1 gagne 
                villageois = list_villageois.pop(0)
                villageois[1].fin_de_revolte()
                if self.duel_perdu(0): #si le villageois meurt
                    
                    village.tuer_villageois(villageois[1],villageois[0]-nb_mort)
                    del(dico_revolte[villageois[0]])
                    nb_mort += 1
            else: #joueur 2 gagne joueur 1 perd son unité
                #un chevalier ne peut pas se faire capturer par un village
                if self.duel_perdu(unite_joueur1):         
                    list_mort_joueur1[unite_joueur1] += 1
                else:
                    list_blesser_joueur1[unite_joueur1] += 1
                unite_joueur1 = unite_suivante(list_unite_joueur1)  # unite_joueur1 perd
                
            tour += 1
        
        if unite_joueur1 != None:
            print("Joueur 1 Maté la revolte !")
            victoire =  joueur1            
            list_unite_joueur1[unite_joueur1] += 1 #remet la dernierre unité qui a gagne son duel dans la liste
        else:
            print("La revolte a gagné !")
            victoire =  "village"
        
        
        
        #on remet au joueur les soldats qui sont on vie apres la guerre  
        joueur1_class.modifier_fantassin(list_unite_joueur1[0])
        joueur1_class.modifier_soldat(list_unite_joueur1[1])
        if list_unite_joueur1[2] >= 1: #si il reste au moins 1 chevalier en vie
            joueur1_class.modifier_chevalier(1) #on remet le chevalier au joueur 
            if list_unite_joueur1[2] >1: #puis les vassaux recuppere leur chevalier
                list_vassal = list(joueur1_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier(1)
        
        list_blesser_joueur1[2] += list_mort_joueur1[2] #Les villageois ne peuvent pas capturer le noble donc si il meurt il est juste blesser
        
        #on rajoute les blesser a la leur liste d'attente resspective, il seron de nouveau disponnible au prochain tour 
        joueur1_class.modifier_fantassin_en_attente(list_blesser_joueur1[0])
        joueur1_class.modifier_soldat_en_attente(list_blesser_joueur1[1]) 
        if list_blesser_joueur1[2]>= 1:
            joueur1_class.modifier_chevalier_en_attente(1)
            if list_blesser_joueur1[2] >1:
                list_vassal = list(joueur1_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier_en_attente(1)
                    
        list_villageois_restant = list(dico_revolte.values())
        for villageois in list_villageois_restant:
            villageois.gestionhumeur(3) #Les villageois qui on survecu a la revolte gagne 5 de bonheur (pour eviter les revolte en boucle)
        
        village.finir_revolte_village()
        
        self.barre_menu.update_unite()
        self.resultat_guerre = victoire == joueur1
        self.rapport = (joueur1,list_unite_joueur1,list_blesser_joueur1,list_mort_joueur1,village,dico_revolte,nb_mort,victoire)
        if joueur1 != "Joueur":
            self.guerre_en_cours = False
        return (joueur1,list_unite_joueur1,list_blesser_joueur1,list_mort_joueur1,village,dico_revolte,nb_mort,victoire)
        
       
    def fenetre_fin_guerre(self,fenetre,joueur1,list_unite_joueur1,joueur2,list_unite_joueur2,cout_argent,cout_ressource):
        
        self.clear_fenetre(fenetre)
        
        fenetre.title("Rapport de Guerre")
        fenetre.geometry("800x600")
        

        # Création d'un frame pour contenir les labels
        frame_label = tk.Frame(fenetre)
        frame_label.pack(side='top', fill="x",pady=10) 

        # Configuration des colonnes du frame pour une disposition dynamique
        frame_label.columnconfigure(0, weight=1)  
        frame_label.columnconfigure(1, weight=1) 
        frame_label.columnconfigure(2, weight=1) 
        frame_label.rowconfigure(0, weight=1) 
        
        joueur1_class = self.dico_joueurs[joueur1]
        joueur2_class = self.dico_joueurs[joueur2]
        
        
        

        # Texte "joueur1" en haut à gauche
        label_joueur1 = tk.Label(frame_label, text=f"{joueur1_class.get_nom()}", font = self.custom_font)
        label_joueur1.grid(row=0, column=0, sticky="ne", padx=10)
        label_joueur1 = tk.Label(frame_label, text="(vous)", font = self.custom_font)
        label_joueur1.grid(row=1, column=0, sticky="ne", padx=10)

        # Texte "contre" au centre
        label_contre = tk.Label(frame_label, text="contre", font = self.custom_font)
        label_contre.grid(row=0, column=1, sticky="n", padx=20)

        # Texte "joueur2" en haut à droite
        label_joueur2 = tk.Label(frame_label, text=f"{joueur2_class.get_nom()}", font = self.custom_font)
        label_joueur2.grid(row=0, column=2, sticky="nw", padx=10)
        
        

        # Création de frame pour contenir deux frame
        frame_box = tk.Frame(fenetre)  
        frame_box.pack(side='top', fill="both", expand=True) 

        # Sous-frames dans frame_box
        frame1 = tk.Frame(frame_box, height=50, bg='lightgray', width=100,relief="sunken", bd=2)
        frame1.pack(side="left", fill="both", expand=True,padx=1) 
        frame1.pack_propagate(False)

        frame2 = tk.Frame(frame_box, height=50, bg='lightblue', width=100,relief="sunken", bd=2)
        frame2.pack(side="right", fill="both", expand=True,padx=1) 
        frame2.pack_propagate(False)
        
        def fin_guerre(fenetre):
            self.custom_font.config(size=12)
            self.guerre_en_cours = False
            fenetre.destroy()
            
            
        btn = tk.Button(fenetre, text="Continuer", command=lambda :fin_guerre(fenetre))
        btn.pack(side="top",pady=10)
        
        
        
        rapport_guerre = self.simuler_guerre(joueur1,list_unite_joueur1,joueur2,list_unite_joueur2,cout_argent,cout_ressource)
        
        texte_joueur1,texte_joueur2 = self.generer_rapport(rapport_guerre)
        
        victoire = rapport_guerre[10]
        if victoire == joueur1:
            texte_victoir = ("Victoire !","green")
        else:
            texte_victoir = ("Défaite !","red")
        

        label_victoir = tk.Label(frame_label, text=f"{texte_victoir[0]}", font = self.custom_font,fg=f"{texte_victoir[1]}")
        label_victoir.grid(row=1, column=1, sticky="n", padx=20)
       
        # Ajout des textes générés dans les frames
        text_joueur1 = tk.Text(frame1, wrap="word", font = self.custom_font, bg="lightgray", relief="flat")
        text_joueur1.insert("1.0", texte_joueur1)  # Insère le texte du joueur 1
        text_joueur1.config(state="disabled")  # Rend le texte non modifiable
        text_joueur1.pack()
    
        text_joueur2 = tk.Text(frame2, wrap="word", font = self.custom_font, bg="lightblue", relief="flat")
        text_joueur2.insert("1.0", texte_joueur2)  # Insère le texte du joueur 2
        text_joueur2.config(state="disabled")  # Rend le texte non modifiable
        text_joueur2.pack()
    
    

    def fenetre_guerre_anime(self, fenetre, joueur1, list_unite_joueur1, joueur2, list_unite_joueur2, cout_argent, cout_ressource):
        self.clear_fenetre(fenetre)
        fenetre.title("Guerre animée")
        fenetre.geometry("800x800")
        
        # Frame pour afficher le GIF
        self.gif_label = tk.Label(fenetre, width=700, height=400)
        self.gif_label.pack(pady=10)
    
        # Création de frame pour contenir deux frame
        frame_box = tk.Frame(fenetre)  
        frame_box.pack(side='top', fill="both", expand=True) 
        
        # Ajout de la scrollbar
        scrollbar = tk.Scrollbar(frame_box, orient="vertical")
        scrollbar.pack(side="left", fill="y")
    
        # Sous-frames dans frame_box
        frame1 = tk.Frame(frame_box, height=50, bg='lightgray', width=100, relief="sunken", bd=2)
        frame1.pack(side="left", fill="both", expand=True, padx=1) 
        frame1.pack_propagate(False)
    
        frame2 = tk.Frame(frame_box, height=50, bg='lightblue', width=100, relief="sunken", bd=2)
        frame2.pack(side="right", fill="both", expand=True, padx=1) 
        frame2.pack_propagate(False)
        
        # Ajout des textes générés dans les frames
        text_joueur1 = tk.Text(frame1, wrap="word", font = self.custom_font, bg="lightgray", relief="flat", yscrollcommand=scrollbar.set)
        text_joueur1.pack(fill="both", expand=True)
        
        text_joueur2 = tk.Text(frame2, wrap="word", font = self.custom_font, bg="lightblue", relief="flat", yscrollcommand=scrollbar.set)
        text_joueur2.pack(fill="both", expand=True)
        
        fenetre.update()
        
        text_joueur1.tag_configure("rouge", foreground="red")
        text_joueur1.tag_configure("vert", foreground="green")
        
        text_joueur2.tag_configure("rouge", foreground="red")
        text_joueur2.tag_configure("vert", foreground="green")
    
        # Lier la scrollbar aux deux Text widgets
        def sync_scroll(*args):
            text_joueur1.yview(*args)
            text_joueur2.yview(*args)
    
        scrollbar.config(command=sync_scroll)
        text_joueur1.config(yscrollcommand=scrollbar.set)
        text_joueur2.config(yscrollcommand=scrollbar.set)
        
        joueur1_class = self.dico_joueurs[joueur1]
        joueur2_class = self.dico_joueurs[joueur2]
        
        joueur1_class.modifier_argent(-cout_argent)
        joueur1_class.modifier_ressource(-cout_ressource)
        self.barre_menu.update_stats()
    
        # On enlève les unités utilisées lors de cette guerre à chaque joueur
        joueur1_class.modifier_fantassin(-list_unite_joueur1[0])
        joueur1_class.modifier_soldat(-list_unite_joueur1[1])
        joueur1_class.modifier_chevalier(-list_unite_joueur1[2])
        
        joueur2_class.modifier_fantassin(-list_unite_joueur2[0])
        joueur2_class.modifier_soldat(-list_unite_joueur2[1])
        joueur2_class.modifier_chevalier(-list_unite_joueur2[2])
    
        list_blesser_joueur1 = [0, 0, 0]
        list_mort_joueur1 = [0, 0, 0]
    
        list_blesser_joueur2 = [0, 0, 0]
        list_mort_joueur2 = [0, 0, 0]
        
        
        def unite_suivante(list_unite):
            """Retourne la prochaine unité disponible et la supprime de la liste."""
            for tier, unite in enumerate(list_unite):
                if unite > 0:
                    list_unite[tier] -= 1
                    return tier
            return None
    
        unite_joueur1 = unite_suivante(list_unite_joueur1)
        unite_joueur2 = unite_suivante(list_unite_joueur2)
        def charger_gif(gif_path):
            """
            Mélange de mthode trouvée sur Stackoverflow
            Charge toutes les images du GIF et les retourne.
            """
            frames = []
            gif = Image.open(gif_path)
            for frame in range(gif.n_frames):
                gif.seek(frame)
                frames.append(ImageTk.PhotoImage(gif))
            return frames
    
        def afficher_gif(frames, i, callback=None):
            """Affiche l'animation du GIF image par image."""
            if i < len(frames):
                self.gif_label.config(image=frames[i])
                fenetre.after(90, afficher_gif, frames, i + 1, callback)  # Appel récursif pour afficher l'image suivante
            elif callback:
                callback()  # Appel du callback une fois le GIF terminé
    
        tour = 1
        def lancer_tour():
            nonlocal unite_joueur1,list_blesser_joueur1,list_mort_joueur1, unite_joueur2,list_blesser_joueur2,list_mort_joueur2, tour
    
            if unite_joueur1 == None or unite_joueur2 == None:  # Vérifier si une unité est morte
                if unite_joueur1 != None:
                    img = Image.open("Images/guerre/victoire.png").resize((700, 400), Image.LANCZOS)
                else:
                    img = Image.open("Images/guerre/defaite.png").resize((700, 400), Image.LANCZOS)
         
                img = ImageTk.PhotoImage(img)         
                self.current_image = img
                self.gif_label.config(image=img)
                
                self.fin_de_guerre_animer(fenetre, joueur1, joueur1_class, unite_joueur1, list_unite_joueur1, list_blesser_joueur1, list_mort_joueur1, joueur2, joueur2_class, unite_joueur2, list_unite_joueur2, list_blesser_joueur2, list_mort_joueur2, cout_argent, cout_ressource,text_joueur1,text_joueur2)
            else:     
                resultat = self.simuler_bataille(unite_joueur1, unite_joueur2)
                print(f"Le joueur {resultat} gagne au tour {tour}")
        
                # Charger le GIF
                if resultat == 1:
                    gif_path = self.dico_gif[str(unite_joueur1) + str(unite_joueur2) + str(resultat)]
                else:
                    gif_path = self.dico_gif[str(unite_joueur2) + str(unite_joueur1) + str(resultat)]
                frames_gif = charger_gif(gif_path)
        
                # Affichage du GIF et lancement de la prochaine bataille après le délai
                afficher_gif(frames_gif, 0, lambda: prochaine_bataille(resultat))
    
        def prochaine_bataille(resultat):
            nonlocal unite_joueur1,list_blesser_joueur1,list_mort_joueur1, unite_joueur2,list_blesser_joueur2,list_mort_joueur2, tour
            # Affichage du texte des résultats de la bataille
            self.custom_font.config(size=12)
            text_joueur1.insert("end", f"Tour {tour}"+"-"*30+"\n\n")
            text_joueur2.insert("end", f"Tour {tour}"+"-"*30+"\n\n")
            
            if resultat == 1:  # joueur 1 gagne, joueur 2 perd son unité
                if self.duel_perdu(unite_joueur2):
                    list_mort_joueur2[unite_joueur2] += 1
                    text_joueur2.insert("end", f"Le {self.dico_tier_unit[unite_joueur2]} Ennemi est mort en combat\n\n", "rouge")
                else:
                    list_blesser_joueur2[unite_joueur2] += 1
                    text_joueur2.insert("end", f"Le {self.dico_tier_unit[unite_joueur2]} Ennemi a été blessé en combat\n\n", "rouge")
                unite_joueur2 = unite_suivante(list_unite_joueur2)  # joueur2 change d'unité
                text_joueur1.insert("end", f"Votre {self.dico_tier_unit[unite_joueur1]} a gagné sa bataille\n\n", "vert")
            else:  # joueur 2 gagne, joueur 1 perd son unité
                if self.duel_perdu(unite_joueur1):
                    list_mort_joueur1[unite_joueur1] += 1
                    text_joueur1.insert("end", f"Votre {self.dico_tier_unit[unite_joueur1]} est mort en combat\n\n", "rouge")
                else:
                    list_blesser_joueur1[unite_joueur1] += 1
                    text_joueur1.insert("end", f"Votre {self.dico_tier_unit[unite_joueur1]} a été blessé en combat\n\n", "rouge")
                unite_joueur1 = unite_suivante(list_unite_joueur1)  # unite_joueur1 perd
                text_joueur2.insert("end", f"Le {self.dico_tier_unit[unite_joueur2]} Ennemi a gagné sa bataille\n\n", "vert")
            
            text_joueur1.yview(tk.END)
            text_joueur2.yview(tk.END)
            fenetre.after(30)
            tour += 1
            lancer_tour()  # Lancer le tour suivant
        lancer_tour()  # Lancer le tour suivant
        
        
    def fin_de_guerre_animer(self,fenetre,joueur1,joueur1_class,unite_joueur1,list_unite_joueur1,list_blesser_joueur1,list_mort_joueur1,joueur2,joueur2_class, unite_joueur2,list_unite_joueur2,list_blesser_joueur2,list_mort_joueur2,cout_argent,cout_ressource,text_joueur1,text_joueur2):
        if unite_joueur1 != None:
            print("Joueur 1 gagne la guerre !")
            victoire =  joueur1
            
            list_unite_joueur1[unite_joueur1] += 1 #remet la dernierre unité qui a gagne son duel dans la liste
        else:
            print("Joueur 2 gagne la guerre !")
            joueur2_class.modifier_argent(cout_argent//2)
            joueur2_class.modifier_ressource(cout_ressource//2)
            self.barre_menu.update_stats()
            victoire =  joueur2
            if unite_joueur2 != None:
                list_unite_joueur2[unite_joueur2] += 1
        
       
        
        #on remet au joueur les soldats qui sont on vie apres la guerre  
        joueur1_class.modifier_fantassin(list_unite_joueur1[0])
        joueur1_class.modifier_soldat(list_unite_joueur1[1])
        if list_unite_joueur1[2] >= 1: #si il reste au moins 1 chevalier en vie
            joueur1_class.modifier_chevalier(1) #on remet le chevalier au joueur 
            if list_unite_joueur1[2] >1: #puis les vassaux recuppere leur chevalier
                list_vassal = list(joueur1_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier(1)
            
        
        joueur2_class.modifier_fantassin(list_unite_joueur2[0])
        joueur2_class.modifier_soldat(list_unite_joueur2[1])
        if list_unite_joueur2[2] >= 1:
            joueur2_class.modifier_chevalier(1)
            if list_unite_joueur2[2] >1:
                list_vassal = list(joueur2_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier(1)
        
        list_capture1 = []#garde les noms des Noble capturé
        if list_mort_joueur1[2] != 0: #si un chevalier est mort on va considérer qu'il est capturer
            list_vassal_class = list(joueur1_class.get_vassal().values())
            nb_chevalier_capturer = list_mort_joueur1[2]
            nb_chevalier_total = list_mort_joueur1[2]+list_blesser_joueur1[2]+list_unite_joueur1[2] 
            while nb_chevalier_capturer != 0: #on veut que les vassault du joueur soit capturer avant je joueur
                if nb_chevalier_total == 1:
                    joueur1_class.capturer_par(joueur2)
                    list_capture1 += [joueur1_class.get_nom()]
                    nb_chevalier_capturer -= 1
                    nb_chevalier_total -= 1
                else :
                    list_vassal_class[nb_chevalier_capturer-2].capturer_par(joueur2)
                    list_capture1 += [list_vassal_class[nb_chevalier_capturer-2].get_nom()]
                    nb_chevalier_capturer -= 1
                    nb_chevalier_total -= 1
        list_capture2 = []
        #de meme avec l'autre joueur
        if list_mort_joueur2[2] != 0: #si un chevalier est mort on va considérer qu'il est capturer
            list_vassal_class = list(joueur2_class.get_vassal().values())
            nb_chevalier_capturer = list_mort_joueur2[2]
            nb_chevalier_total = list_mort_joueur2[2]+list_blesser_joueur2[2]+list_unite_joueur2[2] 
            while nb_chevalier_capturer != 0: #on veut que les vassault du joueur soit capturer avant je joueur
                if nb_chevalier_total == 1:
                    joueur2_class.capturer_par(joueur1)
                    list_capture2 += [joueur2_class.get_nom()]
                    nb_chevalier_capturer -= 1
                    nb_chevalier_total -= 1
                else :
                    list_vassal_class[nb_chevalier_capturer-2].capturer_par(joueur1)
                    list_capture2 += [list_vassal_class[nb_chevalier_capturer-2].get_nom()]
                    nb_chevalier_capturer -= 1
                    nb_chevalier_total -= 1
                               
        
        #on rajoute les blesser a la leur liste d'attente resspective, il seron de nouveau disponnible au prochain tour 
        joueur1_class.modifier_fantassin_en_attente(list_blesser_joueur1[0])
        joueur1_class.modifier_soldat_en_attente(list_blesser_joueur1[1]) 
        if list_blesser_joueur1[2]>= 1:
            joueur1_class.modifier_chevalier_en_attente(1)
            if list_blesser_joueur1[2] >1:
                list_vassal = list(joueur1_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier_en_attente(1)
        
        
        joueur2_class.modifier_fantassin_en_attente(list_blesser_joueur2[0])
        joueur2_class.modifier_soldat_en_attente(list_blesser_joueur2[1])
        if list_blesser_joueur2[2] >= 1:
            joueur2_class.modifier_chevalier_en_attente(1)
            if list_blesser_joueur2[2] >1:
                list_vassal = list(joueur2_class.get_vassal().values())
                for vassal in list_vassal:
                    vassal.modifier_chevalier_en_attente(1)
        self.barre_menu.update_unite()
        self.resultat_guerre = victoire == joueur1
        self.rapport = (joueur1,list_unite_joueur1,list_blesser_joueur1,list_mort_joueur1,list_capture1,joueur2,list_unite_joueur2,list_blesser_joueur2,list_mort_joueur2,list_capture2,victoire,cout_argent,cout_ressource)
        rapport_guerre = (joueur1,list_unite_joueur1,list_blesser_joueur1,list_mort_joueur1,list_capture1,joueur2,list_unite_joueur2,list_blesser_joueur2,list_mort_joueur2,list_capture2,victoire,cout_argent,cout_ressource)
        texte_joueur1,texte_joueur2 = self.generer_rapport(rapport_guerre)
        text_joueur1.insert("end",texte_joueur1)
        text_joueur2.insert("end",texte_joueur2)
        
        # Désactiver les Text widgets pour qu'ils soient non modifiables
        text_joueur1.config(state="disabled")
        text_joueur2.config(state="disabled")
        
        def fin_guerre(fenetre):
            self.custom_font.config(size=12)
            self.guerre_en_cours = False
            fenetre.destroy()
        # Bouton pour fermer l'application
        close_button = tk.Button(fenetre, text="Fermer",font=self.custom_font, command=lambda :fin_guerre(fenetre))
        close_button.pack(pady = 10)
        
        

        
            
        
    def fenetre_fin_revolte(self,fenetre,joueur1,list_unite_joueur1,village,dico_revolte):
        
        self.clear_fenetre(fenetre)
        
        fenetre.title("Rapport de revolte")
        fenetre.geometry("800x600")  # Dimensions initiales
        

        # Création d'un frame pour contenir les labels
        frame_label = tk.Frame(fenetre)
        frame_label.pack(side='top', fill="x",pady=10)  # Le frame occupe tout l'espace disponible

        # Configuration des colonnes du frame pour une disposition dynamique
        frame_label.columnconfigure(0, weight=1)  # Colonne gauche
        frame_label.columnconfigure(1, weight=1)  # Colonne centrale
        frame_label.columnconfigure(2, weight=1)  # Colonne droite
        frame_label.rowconfigure(0, weight=1)  # Ligne contenant les labels
        
        joueur1_class = self.dico_joueurs[joueur1]
        
        
        

        # Texte "joueur1" en haut à gauche
        label_village = tk.Label(frame_label, text=f"{village.get_nom()} en revolte", font = self.custom_font)
        label_village.grid(row=0, column=0, sticky="ne", padx=10)
        

        # Texte "contre" au centre
        label_contre = tk.Label(frame_label, text="contre", font = self.custom_font)
        label_contre.grid(row=0, column=1, sticky="n", padx=20)

        # Texte "joueur2" en haut à droite
        label_joueur2 = tk.Label(frame_label, text=f"{joueur1_class.get_nom()}", font = self.custom_font)
        label_joueur2.grid(row=0, column=2, sticky="nw", padx=10)
        label_joueur1 = tk.Label(frame_label, text="(vous)", font = self.custom_font)
        label_joueur1.grid(row=1, column=2, sticky="nw", padx=10)
        
        

        # Création de frame pour contenir deux frame
        frame_box = tk.Frame(fenetre)  
        frame_box.pack(side='top', fill="both", expand=True) 

        # Sous-frames dans frame_box
        frame1 = tk.Frame(frame_box, height=50, bg='lightgray', width=100,relief="sunken", bd=2)
        frame1.pack(side="left", fill="both", expand=True,padx=1) 
        frame1.pack_propagate(False)

        frame2 = tk.Frame(frame_box, height=50, bg='lightblue', width=100,relief="sunken", bd=2)
        frame2.pack(side="right", fill="both", expand=True,padx=1) 
        frame2.pack_propagate(False)

        def fin_guerre(fenetre):
            self.custom_font.config(size=12)
            self.guerre_en_cours = False
            fenetre.destroy()
            
        # Bouton en dessous
        btn = tk.Button(fenetre, text="Continuer", command=lambda :fin_guerre(fenetre))
        btn.pack(side="top",pady=10)
        
        rapport_revolte = self.simuler_revolte(joueur1,list_unite_joueur1,village, dico_revolte)
        texte_joueur1,texte_joueur2 = self.generer_rapport_revolte(rapport_revolte)
        
        victoire = rapport_revolte[7]
        if victoire == joueur1:
            texte_victoir = ("Revolte répriméé !","green")
        else:
            texte_victoir = ("Défaite !","red")
        
        # Texte "joueur2" en haut à droite
        label_victoir = tk.Label(frame_label, text=f"{texte_victoir[0]}", font=("Arial", 16,"bold"),fg=f"{texte_victoir[1]}")
        label_victoir.grid(row=1, column=1, sticky="n", padx=20)
        # Ajout des textes générés dans les frames
        text_joueur1 = tk.Text(frame2, wrap="word", font = self.custom_font, bg="lightgray", relief="flat")
        text_joueur1.insert("1.0", texte_joueur1)  # Insère le texte du joueur 1
        text_joueur1.config(state="disabled")  # Rend le texte non modifiable
        text_joueur1.pack()
    
        text_joueur2 = tk.Text(frame1, wrap="word", font = self.custom_font, bg="lightblue", relief="flat")
        text_joueur2.insert("1.0", texte_joueur2)  # Insère le texte du joueur 2
        text_joueur2.config(state="disabled")  # Rend le texte non modifiable
        text_joueur2.pack()
        
        
    def generer_rapport(self,rapport_guerre):
        """
        Génère deux textes cohérents à partir des données du rapport de guerre.
        Retourne deux textes : un pour le joueur 1 et un pour le joueur 2.
        """
        joueur1, list_unite_joueur1, list_blesser_joueur1, list_mort_joueur1,list_capture1,joueur2, list_unite_joueur2, list_blesser_joueur2, list_mort_joueur2,list_capture2,victoire, cout_argent,cout_ressource = rapport_guerre
        
        def afficher_captures(list_capture):
            if list_capture != []:  # Si des chevaliers sont capturés et la liste n'est pas vide
                texte_captures = "\n".join(f"Noble capturé : {nom}" for nom in list_capture)
            else:  # Aucun chevalier capturé ou liste vide
                texte_captures = "Noble capturé : Aucun."
            
            return texte_captures
        
        def defense_reussi():
            texte = ''
            if victoire == joueur2:
                texte += f"Le défenseur victorieux remporte :\n \t{cout_argent//2} d'argent \n\t{cout_ressource//2} ressources"
            return texte
        
        # Construction du texte pour le joueur 1
        chevalier_capture1 = list_mort_joueur1[2] >= 1 #Renvoie s'il y'a eu des noble capturer 
        texte_joueur1 = (
            f"Rapport de guerre pour {joueur1} :\n\n"
            f"Unités restantes : \n\t{list_unite_joueur1[0]} fantassins, \n\t{list_unite_joueur1[1]} soldats, \n\t{list_unite_joueur1[2]} chevaliers\n"
            f"Unités blessées : \n\t{list_blesser_joueur1[0]} fantassins, \n\t{list_blesser_joueur1[1]} soldats, \n\t{list_blesser_joueur1[2]} chevaliers\n"
            f"Unités perdues : \n\t{list_mort_joueur1[0]} fantassins, \n\t{list_mort_joueur1[1]} soldats\n\n"
            f"{afficher_captures(list_capture1)}\n\n"
            f"{'Vous pouvez payer pour votre liberration et celle de vos vassaux au joueur qui vous a vaincu' if chevalier_capture1 else ''}\n\n"
            f"Résultat : {'Victoire !' if victoire == joueur1 else 'Défaite.'}\n"
        ) 
        # Construction du texte pour le joueur 2
        texte_joueur2 = (
            f"Rapport de guerre pour {joueur2} :\n\n"
            f"Unités restantes : \n\t{list_unite_joueur2[0]} fantassins,\n\t{list_unite_joueur2[1]} soldats, \n\t{list_unite_joueur2[2]} chevaliers\n"
            f"Unités blessées : \n\t{list_blesser_joueur2[0]} fantassins, \n\t{list_blesser_joueur2[1]} soldats, \n\t{list_blesser_joueur2[2]} chevaliers\n"
            f"Unités perdues : \n\t{list_mort_joueur2[0]} fantassins, \n\t{list_mort_joueur2[1]} soldats\n\n"
            f"{afficher_captures(list_capture2)}\n\n"
            f"Résultat : {'Victoire !' if victoire == joueur2 else 'Défaite.'}\n\n"
            f"{defense_reussi()}\n"
        )
        
    
        return texte_joueur1, texte_joueur2
    
    def generer_rapport_revolte(self,rapport_revolte):
        joueur1,list_unite_joueur1,list_blesser_joueur1,list_mort_joueur1,village,dico_revolte,nb_mort,victoire = rapport_revolte
        
        def afficher_captures(list_capture):
            if list_capture != []:  # Si des chevaliers sont capturés et la liste n'est pas vide
                texte_captures = "\n".join(f"Noble capturé : {nom}" for nom in list_capture)
            else:  # Aucun chevalier capturé ou liste vide
                texte_captures = "Noble capturé : Aucun."
            
            return texte_captures
    
        # Construction du texte pour le joueur 1
        texte_joueur1 = (
            f"Rapport de guerre pour {joueur1} :\n\n"
            f"Unités restantes : \n\t{list_unite_joueur1[0]} fantassins, \n\t{list_unite_joueur1[1]} soldats, \n\t{list_unite_joueur1[2]} chevaliers\n"
            f"Unités blessées : \n\t{list_blesser_joueur1[0]} fantassins, \n\t{list_blesser_joueur1[1]} soldats, \n\t{list_blesser_joueur1[2]} chevaliers\n"
            f"Unités perdues : \n\t{list_mort_joueur1[0]} fantassins, \n\t{list_mort_joueur1[1]} soldats\n\n"
            f"Résultat : {'Victoire !' if victoire == joueur1 else 'Défaite.'}\n"
        ) 
        
        if victoire == "village":
            texte_joueur2 = f"La révolte a reussi à repousser son Seigneur et a détruit le village de {village.get_nom()}"
        else:
            texte_joueur2 = f"Votre armée a reprimer la révolte mais a fait {nb_mort} mort(s), le reste des révolutionnaire vont retourner au village avec une humeur basse"
        
        return texte_joueur1,texte_joueur2

    
    
    
    
    
    
    def clear_fenetre(self,fenetre):
        # Parcourir et détruire tous les widgets enfants de la fenêtre principale
        for widget in fenetre.winfo_children():
            widget.destroy()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    