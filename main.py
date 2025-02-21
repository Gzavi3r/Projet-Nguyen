# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:21:37 2024

@author: Brice
"""

import CreationMap
import GestionMenu
import GestionClass



import tkinter as tk
from tkinter import font
import os
from PIL import Image, ImageTk
import random as rd


#certain code basique et générique on été générer par IA(chatgpt) pour gagner du temps et car il n'y avais aucun interet pedagogique :
    #telle que :les passage d'une liste d'information un texte mise en forme 
    #Les creation de fenetre avec une mise en page simple et basique

#j'ai trouvé cette fançon d'appeller et gérer les frame sur stackoverflow 


class CreationTitre(tk.Tk):
    """
    Représente la fenêtre principale de l'application "Risk of Conquest".
    
    Hérite de la classe `tk.Tk` et configure la fenêtre principale avec un titre, une taille,
    un fond noir, et des fonctionnalités spécifiques comme le changement de fenêtre.

    :ivar _frame: Le cadre actuel affiché dans la fenêtre.
    """
    def __init__(self):
        """
        Initialise la fenêtre principale avec des paramètres spécifiques.
        
        Charge une police personnalisée si disponible et affiche l'écran titre initial.
        
        """
        tk.Tk.__init__(self)
        self.title("Risk of Conquest")
        self.geometry("1024x750")
        self["bg"] = "black"
        self.resizable(False, False)  # Bloque le redimensionnement de la fenêtre
        self._frame = None
        self.update_idletasks() #met a jour winfo_width() et winfo_height()
        
        def load_font(path):
            """
            Charge une police personnalisée depuis le chemin spécifié.
            
            :param path: Le chemin du fichier de police.
            :return: Le nom de la police chargée ou `None` si la police n'a pas été trouvée.
            """
            if os.path.exists(path):
                os.system(f"fc-cache -f {os.path.dirname(path)}")  # Recharge les polices dans le système (Linux/Windows)
                return os.path.basename(path).split(".")[0]  # Retourne le nom de la police
            else:
                print(f"Erreur : La police n'a pas été trouvée à {path}")
                return None
            
        font_name = load_font('Images/Bitsential.otf')
        if font_name:
            # Utiliser la police dans un widget (si le nom est valide)
            custom_font = font.Font(family=font_name, size=20)
        else:
            custom_font = font.Font(family="Arial", size=12)
            
        self.ChangerFenetre(EcranTitre,0,0,custom_font)

    def ChangerFenetre(self, frame_class, *args):
        """
        Change le cadre actuel pour un nouveau cadre.
        
        :param frame_class: La classe du cadre à afficher.
        :param args: Les arguments supplémentaires nécessaires pour le constructeur du cadre.
        """
        new_frame = frame_class(self, *args)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
        

class EcranTitre(tk.Frame):
    """
    Représente l'écran titre de l'application.
    
    Affiche les options pour jouer, accéder aux paramètres, ou quitter le jeu.
    """
    def __init__(self, master,tuto,cheat,custom_font):
        """
        Initialise l'écran titre avec un arrière-plan et des boutons pour naviguer.
        
        :param master: le conteneur parent.
        :param tuto: État du tutoriel (activé/désactivé).
        :param cheat: État de la triche (activé/désactivé).
        :param custom_font: La police personnalisée à utiliser pour les boutons.
        """
        custom_font.config(size=20)
        tk.Frame.__init__(self, master)
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        img = Image.open("Images/bg/bg_menu_principale.png").resize((window_width, window_height), Image.LANCZOS)
        self.img_bg = ImageTk.PhotoImage(img)
        
        
        
        
        canvas_bg = tk.Canvas(self, width = window_width, height = window_height)
        canvas_bg.pack(fill = "both", expand = True) 
        canvas_bg.create_image( 0, 0, image = self.img_bg,  anchor = "nw") 
        
        tk.Button(self, text="Jouer",font=custom_font, command=lambda: master.ChangerFenetre(ParametreJeux,tuto,cheat,custom_font)).place(anchor = tk.N, relx = 0.5, rely = 0.35)
        tk.Button(self, text="Option",font=custom_font, command=lambda: master.ChangerFenetre(Option,tuto,cheat,custom_font)).place(anchor = tk.N, relx = 0.5, rely = 0.7)
        tk.Button(self, text="Quitter",font=custom_font, command=master.destroy).place(anchor = tk.N, relx = 0.5, rely = 0.8)




class Option(tk.Frame):
    """
    Représente la page des options de l'application.
    
    Permet de modifier la taille de la fenêtre, activer/désactiver le tutoriel et la triche, et de revenir à l'écran titre.
    """
    def __init__(self, master, tuto, cheat, custom_font):
        """
        Initialise la page des options avec des éléments interactifs.
        
        :param master:le conteneur parent.
        :param tuto: État du tutoriel (activé/désactivé).
        :param cheat: État de la triche (activé/désactivé).
        :param custom_font: La police personnalisée à utiliser pour les éléments.
        """
        tk.Frame.__init__(self, master)
        self.pack(expand=True, fill="both")

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        # Canvas pour l'image de fond
        self.canvas_bg = tk.Canvas(self, width=self.master.winfo_width(), height=self.master.winfo_height())
        self.canvas_bg.pack(fill="both", expand=True)



        # Titre de la page
        title_label = tk.Label(self, text="Page des options", font=custom_font)
        

        # Menu déroulant pour changer la taille de la fenêtre
        self.size_var = tk.StringVar(value=f"{self.master.winfo_width()}x{self.master.winfo_height()}")  # Taille initiale        
        size_label = tk.Label(self, text="Changer la taille de la fenêtre (1024x750 recommandé):", font=custom_font)
        

        sizes = ["900x600", "1024x750", "1600x900", "Taille maximale"]
        self.size_menu = tk.OptionMenu(self, self.size_var, *sizes, command=self.change_size)
        

        # Checkbox pour le didacticiel
        self.didacticiel_var = tk.IntVar(value=tuto)
        didacticiel_check = tk.Checkbutton(
            self,
            text="Activer le Didacticiel(Pas implémenté)",
            variable=self.didacticiel_var,
            font=custom_font,
            relief="sunken"
        )

        # Checkbox pour la triche
        self.triche_var = tk.IntVar(value=cheat)
        triche_check = tk.Checkbutton(
            self,
            text="Activer la Triche\n(Donne de manière illimitée de l'argent, des ressources et des unités)",
            variable=self.triche_var,
            font=custom_font,
            relief="sunken"
        )
        

        # Bouton de retour
        retour_button = tk.Button(
            self,
            text="Retour",
            font=custom_font,
            command=lambda: master.ChangerFenetre(EcranTitre, self.didacticiel_var.get(), self.triche_var.get(), custom_font)
        )
        
        
        def update_background():
            """
            Met à jour l'arrière-plan et repositionne les éléments lors du redimensionnement.
            """
            window_width = self.master.winfo_width()
            window_height = self.master.winfo_height()
            img = Image.open("Images/bg/bg_menu_option.png").resize((window_width, window_height), Image.LANCZOS)
            self.img_bg = ImageTk.PhotoImage(img)
            self.canvas_bg.create_image(0, 0, image=self.img_bg, anchor="nw")
            self.canvas_bg.create_window(self.master.winfo_width() // 2, self.master.winfo_height() * 0.1, window=title_label, anchor="n")
            self.canvas_bg.create_window(self.master.winfo_width() // 2, self.master.winfo_height() * 0.2, window=size_label, anchor="n")
            self.canvas_bg.create_window(self.master.winfo_width() // 2, self.master.winfo_height() * 0.5, window=didacticiel_check, anchor="n")
            self.canvas_bg.create_window(self.master.winfo_width() // 2, self.master.winfo_height() * 0.3, window=self.size_menu, anchor="n")
            self.canvas_bg.create_window(self.master.winfo_width() // 2, self.master.winfo_height() * 0.6, window=triche_check, anchor="n")
            self.canvas_bg.create_window(self.master.winfo_width() // 2, self.master.winfo_height() * 0.9, window=retour_button, anchor="n")

        self.bind("<Configure>", lambda event: update_background())
        
        
    def change_size(self, selected_size):
        """
        Change la taille de la fenêtre principale selon l'option sélectionnée.
        
        :param selected_size: La taille choisie pour la fenêtre (e.g., "900x600").
        """
        
        
        if selected_size == "Taille maximale":
            #Maximiser la fenêtre 
            #self.master.state("zoomed")
            self.master.attributes("-fullscreen", False)
            selected_size = f'{self.screen_width}x{self.screen_height}'
            self.master.geometry(selected_size)
            
        else:
            # Ajuste à une taille prédéfinie
            self.master.attributes("-fullscreen", False)  # Désactive le mode plein écran si activé
            self.master.state("normal")  # Revenir au mode normal si maximisé
            self.master.geometry(selected_size)
            




class ParametreJeux(tk.Frame):
    """
    Classe représentant l'écran de configuration des paramètres de jeu.
    
    """
    def __init__(self, master,tuto,cheat,custom_font):
        """
        Initialise l'écran des paramètres de jeu, permettant de choisir le nombre de joueurs
        et la taille de la carte.
        
        :param master: Fenêtre principale de l'application.
        :param tuto: Booléen indiquant si le didacticiel est activé.
        :param cheat: Booléen indiquant si le mode triche est activé.
        :param custom_font: Police personnalisée utilisée dans l'interface.
        """
        tk.Frame.__init__(self, master)
        self.pack(expand=True, fill="both")
        
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        
        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        img = Image.open("Images/bg/bg_menu_option.png").resize((window_width, window_height), Image.LANCZOS)
        self.img_bg = ImageTk.PhotoImage(img)
    
        canvas_bg = tk.Canvas(self, width = window_width, height = window_height)
        canvas_bg.pack(fill = "both", expand = True) 
        canvas_bg.create_image( 0, 0, image = self.img_bg,  anchor = "nw") 
        
        # Titre de la page
        tk.Label(self, text="Paramètres du jeu",font=custom_font).place(anchor = tk.N, relx = 0.5, rely = 0.1)
        
        

        # Section pour sélectionner le nombre de joueurs
        tk.Label(self, text="Nombre de joueurs :",font=custom_font).place(anchor = tk.N, relx = 0.5, rely = 0.2)
        self.nb_joueurs_var = tk.IntVar(value=2)  # Valeur par défaut
        options_joueurs = [2, 3, 4]
        self.menu_joueurs = tk.OptionMenu(self, self.nb_joueurs_var, *options_joueurs)
        self.menu_joueurs.place(anchor = tk.N, relx = 0.5, rely = 0.3)

        # Section pour sélectionner la taille de la carte
        tk.Label(self, text="Taille de la carte :",font=custom_font).place(anchor = tk.N, relx = 0.5, rely = 0.5)
        self.taille_map_var = tk.IntVar(value=16)  # Valeur par défaut
        options_taille = [16, 24, 32]
        self.menu_taille = tk.OptionMenu(self, self.taille_map_var, *options_taille)
        self.menu_taille.place(anchor = tk.N, relx = 0.5, rely = 0.6)
        
        tk.Button(self, text="Retour",font=custom_font,command=lambda: master.ChangerFenetre(EcranTitre,tuto,cheat,custom_font)).place(anchor = tk.N, relx = 0.3, rely = 0.8)
        tk.Button(self, text="Jouer",font=custom_font,command=lambda :self.lancer_jeu(tuto,cheat,custom_font)).place(anchor = tk.N, relx = 0.7, rely = 0.8)
        
    def lancer_jeu(self,tuto, cheat, custom_font):
        """
        Récupère les paramètres sélectionnés et passe à l'écran de jeu.
        
        :param tuto: Booléen indiquant si le didacticiel est activé.
        :param cheat: Booléen indiquant si le mode triche est activé.
        :param custom_font: Police personnalisée utilisée dans l'interface.
        """
        nb_joueurs = self.nb_joueurs_var.get()
        taille_map = self.taille_map_var.get()

        # Passer les paramètres à l'écran Plateau_jeux
        self.master.ChangerFenetre(PlateauJeux, nb_joueurs, taille_map,tuto ,cheat,custom_font)
        
        
        
        
class PlateauJeux(tk.Frame):
    """
    Classe représentant le plateau de jeu où les joueurs interagissent avec la carte.

    """
    def __init__(self, fenetre, nb_joueur, taille_map, tuto, cheat ,custom_font):
        """
        Initialise le plateau de jeu avec les joueurs, la carte et les interfaces nécessaires.
        
        :param fenetre: Fenêtre principale de l'application.
        :param nb_joueur: Nombre de joueurs dans la partie.
        :param taille_map: Taille de la carte en nombre de cases.
        :param tuto: Booléen indiquant si le didacticiel est activé.
        :param cheat: Booléen indiquant si le mode triche est activé.
        :param custom_font: Police personnalisée utilisée dans l'interface.
        """
        tk.Frame.__init__(self, fenetre)
        
        self.nb_joueus = nb_joueur
        self.taille_map = taille_map
        
        #/!\ la seed est transmise a tout les autre fichier et est la seed global au jeux
        self.seed = rd.randint(0, 2**32 - 1)  # Seed aléatoire (32 bits) mettre un entier pour toujours avoir le meme aléatoire 

        
        self.matrice = CreationMap.Initialisation_Map(taille_map, self.seed, nb_joueur)
        self.taille_image = 64
        self.dico_joueurs = creer_joueurs(nb_joueur)
        self.menu_actif = ("idle","Autre")
        self.dico_village = {}
        self.dico_images_tk = cree_image_tk(self.taille_image)
        self.dico_images = {
                                0: ("plaine", self.dico_images_tk["plaine_Neutre"], self.dico_images_tk["plaine_Joueur"], self.dico_images_tk["plaine_Ennemi 1"], self.dico_images_tk["plaine_Ennemi 2"], self.dico_images_tk["plaine_Ennemi 3"]),
                                1: ("foret", self.dico_images_tk["foret_Neutre"], self.dico_images_tk["foret_Joueur"], self.dico_images_tk["foret_Ennemi 1"], self.dico_images_tk["foret_Ennemi 2"], self.dico_images_tk["foret_Ennemi 3"]),
                                2: ("montagne", self.dico_images_tk["montagne_Neutre"], self.dico_images_tk["montagne_Joueur"], self.dico_images_tk["montagne_Ennemi 1"], self.dico_images_tk["montagne_Ennemi 2"], self.dico_images_tk["montagne_Ennemi 3"]),
                                3: ("lac", self.dico_images_tk["lac_Neutre"], self.dico_images_tk["lac_Joueur"], self.dico_images_tk["lac_Ennemi 1"], self.dico_images_tk["lac_Ennemi 2"], self.dico_images_tk["lac_Ennemi 3"]),
                                4: ("village", self.dico_images_tk["village"], self.dico_images_tk["village"], self.dico_images_tk["village"], self.dico_images_tk["village"], self.dico_images_tk["village"])
                           }
        self.dico_valeur = {
                            "village":0,
                            "plaine": 3,
                            "foret": 4,
                            "montagne": 5,
                            "lac": 2
                           }
        
        
        self.canvas_menu = tk.Canvas(self, width=320,bg ="red") 
        
        self.canvas_map = tk.Canvas(self, width=self.taille_map * self.taille_image, height=self.taille_map * self.taille_image)
        self.update_idletasks()  
        
        self.label_menu = tk.Canvas(self, height=30, bg="blue")
        self.label_menu.pack(side=tk.TOP,fill=tk.X) 
        self.label_menu.pack_propagate(False)

        self.barre_menu = GestionMenu.GestionLabel(self.label_menu, self.dico_joueurs["Joueur"],custom_font)

        #on pack le canvas menu apres la creation de la barre de menu
        self.canvas_menu.pack(side = tk.RIGHT,fill = tk.Y)
 
        
        # Créer une barre de défilement verticale sans l'afficher (à gauche)
        self.scrollbar_y = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas_map.yview,repeatinterval = 500)
        self.scrollbar_y.pack(side=tk.LEFT, fill=tk.Y)

        # Créer une barre de défilement horizontale sans l'afficher (en bas)
        self.scrollbar_x = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas_map.xview, repeatinterval = 500)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        #on pack apres les scrollbar
        self.canvas_map.pack(side = tk.LEFT)
        #le rectangle de selection doit etre créer apres toute les images de la map mais doit etre initialiser avant GestionMenu donc on lui donne pour id temporaire taillemap**2 +1
        self.selection_rect = self.taille_map**2+1
        
        # Configurer le canvas_map pour qu'il prenne en compte les barres de défilement
        self.canvas_map.config(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Définir la région qui peut être scrollée (basée sur la taille de la matrice et des images)
        self.canvas_map.config(scrollregion=(0, 0, self.taille_map * self.taille_image, self.taille_map * self.taille_image))

        self.scrollbar_x.config(command=self.canvas_map.xview)
        self.scrollbar_y.config(command=self.canvas_map.yview)
        
        # Associer les événements pour le défilement avec le clic droit
        self.canvas_map.bind("<ButtonPress-3>", self.commencer_defilement)
        self.canvas_map.bind("<B3-Motion>", self.defilement)  # Lorsque le bouton droit est enfoncé et que la souris bouge
    
        self.Menu = GestionMenu.Initialisation_Menu(fenetre,self.seed,self.taille_map,self.taille_image,self.canvas_map, self.canvas_menu,self.barre_menu,self.dico_village,self.dico_joueurs,self.dico_images_tk,self.dico_valeur ,self.selection_rect,tuto,cheat,custom_font)
        self.initialisation_map()
        self.selection_rect = self.canvas_map.create_rectangle(0, 0, self.taille_image, self.taille_image, outline="black", width=2)
        self.canvas_map.itemconfig(self.selection_rect, state="hidden")

    # Fonction pour capturer la position de la souris au clic droit (Melange de code trouvé sur Stackoverflow)
    def commencer_defilement(self,event):
        """
        Capture la position initiale de la souris pour le défilement de la carte.
        
        :param event: Événement contenant les coordonnées de la souris.
        """
        self.canvas_map.scan_mark(event.x, event.y)  # Marque la position initiale du clic

    # Fonction pour déplacer la carte en fonction du mouvement de la souris
    def defilement(self,event):
        """
        Déplace la vue de la carte en fonction du mouvement de la souris.
        
        :param event: Événement contenant les coordonnées de la souris.
        """
        self.canvas_map.scan_dragto(event.x, event.y, gain=1)  # Déplace en suivant la souris
    
    def initialisation_map(self):
        """
        Initialise la carte du jeu en créant les cases, les images correspondantes,
        et les villages associés.
        """
        # Dessiner les images sur le canvas_map
        Liste_village = []
        for i in range(self.taille_map):
            for j in range(self.taille_map):
                x = j * self.taille_image
                y = i * self.taille_image
                terrain_type = self.dico_images[self.matrice[i][j][0]][0] #recupere le type dans la matrice Map
                image_tk = self.dico_images[self.matrice[i][j][0]][self.matrice[i][j][1]+1] #recupere l'image corresspondant a l'appartenance dans la matrice Map
                image_id = self.canvas_map.create_image(x, y, anchor=tk.NW, image=image_tk) 
                #ajout pour chaque case de son tag type
                self.canvas_map.addtag_withtag(terrain_type, image_id)
                
                #ajout pour chaque case de son tag appartenance 
                if self.matrice[i][j][1] == 0:
                    self.canvas_map.addtag_withtag("Neutre", image_id)
                elif self.matrice[i][j][1] == 1:
                    self.canvas_map.addtag_withtag("Joueur", image_id)
                    if terrain_type == "village":
                        Liste_village += [("Joueur",image_id)]
                else:
                    self.canvas_map.addtag_withtag(f"Ennemi {self.matrice[i][j][1]-1}", image_id)
                    if terrain_type == "village":
                        Liste_village += [(f"Ennemi {self.matrice[i][j][1]-1}",image_id)]
                self.canvas_map.tag_bind(image_id, "<Button-1>", self.Menu.selection)
                self.canvas_map.tag_bind(image_id, "<Button-3>", self.Menu.deselection)
        
        #creation des villge apres la map pour que toutes les cases soit créée
        for appartenance,image_id in Liste_village:
            village = self.Menu.initialisation_village(image_id,10)
            self.dico_joueurs[appartenance].ajouter_village(image_id,village)
    





def creer_joueurs(nb_joueur):
    """
    Crée un nombre spécifié de nobles et les retourne dans un dictionnaire avec des clés nommées pour les joueurs et ennemis.

    :param nb_joueur: Nombre de nobles (joueurs) à créer, doit être inférieur ou égal à 4.
    :return: Dictionnaire des nobles créés.
    """
    dico_joueurs = {}
    if nb_joueur > 4:
        print("Erreur : Le nombre de joueurs ne peut pas dépasser 4.")

    for i in range(nb_joueur):
        joueur = GestionClass.Noble(100,100)
        if i == 0:
            dico_joueurs["Joueur"] = joueur  # Le premier joueur est le "Joueur"
        else:
            dico_joueurs[f"Ennemi {i}"] = joueur  # Les autres sont des ennemis

        print(f"{joueur.nom} a été créé comme {('Joueur' if i == 0 else f'Ennemi {i}')}.")
    return dico_joueurs

def cree_image_tk(taille_image):
    """
    Charge et redimensionne des images pour les utiliser avec Tkinter, en fonction d'une taille donnée.
    
    :param taille_image: Taille souhaitée (en pixels) pour chaque côté des images (carrées).
    :return: Dictionnaire contenant les images redimensionnées et prêtes pour Tkinter, associées à leurs noms.
             Exemple : {"village": <ImageTk.PhotoImage>, ...}.
    """
    images_tk = {}
    # Liste des chemins et noms d'images
    images_info = {
        "village": "Images/case/village.jpg",
        "village_incendie": "Images/case/village_incendie.png",
        "village_epidemie": "Images/case/village_epidemie.png",
        "plaine_Neutre": "Images/case/plaine_neutre.png",
        "foret_Neutre": "Images/case/foret_neutre.png",
        "montagne_Neutre": "Images/case/montagne_neutre.png",
        "lac_Neutre": "Images/case/lac_neutre.png",
        "plaine_Joueur": "Images/case/plaine_joueur.png",
        "foret_Joueur": "Images/case/foret_joueur.png",
        "montagne_Joueur": "Images/case/montagne_joueur.png",
        "lac_Joueur": "Images/case/lac_joueur.png",
        "plaine_Ennemi 1": "Images/case/plaine_ennemi1.png",
        "foret_Ennemi 1": "Images/case/foret_ennemi1.png",
        "montagne_Ennemi 1": "Images/case/montagne_ennemi1.png",
        "lac_Ennemi 1": "Images/case/lac_ennemi1.png",
        "plaine_Ennemi 2": "Images/case/plaine_ennemi2.png",
        "foret_Ennemi 2": "Images/case/foret_ennemi2.png",
        "montagne_Ennemi 2": "Images/case/montagne_ennemi2.png",
        "lac_Ennemi 2": "Images/case/lac_ennemi2.png",
        "plaine_Ennemi 3": "Images/case/plaine_ennemi3.png",
        "foret_Ennemi 3": "Images/case/foret_ennemi3.png",
        "montagne_Ennemi 3": "Images/case/montagne_ennemi3.png",
        "lac_Ennemi 3": "Images/case/lac_ennemi3.png",
        
        
        
        "fantassin": "Images/unite/fantassin.png",
        "fantassin_m": "Images/unite/fantassin_m.png",
        
        "soldat": "Images/unite/soldat.png",
        "soldat_m": "Images/unite/soldat_m.png",
        
        "chevalier": "Images/unite/chevalier.png",
        "chevalier_m": "Images/unite/chevalier_m.png"
        
        
    }
    # Chargement et transformation des images
    for name, path in images_info.items():
        img = Image.open(path).resize((taille_image, taille_image), Image.LANCZOS)
        images_tk[name] = ImageTk.PhotoImage(img)
    return images_tk
        

if __name__ == "__main__":
    app = CreationTitre()
    app.mainloop()