# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:47:12 2024

@author: Brice
"""
import main
import GestionClass
import GestionIA
import GestionEvenement
import GestionGuerre
from WidgetCustom import Button_Custom

import tkinter as tk
from tkinter import messagebox
#utiliser pour faire les tooltip des boutons
from idlelib.tooltip import Hovertip


from PIL import Image, ImageTk  # Nécessite le module Pillow
import random as rd


class GestionLabel:
    """
    Permet de modifier et gérer la barre de menu située en haut de l'interface,
    visible et utilisable uniquement par le joueur.
    
    :param barre_menu: L'objet Canvas représentant la barre de menu.
    :param joueur: Instance représentant le joueur, contenant ses informations.
    :param custom_font: Police personnalisée utilisée pour afficher les textes.
    """
    def __init__(self, barre_menu, joueur,custom_font):
        """
        Initialise les éléments visuels et les images nécessaires pour afficher 
        les statistiques et unités dans la barre de menu.
        
        :param barre_menu: L'objet Canvas représentant la barre de menu.
        :param joueur: Instance du joueur avec ses statistiques et unités.
        :param custom_font: Police personnalisée pour les textes dans le menu.
        """
        self.barre_menu = barre_menu
        self.joueur = joueur
        self.custom_font = custom_font
        
        
        # Charger les images
        self.pierre_image = ImageTk.PhotoImage(Image.open("Images/ressource/pierre.png").resize((20, 25)))
        self.coffre_plein_image = ImageTk.PhotoImage(Image.open("Images/ressource/coffre_plein.png").resize((25, 25)))
        self.coffre_image = ImageTk.PhotoImage(Image.open("Images/ressource/coffre.png").resize((25, 25)))
        self.coffre_vide_image = ImageTk.PhotoImage(Image.open("Images/ressource/coffre_vide.png").resize((25, 25)))
        self.tete_fantassin = ImageTk.PhotoImage(Image.open("Images/unite/fantassin_head.png").resize((25, 25)))
        self.tete_soldat = ImageTk.PhotoImage(Image.open("Images/unite/soldat_head.png").resize((28, 25)))
        self.tete_chevalier = ImageTk.PhotoImage(Image.open("Images/unite/chevalier_head.png").resize((30, 25)))
        
        self.frame_btn_option = tk.Frame(self.barre_menu,bg = 'green')
        self.frame_btn_option.pack(side="left", padx=5)
        
        self.frame_btn_fin = tk.Frame(self.barre_menu,bg = 'green')
        self.frame_btn_fin.pack(side="right", padx=5)
        
        self.couleur = 'white'
        
        
    
        
    
    def dessiner_menu_stat(self):
        """
        Dessine les statistiques du joueur dans la barre de menu, incluant l'argent et les ressources.
        
        :return: None
        """
        x_offset = 90
        y_offset = 17
        
        if self.joueur.get_argent() >= 500:
            image_argent = self.coffre_plein_image         
        elif self.joueur.get_argent() >= 250:
            image_argent = self.coffre_image
        else:
            image_argent = self.coffre_vide_image
        
        #image + texte argent
        self.barre_menu.create_image(x_offset, y_offset - 13, anchor=tk.NW, image=image_argent,tags = "stat")
        x_offset += image_argent.width() + 2      
        text_id = self.barre_menu.create_text(x_offset, y_offset, text=f"{self.joueur.get_argent()}", anchor="w", fill=self.couleur, font=self.custom_font,tags = "stat")
        bbox = self.barre_menu.bbox(text_id)
        x_offset = bbox[2] + 20
        
        #image + texte ressource
        self.barre_menu.create_image(x_offset, y_offset - 13, anchor=tk.NW, image=self.pierre_image,tags = "stat")
        x_offset += self.pierre_image.width() + 2      
        text_id = self.barre_menu.create_text(x_offset, y_offset, text=f"{self.joueur.get_ressource()}", anchor="w", fill=self.couleur, font=self.custom_font,tags = "stat")
        bbox = self.barre_menu.bbox(text_id)
    
        
        
    def dessiner_menu_unite(self):
        """
        Dessine les unités du joueur dans la barre de menu, incluant fantassins, soldats, et chevaliers.
        
        :return: None
        """
        x_offset = 280
        y_offset = 16
        #image + texte fantassin
        self.barre_menu.create_image(x_offset, y_offset - 13, anchor=tk.NW, image=self.tete_fantassin,tags = "unit")
        x_offset += self.tete_fantassin.width() + 2      
        text_id = self.barre_menu.create_text(x_offset, y_offset, text=f"{self.joueur.get_fantassin()} ({self.joueur.get_fantassin_en_attente()})", anchor="w", fill=self.couleur, font=self.custom_font,tags = "unit")
        bbox = self.barre_menu.bbox(text_id)
        x_offset = bbox[2] + 13
        
        #image + texte soldat
        self.barre_menu.create_image(x_offset, y_offset - 13, anchor=tk.NW, image=self.tete_soldat,tags = "unit")
        x_offset += self.tete_soldat.width() + 2      
        text_id = self.barre_menu.create_text(x_offset, y_offset, text=f"{self.joueur.get_soldat()} ({self.joueur.get_soldat_en_attente()})", anchor="w", fill=self.couleur, font=self.custom_font,tags = "unit")
        bbox = self.barre_menu.bbox(text_id)
        x_offset = bbox[2] + 13
        
        nb_chevalier = self.joueur.get_chevalier()
        nb_chevalier_en_attente = self.joueur.get_chevalier_en_attente()
        list_vassal = list(self.joueur.get_vassal().values())
        for vassal in list_vassal:
            nb_chevalier += vassal.get_chevalier()
            nb_chevalier_en_attente += vassal.get_chevalier_en_attente()
        
        #image + texte chevalier
        self.barre_menu.create_image(x_offset, y_offset - 13, anchor=tk.NW, image=self.tete_chevalier,tags = "unit")
        x_offset += self.tete_chevalier.width() + 2      
        text_id = self.barre_menu.create_text(x_offset, y_offset, text=f"{nb_chevalier} ({nb_chevalier_en_attente})", anchor="w", fill=self.couleur, font=self.custom_font,tags = "unit")
        bbox = self.barre_menu.bbox(text_id)
        
    def dessiner_menu_event(self,event):
        """
        Affiche un texte indiquant l'événement en cours dans la barre de menu.
        
        :param event: Texte décrivant l'événement.
        :return: None
        """
        x_offset = 580
        y_offset = 17
        #Texte event
        text_id = self.barre_menu.create_text(x_offset, y_offset, text=f"Evenement :{event}", anchor="w", fill=self.couleur, font=self.custom_font,tags = "event")
        bbox = self.barre_menu.bbox(text_id)
        x_offset = bbox[2] + 3
        
        
    def get_frame_fin(self):
        return self.frame_btn_fin
    
    def get_frame_menu(self):
        return self.frame_btn_option

    def get_canvas(self):
        return self.barre_menu
        
        
    
    def update_unite(self):
        """
        Met à jour l'affichage des unités dans la barre de menu.
        
        :return: None
        """
        self.barre_menu.delete("unit")
        self.dessiner_menu_unite()

    def update_stats(self):
        """
        Met à jour l'affichage des statistiques dans la barre de menu.
        
        :return: None
        """
        # Actualiser les labels avec les dernières valeurs
        self.barre_menu.delete("stat")
        self.dessiner_menu_stat()
    
    def update_event(self,event):
        """
        Met à jour l'affichage de l'événement en cours dans la barre de menu.
        
        :param event: Texte décrivant l'événement.
        :return: None
        """
        self.barre_menu.delete("event")
        self.dessiner_menu_event(event)


class Initialisation_Menu():
    """
    Permet de gérer tout les widgets affiché dans le canvas de gauche.
    Il sert aussi de moteur de jeux
    """

    def __init__(self,root,seed,taille_map,taille_image,canvas_map,canvas_menu,barre_menu,dico_village,dico_joueurs,images_tk ,dico_valeur,selection_rect,tuto,cheat ,custom_font):
        """
        Initialise les paramètres nécessaires au moteur du jeu et configure les éléments de l'interface.
  
        :param root: La fenêtre principale de l'application.
        :param seed: La graine aléatoire pour générer des événements.
        :param taille_map: La taille de la carte du jeu.
        :param taille_image: La taille des images sur la carte.
        :param canvas_map: Le canvas où est affichée la carte du jeu.
        :param canvas_menu: Le canvas où sont affichés les menus.
        :param barre_menu: La barre de menu affichée dans l'application.
        :param dico_village: Dictionnaire contenant les informations sur les villages.
        :param dico_joueurs: Dictionnaire contenant les informations sur les joueurs.
        :param images_tk: Liste des images utilisées dans le jeu (au format Tkinter).
        :param dico_valeur: Dictionnaire contenant diverses valeurs de jeu.
        :param selection_rect: Rectangle utilisé pour indiquer la sélection dans le canvas de la carte.
        :param tuto: Indique si le tutoriel est activé ou non.
        :param cheat: Indique si les options de triche sont activées.
        :param custom_font: Police personnalisée utilisée pour l'affichage du texte.
        :return: None
        """
        self.root = root
        rd.seed(seed)
        self.taille_map = taille_map
        self.taille_image = taille_image
        self.canvas_map = canvas_map
        self.canvas_menu = canvas_menu
        self.barre_menu = barre_menu
        self.dico_village = dico_village
        self.dico_joueurs = dico_joueurs
        self.images_tk = images_tk
        self.dico_valeur = dico_valeur
        self.selection_rect = selection_rect
        self.tuto = tuto
        self.cheat = cheat
        self.custom_font = custom_font
        
        self.id_image_bg_menu = None
        
        self.nb_de_tour = 0

        self.dico_images_bg = {
            "bg_menu": "Images/bg/menu_bg.png", 
            "bg_eglise": "Images/bg/eglise_bg.png",
            "bg_village": "Images/bg/bg_village.png",
            "bg_caserne": "Images/bg/bg_caserne.png"
        }
        
        #TODO changer les prix en fonction du gamplay
        self.dico_prix = {
            "creation_village": (150,130),
            "conquete": (25,15),
            "creation_eglise": (120,100),
            "creation_caserne": (120,120),
            "festival": (25,20),
            "venir_villageois":(20,30),
            "former_fantassin":(20,10),
            "former_soldat":(35,20),
            "recruter_fantassin":(40,25),
            "recruter_soldat":(85,50),
            "vassaliser": self.valeur_vassalisation,
            "liberer_joueur":(100,100),
            "liberer_vassal":(95,95)
            
            }
    
        
        
        self.bg_menu_actuelle = "bg_menu"
        
        #bind pour update la taille du bg du menu et de la barre menu (utile si l'option changer taille ecran est accessible durant la partie )
        self.canvas_menu.bind("<Configure>", lambda event: self.update_background(self.dico_images_bg[self.bg_menu_actuelle]))
        
        
        #premet de savoir la valeur des taxes lors de taxer tout les village 
        self.valeur_tax = [0,0]
        
        self.id_rectangle_selection = None
        #booleen qui premet de savor si le jeux est fini et bloque certaine fonction
        self.fin_du_jeux = False
        self.tour_joueur = True
        
        #on initialise le menu actif a vide
        self.menu_actif = ()

        self.texte = tk.StringVar() #Le texte qui sert dans les introduction de case
        self.texte_introrapport = tk.StringVar() #Le texte qui sert dans les intro du sous menu rapport village
        self.texte_introeglise = tk.StringVar() #Le texte qui sert dans les intro du sous menu eglise
        self.texte_rapport_joueur = tk.StringVar()
        
        #le texte utiliser par la fenetre bloquante durant le tour des IA
        self.fenetre_bloquante_tour = tk.StringVar() #
        self.fenetre_bloquante_joueur = tk.StringVar()
        
        #Le texte dans les rapport de debut de tour
        self.label_intro_debut_tour = tk.StringVar()
        self.text_rapport_debut_tour = []
        #dico pour s'avoir si des vassaux on ete "exiger" (on initialise se dico avec tout les ennemi pour ne pas avoir a le gérer plus tard)
        self.dico_vassal_exiger = {}
        for ennemi_nom in self.dico_joueurs: 
            self.dico_vassal_exiger[ennemi_nom] = [False,False] #le booleen argent_exiger , ressource_exiger
        
        
        #Au premier tour on joue dans l'ordre (Joueur -> Ennemi 1 -> Ennemi 2 ...)
        self.tour_jeux = list(dico_joueurs.keys())
        #on definit le joueur qui joue actuellement 
        self.joueur_actuelle = self.tour_jeux.pop(0)
        #indique si la fenetre bloquante est activée ou non
        self.fenetre_bloquante = None
        #on initialise la classe qui va permettre de choisir et d'executer des evenement aleatoire 
        self.Evenement = GestionEvenement.Initialisation_Evenement(self.root,seed,self,self.canvas_map,self.canvas_menu,self.barre_menu,self.dico_village,self.dico_joueurs,self.images_tk,self.label_intro_debut_tour)
        self.Guerre = GestionGuerre.Initialisation_Guerre(self.root,seed,self,self.canvas_map,self.canvas_menu,self.barre_menu,self.dico_village,self.dico_joueurs,self.images_tk,custom_font)
        self.IA = GestionIA.Initialisation_IA(root, seed, self,self.Guerre, taille_map, taille_image, canvas_map, canvas_menu, barre_menu, dico_village, dico_joueurs, images_tk, dico_valeur,self.dico_prix)
        # Création des widgets du menu une seule fois
        self.cree_widget()
        
    
    def selection(self,event):
        """
        Gère l'événement de sélection d'une case sur le canvas de la carte.
        
        :param event: L'événement déclenché lors du clic sur une case.
        :return: None
        """
        if self.bg_menu_actuelle != "bg_menu":
            self.bg_menu_actuelle = "bg_menu"
            self.update_background(self.dico_images_bg[self.bg_menu_actuelle])
        # Obtenir l'ID de l'image sous le curseur
        image_id = self.canvas_map.find_withtag("current")
        
        
        self.id_rectangle_selection = image_id[0]
        #afficher le bon menu        
        self.affiche_menu()
              

        # Obtenir les coordonnées de l'image
        x1, y1, x2, y2 = self.canvas_map.bbox(image_id)
        
        #on verifie que le rectangle de selection et bien afficher et on le bouge au meme endroit que la case cliquée
        if self.canvas_map.itemcget(self.selection_rect, "state") == "normal":    
            self.canvas_map.coords(self.selection_rect,x1+1, y1+1, x2-1, y2-1)
        else:
            # Dessiner un rectangle autour de la case sélectionnée
            self.canvas_map.itemconfig(self.selection_rect, state="normal")
            self.canvas_map.coords(self.selection_rect,x1+1, y1+1, x2-1, y2-1)
        
        


    def deselection(self,event):
        """
        Fonction appeller lors d'un clique droit
        """
        if self.bg_menu_actuelle != "bg_menu":
            self.bg_menu_actuelle = "bg_menu"
            self.update_background(self.dico_images_bg[self.bg_menu_actuelle])
        self.id_rectangle_selection = None
        self.affiche_menu(self.widget_menu_autre ,"idle")
        # cacher le rectangle de sélection s'il existe (pour clic droit)
        if self.canvas_map.itemcget(self.selection_rect, "state") == "normal":
            self.canvas_map.itemconfig(self.selection_rect, state="hidden")
        
    def cree_widget(self):
        """
        Initialise et configure les widgets de l'interface utilisateur.
        
        Cette fonction crée des boutons, menus déroulants, labels et autres
        composants graphiques en fonction des différentes catégories 
        (Joueur, Neutre, Ennemi) et états possibles dans le jeu.
        
        Les IA peuvent utiliser les fonctionnalités du menu, mais seuls 
        les joueurs humains peuvent voir et modifier ces widgets.
        
        :return: None
        """
        ressource_image = ImageTk.PhotoImage(Image.open("Images/ressource/pierre.png").resize((20, 25)))
        or_image = ImageTk.PhotoImage(Image.open("Images/ressource/coffre.png").resize((25, 25)))
        
        
        self.custom_font.config(size=12)
        
        
        
        #bouton fin du tour toujours afficher dans la barre menu
        bouton_fin_tour = Button_Custom(self.barre_menu.get_frame_fin(),("Fin de tour","black",self.custom_font), None, None, None, None,bg="white",height = 20,command= self.fin_de_tour)
        bouton_fin_tour.pack(side="right")
        Hovertip(bouton_fin_tour, "Lance la fin du tour,\ntous les villagesois de vos villages vont:\nProduire des ressources\nManger\nCommercer\nLes autres joueur vont jouer leur tour dans un ordre aléatoire\nVous aurez un rapport au début de votre prochain tour")
        
        # Création du menu déroulant
        menu_deroulant  = tk.Menubutton(self.barre_menu.get_frame_menu() , text="Menu",font = self.custom_font, underline=0)

        menu = tk.Menu(menu_deroulant, tearoff=False)
        
        # Ajout des options au menu déroulant
        menu.add_command(label="Sauvegarder",font = self.custom_font, state="disabled") 
        menu.add_command(label="Charger", font = self.custom_font, state="disabled")      
        menu.add_separator()                                     
        menu.add_command(label="Accueil", font = self.custom_font, command=self.retour_ecran_titre)     
        menu.add_command(label="Quitter", font = self.custom_font, command=self.root.destroy)       
        menu_deroulant["menu"] = menu
        menu_deroulant.pack()
        
        if self.cheat:
            bouton_cheat = Button_Custom(self.canvas_menu, text=("Triche","black",self.custom_font),command= self.triche)
            Hovertip(bouton_cheat, "Active le mode triche : ajoute 1000 pieces, 1000 ressources, 100 Fantassins et 50 soldats")
            bouton_cheat.place(anchor = tk.NW, relx = 0.1, rely = 0.9)
        
        #creation des widget du sous menu Rapport village
        frame_rapport = tk.Frame(self.canvas_menu,width=300, height=250 )
        frame_rapport.pack_propagate(False)
        scrollbar_y = tk.Scrollbar(frame_rapport, orient=tk.VERTICAL)  
        scrollbar_x = tk.Scrollbar(frame_rapport, orient=tk.HORIZONTAL)  
        self.texte_rapport = tk.Text(frame_rapport, wrap="none",font = self.custom_font,yscrollcommand=scrollbar_y.set,xscrollcommand=scrollbar_x.set )
        scrollbar_y.config(command=self.texte_rapport.yview)      
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.config(command=self.texte_rapport.xview)      
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.texte_rapport.pack(side=tk.LEFT, fill=tk.BOTH)  
        label_intro_rapport_village = tk.Label(self.canvas_menu, textvariable = self.texte_introrapport,font = self.custom_font ,wraplength=300 ,anchor="w" , justify="left",bg="lightgrey",width=35)
        
        #creation des widget du sous menu eglise
        label_intro_eglise = tk.Label(self.canvas_menu, textvariable = self.texte_introeglise,font = self.custom_font,wraplength=280)
        # Variable pour stocker le choix
        self.var_choix = tk.StringVar(value="fertilité")
        frame_radiobutton = tk.Frame(self.canvas_menu)       
        choix1 = tk.Radiobutton(frame_radiobutton, text="Rite de fertilité", font = self.custom_font,variable=self.var_choix, value="fertilité")
        choix1.pack(anchor="w", pady=2, padx=15)
        choix2 = tk.Radiobutton(frame_radiobutton, text="Rite de bonheur",font = self.custom_font, variable=self.var_choix, value="bonheur")
        choix2.pack(anchor="w", pady=2, padx=15)     
        choix3 = tk.Radiobutton(frame_radiobutton, text="Rite de production",font = self.custom_font, variable=self.var_choix, value="production")         
        choix3.pack(anchor="w", pady=2, padx=15)
        

        def changer_rite(*args):
            """
            Change le rite du village selectionné.
            ne srra utiliser que lorsque l'utilisateur sera dans le menu eglise
            
            """  
            image_id = self.id_rectangle_selection
            village = self.dico_village[image_id]            
            village.modifier_rite_egilse(self.var_choix.get()) 
            rite = self.var_choix.get()
            
            if rite == "fertilité":
                effet_rite = "Le village produit 1 habitant par tour"
            elif rite == 'bonheur':
                effet_rite = "Les villageois gagne 1 de bonheur de plus par tour"
            elif rite == 'production':
                effet_rite = "Les villageois produise 20 pourcent de plus par tour"
            else:
                effet_rite = "Erreur : le rite n'existe pas"
                print("Erreur : modifier_eglise() : le rite n'existe pas")
            
            message = f"Bienvenu dans l'égilse de {village.get_nom()}\nUne égilse qui pratique le rite de {rite}\nQui offre les bonus suivant:\n{effet_rite}"           
            self.texte_introeglise.set(message)
            self.affiche_menu(self.widget_menu_joueur,"eglise")

        # Observer les changements sur var_choix
        self.var_choix.trace("w", changer_rite)
        
        
        #creation des widgets pour le sous menu caserne
        label_introcaserne = tk.Label(self.canvas_menu, text = "Bienvenu dans la caserne du village\nici vous pouvez recruter des unitées ou former les unitées que vous avez\n(former une unitées enleverra un villageois au village)",font = self.custom_font,wraplength=280)
        btn_joueur_caserne_former_fantassin = Button_Custom(self.canvas_menu, text=("Former un Villageois  \n    en Fantassin:","black",self.custom_font),valeur1= (self.dico_prix['former_fantassin'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['former_fantassin'][1],"black",self.custom_font),image2= ressource_image,height = 40,command=lambda: self.former_fantassin())
        Hovertip(btn_joueur_caserne_former_fantassin, "Forme un villageois en fantassin en échange de ressources et d'or.\nAttention :Le villageois ne fera plus partie du village")

        btn_joueur_caserne_former_soldat = Button_Custom(self.canvas_menu, text=("Former un Fantassin  \n    en Soldat:","black",self.custom_font),valeur1= (self.dico_prix['former_soldat'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['former_soldat'][1],"black",self.custom_font),image2= ressource_image,height = 40 ,command=lambda: self.former_soldat())
        Hovertip(btn_joueur_caserne_former_soldat, "Améliore un fantassin existant en soldat contre une certaine somme d'argent et de ressource.")

        btn_joueur_caserne_recruter_fantassin = Button_Custom(self.canvas_menu, text=("Recruter un Fantassin:","black",self.custom_font),valeur1= (self.dico_prix['recruter_fantassin'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['recruter_fantassin'][1],"black",self.custom_font),image2= ressource_image,command=lambda: self.recruter_fantassin())
        Hovertip(btn_joueur_caserne_recruter_fantassin, "Recrute directement un fantassin en dépensant une grande somme de ressources et d'or.")
      
        btn_joueur_caserne_recruter_soldat = Button_Custom(self.canvas_menu, text=("Recruter un Soldat:","black",self.custom_font),valeur1= (self.dico_prix['recruter_soldat'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['recruter_soldat'][1],"black",self.custom_font),image2= ressource_image,command=lambda: self.recruter_soldat())
        Hovertip(btn_joueur_caserne_recruter_soldat, "Recrute un soldat entraîné pour un coût très élevé.")

        #Le label qui sert d'introduction a chaque case
        label = tk.Label(self.canvas_menu, textvariable = self.texte,font = self.custom_font,wraplength=280)
        
        #Creation des widgets de rapport de joueur
        label_rapport_joueur = tk.Label(self.canvas_menu, textvariable = self.texte_rapport_joueur,font = self.custom_font ,wraplength=300 ,anchor="w" , justify="left",bg="lightgrey",width=35)

        
        
        
        
        # Création d'un dictionnaire pour stocker les widgets par menu
        """
        chaque proprietaire (Joueur,Ennemi,Neutre) a un dico qui contient en clé le type de menu affichable qui n'est visible que par l'utilisateur.
        Exemple widget_menu_joueur["plaine"] affiche le menu representant une plaine qui appartient au Joueur
        
        chaque clé de dico contient une liste de tuple 
        chaque tuple est de type (widget,condition d'activation,placement,condition d'affichage) avec:
            widget = le type de widget créer,
            condition d'activation = une fonction qui renvoie un triplet de booleen (check_argent,check_ressource,check_final) pour s'avoir si il manque de l'argent, des ressources et s'avoir si au final le bouton est activer(tk.NORMAL) ou non
            placement = un tuple de float (x,y) qui represente le placement ,en % de la taille max du canvas menu, du widget en partant du coin haut gauche du canvas menu (par exemple (0.1,0.1) représente un widget placé a 10% de la largeur et la hauteur total du canvas menu )
            condition d'affichage = une fonction qui renvoie un booleen qui décide de si oui ou non le widget est affiché
        lors de l'affichage la methode affiche_menu() va checker chaque widget et ses conditions et va lui configurer son etat en fonction des resultat obtenu
        Cette structure bien que lourde permet d'eviter d'avoir a faire des if ... elif pour checker chaque bouton possible
        """
        #on créer tout les bouton en avance
        #btn_menu_autre
        btn_autre_taxer_auto = Button_Custom(self.canvas_menu, text=("Taxer tous vos villages","black",self.custom_font),command=lambda: self.taxer_multiple_village())
        Hovertip(btn_autre_taxer_auto, "Collecte automatiquement les taxes de tous vos villages.\nAttention à l'humeur de vos villageois")
        btn_autre_rapport_tour = Button_Custom(self.canvas_menu, text=("Ouvrir le rapport de début de tour","black",self.custom_font),command=lambda: self.creer_fenetre_rapport_debut_tour(self.text_rapport_debut_tour))
        Hovertip(btn_autre_rapport_tour, "Réaffiche le rapport de début de tour.")
        btn_autre_rapport_joueur = Button_Custom(self.canvas_menu, text=("Rapport du Joueur ->","black",self.custom_font),command=lambda: self.affiche_rapport_joueur())
        Hovertip(btn_autre_rapport_joueur, "Affiche le rapport détaillé de l’état du joueur.")

        #bouton menu joueur
        btn_joueur_plaine_creer_village = Button_Custom(self.canvas_menu, text=("Créer un village:","black",self.custom_font),valeur1= (self.dico_prix['creation_village'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['creation_village'][1],"black",self.custom_font),image2= ressource_image,command=lambda: self.creation_village())
        Hovertip(btn_joueur_plaine_creer_village,"Permet de créer un nouveau village en échange de ressources et d'or.\nLe village possède directement 10 villageois à sa création\nNécessite 8 cases libre autour de lui\nLes 8 cases autour des autres villages ne compte pas comme des cases libre")        
        btn_joueur_village_taxer = Button_Custom(self.canvas_menu, text=("Taxer","black",self.custom_font), command=lambda: self.taxer())
        Hovertip(btn_joueur_village_taxer, "Collecte les taxes du village actuel.\nLes Paysans sont taxé pour 1/2 de leurs ressource/argent total.\nLes Artisans sont taxé pour 1/4 de leurs ressource/argent total.\nLes villageois de ce village perdrons 1 d'humeur\nAttention : Si l'humeur d'un villageois passe à 0 il va se revolter")
        btn_joueur_village_festival = Button_Custom(self.canvas_menu, text=("Faire un festival:","black",self.custom_font),valeur1= (self.dico_prix['festival'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['festival'][1],"black",self.custom_font),image2= ressource_image, command=lambda: self.festival())
        Hovertip(btn_joueur_village_festival,"Organise un festival pour améliorer de 1 l'humeur des villageois.")
        
        btn_joueur_village_ajouter_villageois = Button_Custom(self.canvas_menu, text=("Faire venir un villageois:","black",self.custom_font),valeur1= (self.dico_prix['venir_villageois'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['venir_villageois'][1],"black",self.custom_font),image2= ressource_image, command=lambda: self.ajouter_villageois())
        Hovertip(btn_joueur_village_ajouter_villageois, "Fait venir un villageois dans votre village.\nIl y a 1 chance sur 3 que ce soit un Artisant")
        
        btn_joueur_village_creer_egilse = Button_Custom(self.canvas_menu, text=("Créer une égilse:","black",self.custom_font),valeur1= (self.dico_prix['creation_eglise'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['creation_eglise'][1],"black",self.custom_font),image2= ressource_image, command=lambda: self.creer_egilse())
        Hovertip(btn_joueur_village_creer_egilse, "Créer une égilse permet de faire venir un eclésiastique qui offre un bonus au village.")
        
        btn_joueur_village_modifier_egilse = Button_Custom(self.canvas_menu, text=("Modifier l'église ->","black",self.custom_font),cursor='hand2' ,command=lambda: self.modifier_eglise())        
        Hovertip(btn_joueur_village_modifier_egilse, "Permet de changer le bonus qu'offre l'eclésiastique.")
        btn_joueur_village_creer_caserne = Button_Custom(self.canvas_menu, text=("Créer une caserne:","black",self.custom_font),valeur1= (self.dico_prix['creation_caserne'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['creation_caserne'][1],"black",self.custom_font),image2= ressource_image, command=lambda: self.creer_caserne())
        Hovertip(btn_joueur_village_creer_caserne, "Construit une caserne dans le village qui permet de former ou de recruter des unités.")
        btn_joueur_village_entrer_caserne = Button_Custom(self.canvas_menu, text=("Entrer dans la caserne ->","black",self.custom_font),cursor='hand2' ,command=lambda: self.entrer_caserne())       
        btn_joueur_village_rapport = Button_Custom(self.canvas_menu, text=("Rapport des villageois ->","black",self.custom_font),cursor='hand2' ,command=lambda : self.rapport_villageois())
        Hovertip(btn_joueur_village_rapport, "Offre une vue détaillée de tout les villageois dans le village")
        btn_joueur_village_detruire = Button_Custom(self.canvas_menu, text=("Detruire le village","black",self.custom_font), command=lambda: self.confirmation_detruire_village())
        Hovertip(btn_joueur_village_detruire, "Détruit le village actuel. Cette action est irréversible !")

        #bouton menu neutre
        btn_neutre_conquerir = Button_Custom(self.canvas_menu, text=("Conquérir:","black",self.custom_font),valeur1= (self.dico_prix['conquete'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['conquete'][1],"black",self.custom_font),image2= ressource_image, command=lambda: self.conquerir())
        Hovertip(btn_neutre_conquerir, "Conquiert une case neutre et l'ajoute à votre territoire.\nVous ne pouvez conquérire que des cases qui jouxte votre territoire.")

        #bouton menu ennemie
        btn_ennemi_attaque = Button_Custom(self.canvas_menu, text=("Attaquer","black",self.custom_font), command=lambda: self.attaquer())
        Hovertip(btn_ennemi_attaque, "Ouvre la fenêtre de Guerre.\nVous ne pouvez attaquer que des cases qui jouxte votre territoire")

        self.btn_ennemi__village_vassaliser = Button_Custom(self.canvas_menu, text=("vassaliser l'ennemi:","black",self.custom_font),valeur1= (0,"black",self.custom_font),image1 =or_image,valeur2 =(0,"black",self.custom_font),image2= ressource_image ,command=lambda: self.vassaliser()) 
        Hovertip(self.btn_ennemi__village_vassaliser, "Nécessite 2 fois l'argent et les ressources de votre ennemi pour le vassaliser\nUne fois vassaliser, l'ennemi deviendra un vassal qui vous aidera durant vos guerre.\nVous pourrez aussi exiger de lui qu'il vous donne de l'argent ou des ressources.")

        btn_ennemi_rapport_ennemi = Button_Custom(self.canvas_menu, text=("Rapport de l'Ennemi ->","black",self.custom_font),command=lambda: self.affiche_rapport_joueur())
        Hovertip(btn_ennemi_rapport_ennemi, "Affiche le rapport détaillé des ressources et de l’état de l'ennemi.")

        btn_ennemi_liberer_joueur = Button_Custom(self.canvas_menu, text=("Payer pour vous libérer:","black",self.custom_font),valeur1= (self.dico_prix['liberer_joueur'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['liberer_joueur'][1],"black",self.custom_font),image2= ressource_image, command=lambda: self.liberer_joueur()) 
        Hovertip(btn_ennemi_liberer_joueur, "Permet de vous libérer et ainsi de retourner en guerre")

        btn_ennemi_liberer_vassal = Button_Custom(self.canvas_menu, text=("Payer pour libérer votre vassal:","black",self.custom_font),valeur1= (self.dico_prix['liberer_vassal'][0],"black",self.custom_font),image1 =or_image,valeur2 =(self.dico_prix['liberer_vassal'][1],"black",self.custom_font),image2= ressource_image, command=lambda: self.liberer_vassal())
        Hovertip(btn_ennemi_liberer_vassal, "Permet de libérer un vassal pour qu'il puisse retourner se faire capturer à la guerre suivante")

        #bouton menu vassal
        btn_vassal_exiger_argent = Button_Custom(self.canvas_menu, text=("Éxiger 50 argent à votre vassal\n(1 fois par tour)","black",self.custom_font),height = 40, command=lambda: self.exiger_argent()) 
        btn_vassal_exiger_ressource = Button_Custom(self.canvas_menu, text=("Éxiger 50 ressource à votre vassal\n(1 fois par tour)","black",self.custom_font),height = 40, command=lambda: self.exiger_ressource()) 
        btn_vassal_rapport_vassal = Button_Custom(self.canvas_menu, text=("Rapport de Vassal ->","black",self.custom_font),command=lambda: self.affiche_rapport_joueur())
        Hovertip(btn_vassal_rapport_vassal, "Affiche le rapport détaillé des ressources et de l’état de votre vassal.")

        
        btn_retour = Button_Custom(self.canvas_menu, text=("Retour","black",self.custom_font),command = lambda : self.retour_menu())
        
        self.widget_menu_autre = {
            "idle": [
                    (label,None,(0.05,0.05),None),
                    (
                        btn_autre_taxer_auto,
                        None,
                        (0.05,0.3),
                        lambda : self.check_affichage_possede_plusieur_village() # ne s'affiche que si on possede > 1 village
                    ),
                    (
                        btn_autre_rapport_tour,
                        None,
                        (0.05,0.8),
                        lambda : self.check_affichage_rapport_tour() #ne s'affiche qu'au tour +1  
                    ),
                    (btn_autre_rapport_joueur,None,(0.05,0.7),None)
                ],
            "bruler": [
                    (label,None,(0.05,0.05),None)
                ],
            "rapport_joueur": [
                    (label_rapport_joueur,None,(0.05,0.05),None),
                    (btn_retour,None,(0.05,0.76),None)
                ]
            }
        self.widget_menu_joueur = {
            "plaine": [
                (label,None,(0.05,0.05),None),
                (
                    btn_joueur_plaine_creer_village,                 
                    lambda : self.check_condition(self.dico_prix['creation_village'][0],self.dico_prix['creation_village'][1],self.check_creation_village),
                    (0.05,0.2),
                    None
                )
            ],
            "foret": [
                (label,None,(0.05,0.05),None)
            ],
            "montagne": [
                (label,None,(0.05,0.05),None)
            ],
            "lac": [
                (label,None,(0.05,0.05),None)
            ],
            "village": [
                (label,None,(0.05,0.05),None),
                (
                    btn_joueur_village_taxer,
                    None,
                    (0.05,0.20),
                    None                  
                ),
                (
                    btn_joueur_village_festival,
                    lambda : self.check_condition(self.dico_prix['festival'][0],self.dico_prix['festival'][1]),
                    (0.05,0.28),
                    None 
                ),
                (
                    btn_joueur_village_ajouter_villageois,
                    lambda : self.check_condition(self.dico_prix['venir_villageois'][0],self.dico_prix['venir_villageois'][1]),
                    (0.05,0.36),
                    None
                ),
                (
                    btn_joueur_village_creer_egilse,
                    lambda : self.check_condition(self.dico_prix['creation_eglise'][0],self.dico_prix['creation_eglise'][1]),
                    (0.05,0.6),
                    lambda : not self.check_affichage_possede_eglise()   
                ),
                (
                    btn_joueur_village_modifier_egilse,
                    None,
                    (0.05,0.6),
                    lambda : self.check_affichage_possede_eglise()   
                ),
                (
                    btn_joueur_village_creer_caserne,
                    lambda : self.check_condition(self.dico_prix['creation_caserne'][0],self.dico_prix['creation_caserne'][1]),
                    (0.05,0.68),
                    lambda : not self.check_affichage_possede_caserne()   
                ),
                (
                    btn_joueur_village_entrer_caserne,
                    None,
                    (0.05,0.68),
                    lambda : self.check_affichage_possede_caserne()  
                ),
                (
                    btn_joueur_village_rapport,
                    None,
                    (0.05,0.76),
                    None  
                ),
                (
                    btn_joueur_village_detruire,
                    None,
                    (0.5,0.91),
                    None   
                )
            ],
            "rapport": [
                (label_intro_rapport_village,None,(0.05,0.05),None),
                (frame_rapport,None,(0.05,0.25),None),
                (btn_retour,None,(0.05,0.76),None)
                ],
            "eglise": [
                (label_intro_eglise,None,(0.05,0.05),None),
                (frame_radiobutton,None,(0.05,0.3),None),
                (btn_retour,None,(0.05,0.6),None)
                ],
            "caserne": [
                (label_introcaserne,None,(0.05,0.05),None),
                (
                     btn_joueur_caserne_former_fantassin,
                     lambda : self.check_condition(self.dico_prix['former_fantassin'][0],self.dico_prix['former_fantassin'][1],self.check_nb_villageois),
                     (0.05,0.25),
                     None
                ),
                (
                     btn_joueur_caserne_former_soldat,
                     lambda : self.check_condition(self.dico_prix['former_soldat'][0],self.dico_prix['former_soldat'][1],self.check_nb_fantassin),
                     (0.05,0.35),
                     None
                ),
                (
                     btn_joueur_caserne_recruter_fantassin,
                     lambda : self.check_condition(self.dico_prix['recruter_fantassin'][0],self.dico_prix['recruter_fantassin'][1]), 
                     (0.05,0.5),
                     None
                ),
                (
                     btn_joueur_caserne_recruter_soldat,
                     lambda : self.check_condition(self.dico_prix['recruter_soldat'][0],self.dico_prix['recruter_soldat'][1]),
                     (0.05,0.58),
                     None
                ),
                (btn_retour,None,(0.05,0.68),None)               
                ]
        
            }
        #affiche le menu d'une case neutre
        self.widget_menu_neutre = {
            "plaine": [
                (label,None,(0.05,0.05),None),
                (
                    btn_neutre_conquerir,
                    lambda : self.check_condition(self.dico_prix['conquete'][0],self.dico_prix['conquete'][1],self.check_adjacent),
                    (0.05,0.2),
                    None
                )
            ],
            "foret": [
                (label,None,(0.05,0.05),None),
                (
                    btn_neutre_conquerir,
                    lambda : self.check_condition(self.dico_prix['conquete'][0],self.dico_prix['conquete'][1],self.check_adjacent),
                    (0.05,0.2),
                    None
                )
            ],
            "montagne": [
                (label,None,(0.05,0.05),None),
                (
                    btn_neutre_conquerir,
                    lambda : self.check_condition(self.dico_prix['conquete'][0],self.dico_prix['conquete'][1],self.check_adjacent),
                    (0.05,0.2),
                    None
                )
            ],
            "lac": [
                (label,None,(0.05,0.05),None),
                (
                    btn_neutre_conquerir,
                    lambda : self.check_condition(self.dico_prix['conquete'][0],self.dico_prix['conquete'][1],self.check_adjacent),
                    (0.05,0.2),
                    None
                )
            ]
            }
        #affiche le menu d'une case ennemi
        self.widget_menu_ennemi = {
            "plaine": [
                (label,None,(0.05,0.05),None),
                (
                    btn_ennemi_attaque,
                    lambda : self.check_condition(0,5,self.check_adjacent),
                    (0.05,0.15),
                    None
                ),
                (
                    btn_ennemi_liberer_joueur,
                    lambda : self.check_condition(self.dico_prix["liberer_joueur"][0],self.dico_prix["liberer_joueur"][1]), 
                    (0.05,0.3),
                    lambda : self.check_affichage_liberer_joueur()
                ),
                (
                    btn_ennemi_liberer_vassal,
                    lambda : self.check_condition(self.dico_prix["liberer_vassal"][0],self.dico_prix["liberer_vassal"][1]), 
                    (0.05,0.38),
                    lambda : self.check_affichage_liberer_vassal()
                ),
                (btn_ennemi_rapport_ennemi,None,(0.05,0.7),None)
            ],
            "foret": [
                (label,None,(0.05,0.05),None),
                (
                    btn_ennemi_attaque,
                    lambda : self.check_condition(0,5,self.check_adjacent),
                    (0.05,0.15),
                    None
                ),
                (
                    btn_ennemi_liberer_joueur,
                    lambda : self.check_condition(self.dico_prix["liberer_joueur"][0],self.dico_prix["liberer_joueur"][1]), 
                    (0.05,0.3),
                    lambda : self.check_affichage_liberer_joueur()
                ),
                (
                    btn_ennemi_liberer_vassal,
                    lambda : self.check_condition(self.dico_prix["liberer_vassal"][0],self.dico_prix["liberer_vassal"][1]), 
                    (0.05,0.38),
                    lambda : self.check_affichage_liberer_vassal()
                ),
                (btn_ennemi_rapport_ennemi,None,(0.05,0.7),None)
            ],
            "montagne": [
                (label,None,(0.05,0.05),None),
                (
                    btn_ennemi_attaque,
                    lambda : self.check_condition(0,5,self.check_adjacent),
                    (0.05,0.15),
                    None
                ),
                (
                    btn_ennemi_liberer_joueur,
                    lambda : self.check_condition(self.dico_prix["liberer_joueur"][0],self.dico_prix["liberer_joueur"][1]), 
                    (0.05,0.3),
                    lambda : self.check_affichage_liberer_joueur()
                ),
                (
                    btn_ennemi_liberer_vassal,
                    lambda : self.check_condition(self.dico_prix["liberer_vassal"][0],self.dico_prix["liberer_vassal"][1]), 
                    (0.05,0.38),
                    lambda : self.check_affichage_liberer_vassal()
                ),
                (btn_ennemi_rapport_ennemi,None,(0.05,0.7),None)
            ],
            "lac": [
                (label,None,(0.05,0.05),None),
                (
                    btn_ennemi_attaque,
                    lambda : self.check_condition(0,5,self.check_adjacent),
                    (0.05,0.15),
                    None
                ),
                (
                    btn_ennemi_liberer_joueur,
                    lambda : self.check_condition(self.dico_prix["liberer_joueur"][0],self.dico_prix["liberer_joueur"][1]), 
                    (0.05,0.3),
                    lambda : self.check_affichage_liberer_joueur()
                ),
                (
                    btn_ennemi_liberer_vassal,
                    lambda : self.check_condition(self.dico_prix["liberer_vassal"][0],self.dico_prix["liberer_vassal"][1]), 
                    (0.05,0.38),
                    lambda : self.check_affichage_liberer_vassal()
                ),
                (btn_ennemi_rapport_ennemi,None,(0.05,0.7),None)
            ],
            "village": [
                (label,None,(0.05,0.05),None),
                (
                    btn_ennemi_attaque,
                    lambda : self.check_condition(0,5,self.check_adjacent),
                    (0.05,0.15),
                    None
                ),
                (
                    self.btn_ennemi__village_vassaliser,
                    lambda : self.check_condition_vassalisation(),
                    (0.05,0.23),
                    lambda :  self.check_affichage_est_vassal()
                ),
                (
                    btn_ennemi_liberer_joueur,
                    lambda : self.check_condition(self.dico_prix["liberer_joueur"][0],self.dico_prix["liberer_joueur"][1]),
                    (0.05,0.35),
                    lambda : self.check_affichage_liberer_joueur()
                ),
                (
                    btn_ennemi_liberer_vassal,
                    lambda : self.check_condition(self.dico_prix["liberer_vassal"][0],self.dico_prix["liberer_vassal"][1]),
                    (0.05,0.43),
                    lambda : self.check_affichage_liberer_vassal()
                ),
                (btn_ennemi_rapport_ennemi,None,(0.05,0.7),None)
            ]
            }
        self.widget_menu_vassal = {
            "plaine": [
                (label,None,(0.05,0.05),None),
                (
                    btn_vassal_exiger_argent, 
                    lambda : self.check_condition_exiger_argent(), 
                    (0.05,0.2),
                    None
                ),
                (
                    btn_vassal_exiger_ressource, 
                    lambda : self.check_condition_exiger_ressource(), 
                    (0.05,0.32),
                    None
                ),
                (btn_vassal_rapport_vassal,None,(0.05,0.7),None)
            ],
            "foret": [
                (label,None,(0.05,0.05),None),
                (
                    btn_vassal_exiger_argent, 
                    lambda : self.check_condition_exiger_argent(), 
                    (0.05,0.2),
                    None
                ),
                (
                    btn_vassal_exiger_ressource, 
                    lambda : self.check_condition_exiger_ressource(), 
                    (0.05,0.32),
                    None
                ),
                (btn_vassal_rapport_vassal,None,(0.05,0.7),None)
            ],
            "montagne": [
                (label,None,(0.05,0.05),None),
                (
                    btn_vassal_exiger_argent, 
                    lambda : self.check_condition_exiger_argent(), 
                    (0.05,0.2),
                    None
                ),
                (
                    btn_vassal_exiger_ressource, 
                    lambda : self.check_condition_exiger_ressource(), 
                    (0.05,0.32),
                    None
                ),
                (btn_vassal_rapport_vassal,None,(0.05,0.7),None)
            ],
            "lac": [
                (label,None,(0.05,0.05),None),
                (
                    btn_vassal_exiger_argent, 
                    lambda : self.check_condition_exiger_argent(), 
                    (0.05,0.2),
                    None
                ),
                (
                    btn_vassal_exiger_ressource, 
                    lambda : self.check_condition_exiger_ressource(), 
                    (0.05,0.32),
                    None
                ),
                (btn_vassal_rapport_vassal,None,(0.05,0.7),None)
            ],
            "village": [
                (label,None,(0.05,0.05),None),
                (
                    btn_vassal_exiger_argent, 
                    lambda : self.check_condition_exiger_argent(), 
                    (0.05,0.2),
                    None
                ),
                (
                    btn_vassal_exiger_ressource, 
                    lambda : self.check_condition_exiger_ressource(), 
                    (0.05,0.32),
                    None
                ),
                (btn_vassal_rapport_vassal,None,(0.05,0.7),None)
            ]
            }
        self.widget_menu_autre["idle"][0][0].place(anchor = tk.N, relx = 0, rely = 0.1)
        self.menu_actif = (self.widget_menu_autre,"idle")
        self.affiche_menu(self.widget_menu_autre ,"idle")
        
    def triche(self):
        
        joueur = self.dico_joueurs["Joueur"]
        joueur.modifier_argent(1000)
        joueur.modifier_ressource(1000)
        joueur.modifier_fantassin(100)
        joueur.modifier_soldat(50)
        self.barre_menu.update_stats()
        self.barre_menu.update_unite()
        self.affiche_menu()
        
    def update_background(self,path):
        """
        Met à jour les arrière-plans pour correspondre à la taille actuelle des canvas.
        L'image doit toujours etre recalculer au cas ou l'utilisateur change de taille de fenetre
        #TODO ajouter un menu option durant la partie
        """
        
        # Mettre à jour l'image de fond pour canvas_menu
        canvas_menu_width = self.canvas_menu.winfo_width()
        canvas_menu_height = self.canvas_menu.winfo_height()
        resized_menu_image = Image.open(path).resize((canvas_menu_width, canvas_menu_height), Image.Resampling.LANCZOS)
        self.bg_image_menu_tk = ImageTk.PhotoImage(resized_menu_image)  # Référence distincte
        self.id_image_bg_menu = self.canvas_menu.create_image(0, 0, image=self.bg_image_menu_tk, anchor="nw")
        
        # Mettre à jour l'image de fond pour label_menu
        barre_menu_width = self.barre_menu.get_canvas().winfo_width()
        barre_menu_height = self.barre_menu.get_canvas().winfo_height()
        resized_label_image = Image.open("Images/bg/pannel_bg.png").resize((barre_menu_width, barre_menu_height), Image.Resampling.LANCZOS)
        self.bg_image_label_tk = ImageTk.PhotoImage(resized_label_image)  # Référence distincte
        self.barre_menu.get_canvas().create_image(0, 0, image=self.bg_image_label_tk, anchor="nw")
        
        self.barre_menu.update_stats()
        self.barre_menu.update_unite()
        self.barre_menu.update_event("Pas d'évenement")
    

    def affiche_menu(self,var_menu = None,cle_menu = None):
        """
        Affiche le menu spécifié par les paramètres ou correspondant à la sélection de l'utilisateur.
        
        :param var_menu: Le dictionnaire de menus à afficher (optionnel).
        :param cle_menu: La clé du menu dans le dictionnaire (optionnel).
        :return: None
        """
        image_id = self.id_rectangle_selection
        if var_menu != None: #passage des element en manuelle 
            menu = var_menu
            tags = (cle_menu,)
        elif image_id != None: # sinon c'est automatique           
            tags = self.canvas_map.gettags(image_id)            
            if tags[1] == "Joueur":
                menu = self.widget_menu_joueur
            elif tags[1] == "Neutre":
                menu = self.widget_menu_neutre
            elif tags[1] == "Autre":
                menu = self.widget_menu_autre
            elif tags[1][0:6] == "Ennemi":
                #si on se trouve chez un vassal
                if tags[1] in self.dico_joueurs["Joueur"].get_vassal().keys():
                    menu = self.widget_menu_vassal
                else:
                    menu = self.widget_menu_ennemi 
                    #les valeurs pour vassaliser un ennemi étant toujours différente, il faut les calculer dynamiquement.
                    self.btn_ennemi__village_vassaliser.set_valeur(valeur1= (self.dico_prix['vassaliser']()[0],"black",self.custom_font),valeur2 =(self.dico_prix['vassaliser']()[1],"black",self.custom_font))
                    self.btn_ennemi__village_vassaliser.calcul_width()
        else:#sinon c'est que aucun menu n'est selectionner
            menu = self.widget_menu_autre
            tags = ("idle",)
        
            
        self.change_texte()            
        self.cacher_menu(self.menu_actif) 
        for widget,condition,placement,condition_affichage in menu[tags[0]]:
            if condition_affichage != None:
                affichage = condition_affichage()
            else:
                affichage = True
                
            if affichage:
                if condition !=None:
                    possede_argent, possede_ressource, etat = condition()
                    if etat:
                        if widget.winfo_class() == "Label":
                            widget.config(state=tk.NORMAL)
                        else:
                            #les bouton personnalisé on leurs propre méthode pour changer leur état 
                            widget.set_state(tk.NORMAL)
                    else:
                        if widget.winfo_class() == "Label":
                            widget.config(state=tk.DISABLED)
                        else:
                            widget.set_state(tk.DISABLED)
                        if not possede_argent:
                            widget.manque_argent()
                        if not possede_ressource:
                            widget.manque_ressource()
                widget.place(anchor = tk.NW, relx = placement[0], rely = placement[1])
                                                                              
        self.menu_actif = (menu,tags[0])
            
    def cacher_menu(self,menu_actif):
        """
        Cache le menu actuellement afficher
        """
        menu = menu_actif[0]
        type_case = menu_actif[1]
        for widgets in menu[type_case]:
            widgets[0].place_forget()
        return (self.widget_menu_autre ,"idle")
    
    def retour_menu(self):
        """
        Une methode pour mettre la bonne image en bg et afficher le bon menu
        """
        self.bg_menu_actuelle = "bg_menu"
        self.update_background(self.dico_images_bg[self.bg_menu_actuelle])
        self.affiche_menu()
        
    
    
        
    
    def check_condition(self,argent,ressource,autre = None):
        """
        revoie un triplet de booleen qui representent:
            check_argent = si le Joueur a asser d'argent
            check_ressource = la meme
            valeur_bool = le valeur que renvoie la fonction autre qui est juste une condition en plus a respecter
        """
        image_id = self.id_rectangle_selection
        check_argent = self.dico_joueurs["Joueur"].get_argent() >= argent
        check_ressource = self.dico_joueurs["Joueur"].get_ressource() >= ressource
        valeur_bool = True
        if autre != None:
            valeur_bool = autre(image_id)
        valeur_bool = valeur_bool and check_argent and check_ressource
        return(check_argent,check_ressource,valeur_bool)
    
    
    
    def check_condition_exiger_argent(self):
        image_id = self.id_rectangle_selection
        vassal_nom = self.canvas_map.gettags(image_id)[1]
        
        vassal_class = self.dico_joueurs[vassal_nom]
        if vassal_class.get_argent() < 50: #si le vassal n'a pas asser d'argent
            return (False,False,False)
        elif self.dico_vassal_exiger[vassal_nom][0]: #si on a deja exiger argent
            return (True,True,False)
        else:
            return (True,True,True)
    
    def check_condition_exiger_ressource(self):
        image_id = self.id_rectangle_selection
        vassal_nom = self.canvas_map.gettags(image_id)[1]
        
        vassal_class = self.dico_joueurs[vassal_nom]
        if vassal_class.get_ressource() < 50: #si le vassal n'a pas asser de ressource
            return (False,False,False)
        elif self.dico_vassal_exiger[vassal_nom][1]: #si on a deja exiger ressource
            return (True,True,False)
        else:
            return (True,True,True)
    
    def valeur_vassalisation(self):
        """
        utile pour le dico_prix
        renvoie le tuple (argent_ennemi*2,ressource_ennemi*2) qui est le prix de la vassalisation 
        """
        if self.id_rectangle_selection != None:
            image_id = self.id_rectangle_selection
        else:
            return (0,0)
        tags = self.canvas_map.gettags(image_id)
        ennemi = self.dico_joueurs[tags[1]]
        argent_ennemi = ennemi.get_argent()
        ressource_ennemi = ennemi.get_ressource()
        return (argent_ennemi*2,ressource_ennemi*2)
    
    def check_condition_vassalisation(self):
        """
        verifie si le Joueur a 2 fois plus de bien que l'ennemi
        """
        image_id = self.id_rectangle_selection
        tags = self.canvas_map.gettags(image_id)
        ennemi = self.dico_joueurs[tags[1]]
        argent_ennemi = ennemi.get_argent()
        ressource_ennemi = ennemi.get_ressource()
        return self.check_condition(argent_ennemi*2,ressource_ennemi*2) 
    
    def check_nb_villageois(self,image_id):
        """
        Verifie qu'il reste un villageois dans le village
        """
        village = self.dico_village[image_id]
        return len(village.get_villageois()) >= 1
    
    def check_nb_fantassin(self,image_id):
        joueur = self.dico_joueurs[self.joueur_actuelle]
        return joueur.get_fantassin() >= 1
    
    def check_affichage_possede_plusieur_village(self):
        """
        Verifie si le joueur a plus d'un village
        """
        joueur = self.dico_joueurs[self.joueur_actuelle]
        return len(joueur.get_villages()) > 1
    
    def check_affichage_rapport_tour(self):
        return self.nb_de_tour > 0
    
    def check_affichage_possede_eglise(self):
        image_id = self.id_rectangle_selection
        village = self.dico_village[image_id]
        return village.possede_egilse()
    
    def check_affichage_possede_caserne(self):
        image_id = self.id_rectangle_selection
        village = self.dico_village[image_id]
        return village.possede_caserne()
    
    def check_affichage_est_vassal(self):
        image_id = self.id_rectangle_selection
        tags = self.canvas_map.gettags(image_id)
        class_joueur = self.dico_joueurs["Joueur"]
        return class_joueur.get_vassaliser_par() != tags[1]
        
    
    def check_affichage_liberer_joueur(self):
        """Check si l'ennemi qu'on observe a capturé le joueur"""
      
        image_id = self.id_rectangle_selection
        tags = self.canvas_map.gettags(image_id)
        joueur = self.dico_joueurs["Joueur"]
        return joueur.get_capturer_par() == tags[1] #est ce l'ennemi qui a capturer le Joueur
    
    def check_affichage_liberer_vassal(self):
        """Check si l'ennemi qu'on observe a capturé un vassal du joueur"""
      
        image_id = self.id_rectangle_selection
        tags = self.canvas_map.gettags(image_id)
        joueur = self.dico_joueurs["Joueur"]
        list_vassal = list(joueur.get_vassal().values())
        for vassal in list_vassal:
            if vassal.get_capturer_par() == tags[1]:
                return True
        return False
          
    
    def check_adjacent(self, image_id):
        """
        Verifie si une des 4 cases autour de la case selectionner appartient a joueur
        """
        
        coords = self.canvas_map.coords(image_id)
        
        x, y = coords[0], coords[1]
        

        # Calcul des coordonnées des images adjacentes (haut, bas, gauche, droite)
        adjacent_coords = [
            (x, y - self.taille_image), 
            (x, y + self.taille_image),  
            (x - self.taille_image, y), 
            (x + self.taille_image, y)  
        ]
        
        # Vérifier chaque position adjacente
        for adj_x, adj_y in adjacent_coords:
            if 0<= adj_x < self.taille_image*self.taille_map and 0<= adj_y < self.taille_image*self.taille_map:
                # Chercher si une image existe à cette position
                overlapping_items = self.canvas_map.find_overlapping(adj_x, adj_y, adj_x + self.taille_image, adj_y + self.taille_image)
                
                # Vérifier si une image existe et si son tag est "Joueur"
                for item in overlapping_items:
                    if self.joueur_actuelle in self.canvas_map.gettags(item):
                        return True  # Trouvé un voisin avec le tag joueur_actuelle
        
        return False  # Aucun voisin avec le tag joueur_actuelle trouvé
    
    def check_creation_village(self, image_id):
        """
        Renvoie True si on peut créer un village sur cette case
        verifie si la case sur laquelle on a cliquer est valide pour construire un village:
            -pas sur les bord de la map
            -les case 8x8 autour du village sont a nous
            -pas a moins de deux case d'un autre village
            -(seuleument sur une plaine)bouton seuleument dispo si on est sur une plaine
        """
        coords = self.canvas_map.coords(image_id)
        
        # Extraire les coordonnées x, y de l'image
        x, y = coords[0], coords[1]
        #on verifie si on est sur un bord
        if x-1<0 or x+self.taille_image >= self.taille_map*self.taille_image or y-1<0 or y+self.taille_image >= self.taille_map*self.taille_image:
            return False
        #on verifie si les 8 cases du village sont a nous
        overlapping_items = self.canvas_map.find_overlapping(x-self.taille_image,y-self.taille_image,x+2*self.taille_image,y+2*self.taille_image)
        for item in overlapping_items:
            if item <= self.taille_map*self.taille_map and self.joueur_actuelle not in self.canvas_map.gettags(item):
                return False
        
        #on verifie si il y'a un village a deux case de proximité
        overlapping_items = self.canvas_map.find_overlapping(x-2*self.taille_image,y-2*self.taille_image,x+3*self.taille_image,y+3*self.taille_image)
        i = 0
        n = len(overlapping_items)
        while i<n and "village" not in self.canvas_map.gettags(overlapping_items[i]):
            i += 1
        
        #on verifie si toute les case on ete checker sinon il y'a une case village
        return i==n

        
    
    def creation_village(self,image_id = None):
        """
        Retire les ressources au joueur et modifie la case
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        #on modifie les ressource + argent du joueur actuelle
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['creation_village'][1]))
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['creation_village'][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        self.canvas_map.dtag(image_id)
        tags = self.canvas_map.gettags(image_id)
        self.canvas_map.itemconfig(image_id, tags = ("village",tags[1]))
        self.canvas_map.itemconfig(image_id, image=self.images_tk['village'])
        village = self.initialisation_village(image_id,10)
        self.dico_joueurs[self.joueur_actuelle].ajouter_village(image_id,village)
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu()
        
        
    def confirmation_detruire_village(self):
        """
        ouvre une messagebox pour confirmer la destruction du village
        """
        image_id = self.id_rectangle_selection
        response = messagebox.askquestion(title="Destruction du village ?", message="Les ressources et les habitants de ce village serons offert en offrande aux Dieux et vous ne recupèrerer rien. Êtes-vous sûr de vouloir détruire ce village ?")
        if response == 'yes':  # Vérifie explicitement si la réponse est 'yes'
            self.detruire_village(image_id)
        
    def detruire_village(self,image_id = None,joueur = None):
        """
        Retire les ressources au joueur et modifie la case
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        tags = self.canvas_map.gettags(image_id)
        
        self.canvas_map.dtag(image_id)        
        if tags[1] == "Autre":
            #un village bruler devient une case neutre
            tags = ("plaine","Neutre")
        #changement de case et d'image sur la map
        self.canvas_map.itemconfig(image_id, tags = ("plaine",tags[1]))
        self.canvas_map.itemconfig(image_id, image=self.images_tk[f'plaine_{tags[1]}'])
        if joueur == None:
            #destruction du village chez le joueur propriétaire
            joueur_nom = tags[1]
            joueur_class = self.dico_joueurs[tags[1]]
            joueur = (joueur_nom,joueur_class)
        else:
            joueur_nom,joueur_class = joueur
        joueur_class.detruire_village(image_id)
        #destruction du village dans le dico principale 
        del self.dico_village[image_id]

        if len(joueur_class.get_villages()) == 0: #si le joueur n'a plus de village
            self.detruire_joueur(joueur)
        self.affiche_menu()
        
    def detruire_joueur(self,joueur_mort):
        """
        On enleve le joueur du dico des joueur,
        On suprime son territoire de la carte
        et on verifie si c'est la fin de partie
        """
        joueur_mort_nom,joueur_mort_class = joueur_mort
        if joueur_mort_nom == "Joueur":
            self.fin_du_jeux = True
            self.fin_de_partie(("aucun","aucun"),"destruction")
        else:
            joueur_nom = joueur_mort_class.get_vassaliser_par() #si le joueur mort était vassal de qlq
            if joueur_nom != False:
                joueur_class = self.dico_joueurs[joueur_nom]
                joueur_class.supprimer_vassal(joueur_mort_nom) #on le supprime de la liste des vassaux
            
            list_joueur = list(self.dico_joueurs.items())
            for joueur_nom,joueur_class in list_joueur:
                if joueur_class.get_capturer_par() == joueur_mort_nom: #si le joueur mort avais des captif
                    joueur_class.modifier_chevalier(1) #le noble recupere son chevalier
                    joueur_class.capturer_par(None)
            
            
            fief_joueur_mort = self.canvas_map.find_withtag(f"{joueur_mort_nom}")
            for image_id in fief_joueur_mort:
                tags = self.canvas_map.gettags(image_id)          
                self.canvas_map.dtag(image_id)        
                self.canvas_map.itemconfig(image_id, tags = (tags[0],"Neutre")) #tout le fief du joeur mort devent neutre
                self.canvas_map.itemconfig(image_id, image=self.images_tk[f'{tags[0]}_Neutre'])
            
            del joueur_mort_class
            del self.dico_joueurs[joueur_mort_nom]
            
            if len(self.dico_joueurs) == 1:
                joueur = list(self.dico_joueurs.items())[0]
                self.fin_du_jeux = True
                self.fin_de_partie(joueur,"conquete")
            else:
            
                for joueur in self.dico_joueurs.items():
                    if len(joueur[1].get_vassal()) == (len(self.dico_joueurs)-1): #si le joueur a vassaliser tout les monde
                        self.fin_du_jeux = True
                        self.fin_de_partie(joueur,"vassaliser")
            
            
            
    
        
        
    
    def initialisation_village(self,image_id, nb_habitant):    
        """
        Créer un village avec nb_habitant choisi au hasard
        """    
        prod = 0
        # Récupérer les coordonnées de l'image (image_id) sur le canvas 
        coords = self.canvas_map.coords(image_id)
        
        if not coords:
            print("L'image n'a pas de coordonnées valides.")
            return False

        # Extraire les coordonnées x, y de l'image
        x, y = coords[0], coords[1]

        # Calcul des coordonnées des images adjacentes    
        overlapping_items = self.canvas_map.find_overlapping(x-self.taille_image,y-self.taille_image,x+2*self.taille_image,y+2*self.taille_image)
        for item in overlapping_items:
            if item <= self.taille_map*self.taille_map:#si l'image se trouve dans la matrice(donc pas le rectangle de selection)
                prod += self.dico_valeur[self.canvas_map.gettags(item)[0]]
                        
        #crée un village avec la bonne production
        self.dico_village[image_id] = GestionClass.Village(prod)
        #lui ajouter x habitant
        for i in range(nb_habitant):          
            choix = rd.choices(["Artisan", "Paysan"],[1,2])[0] #chois de soit Artisans avec une probabilité de 1/3 soit Paysans avec une probabilité de 2/3
            self.dico_village[image_id].ajouter_villageois(choix)
        return self.dico_village[image_id]
    
    def conquerir(self,image_id = None):
        """
        Ajoute la cases selectionnée au territoire du joueur
        """
        if image_id == None:
            image_id = self.id_rectangle_selection

        #on modifie les ressource + argent du joueur actuelle
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix["conquete"][1]))
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix["conquete"][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        self.canvas_map.dtag(image_id)
        tags = self.canvas_map.gettags(image_id)
        self.canvas_map.itemconfig(image_id, tags = (tags[0],self.joueur_actuelle))
        self.canvas_map.itemconfig(image_id, image=self.images_tk[f'{tags[0]}_{self.joueur_actuelle}'])
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu()
 
        
    def attaquer(self,image_id = None,list_revolte = None):
        """
        list_revolte = (class_village,dico_revolte):           
            class_village = l'instance du village en revolte
            dico_revolte = l'indice du villageois dans la list_villageois de son village en cle (permet de le supprimer plus tard) 
                           l'instance du villageois
        
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        tags = self.canvas_map.gettags(image_id)
        if list_revolte != None:
            resultat_guerre = self.Guerre.selection_type_guerre(self.joueur_actuelle,list_revolte[0],list_revolte[1])
        else:
            resultat_guerre = self.Guerre.selection_type_guerre(self.joueur_actuelle,tags[1])
        #Apres a guerre on update la map en fonction du rapport_guerre et resultat_guerre
        self.consequance_attaque(image_id,resultat_guerre,list_revolte )
        
        
    def consequance_attaque(self,image_id,resultat_guerre,list_revolte):
        """
        Est appellée apres une attaque, permet de gerer les actions sur la map apres une attaque 
        """
        tags = self.canvas_map.gettags(image_id)
        if list_revolte != None:
            if not resultat_guerre:
                self.detruire_village(image_id) #on detruit le village
                self.canvas_map.dtag(image_id)
                self.canvas_map.itemconfig(image_id, tags = ("plaine","Neutre"))
                self.canvas_map.itemconfig(image_id, image=self.images_tk['plaine_Neutre']) #la case devient une plaine au joueur
                
        else:
            if resultat_guerre:
                if tags[0] != "village": 
                    self.canvas_map.dtag(image_id)
                    tags = self.canvas_map.gettags(image_id)
                    self.canvas_map.itemconfig(image_id, tags = (tags[0],self.joueur_actuelle))
                    self.canvas_map.itemconfig(image_id, image=self.images_tk[f'{tags[0]}_{self.joueur_actuelle}'])
                    
                else:
                    self.detruire_village(image_id) #on detruit le village
                    self.canvas_map.dtag(image_id)
                    self.canvas_map.itemconfig(image_id, tags = ("plaine",self.joueur_actuelle))
                    self.canvas_map.itemconfig(image_id, image=self.images_tk[f'plaine_{self.joueur_actuelle}']) #la case devient une plaine au joueur
                    
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu()
        
    
    
    def taxer_multiple_village(self):
        # TODO: /!\ bug si multiple revolte et qu'un village est détruit car joueur.get_villages change
        joueur = self.dico_joueurs[self.joueur_actuelle]
        self.valeur_tax = [0,0]
        #bug semble etre resolut si on passe une copie de la liste pour eviter la modification
        for id_village in list(joueur.get_villages()):
            self.taxer(id_village,True)
        if self.tour_joueur:
            self.afficher_notification(f"{self.valeur_tax[0]} argent ,{self.valeur_tax[1]} ressource",0.3)
        

    def taxer(self,image_id = None,multi_taxe = False):
        """
        
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        village = self.dico_village[image_id]
        impot = village.impot()
        #on rajoute l'impot au joueur actuelle 
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(impot[0])
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(impot[1])
        #on update le barre menu
        self.barre_menu.update_stats()
        
        if self.joueur_actuelle == "Joueur":
            if not multi_taxe:
                if self.tour_joueur:
                    self.afficher_notification(f"{impot[0]} argent ,{impot[1]} ressource",0.20)
                
            self.valeur_tax[0] += impot[0]
            self.valeur_tax[1] += impot[1]
            self.affiche_menu()
        revolte , dico_revolte = village.get_revolte_village()
        if revolte:
            self.attaquer(image_id,(village,dico_revolte))
            
    
    def ajouter_villageois(self,image_id = None,eglise=False):
        """
        Ajoute un villageois de type aleatoire au village selectionner
        """
        
        #Faire apparaitre une notif
        if image_id == None:
            image_id = self.id_rectangle_selection
        #on modifie les ressource + argent du joueur actuelle
        if not eglise:
            self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['venir_villageois'][1]))
            self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['venir_villageois'][0]))
            #on update le barre menu
            self.barre_menu.update_stats()
        
        
        village = self.dico_village[image_id]
        
        choix = rd.choices(["Artisan", "Paysan"],[1,2])[0] #chois de soit Artisans avec une probabilité de 1/3 soit Paysans avec une probabilité de 2/3
        village.ajouter_villageois(choix)
        if self.joueur_actuelle == "Joueur":
            if self.tour_joueur:
                self.afficher_notification(f"Un {choix} est arrivé",0.36)
                self.affiche_menu(self.widget_menu_joueur,self.menu_actif[1])
    
    def afficher_notification(self, texte,y):
        """
        Affiche une notification temporaire sur le canvas_map .
        /!\  si une autre notification est apellée, elle disparaitera apres les 2s de la premiere
        /!\  les notification reste figé sur la map durant leur 2s d'apparition'

        """
        # Calcul des dimensions du canvas
        canvas_width = self.canvas_map.winfo_width()
        canvas_height = self.canvas_map.winfo_height()
    
    
        x = canvas_width - 10  
        y = canvas_height / (1/y) + 20 
    
        # Ajouter un rectangle en arrière-plan pour la notification
        self.canvas_map.create_rectangle(
            x - 180, y - 20, x, y + 20,
            fill="lightgrey",
            tags="notification"
        )
        # Ajouter le texte au-dessus du rectangle
        self.canvas_map.create_text(
            x - 90, y, 
            text=texte, fill="black", font=self.custom_font, tags="notification", anchor="center"
        )
        
        # Supprimer la notification après 2 secondes
        self.canvas_map.after(2000, lambda: self.canvas_map.delete("notification"))
        
        
    def rapport_villageois(self):
        self.update_rapport_villageois()
        self.bg_menu_actuelle = "bg_village"
        self.update_background(self.dico_images_bg[self.bg_menu_actuelle])
        self.affiche_menu(self.widget_menu_joueur,"rapport")
        
    def update_rapport_villageois(self):
        """
        créé son propre menu pour afficher ses widgets
        """
        image_id = self.id_rectangle_selection
        village = self.dico_village[image_id]
        
        self.texte_rapport.configure(font=("Courier",12))
        humeurtotal = 0
        nbvillageois = len(village.get_villageois())
        
        message = '{:<12} {:<12} {:<10} {:<8} {:<10} {:<6} {:<6} {:<6}\n'.format(
               'Nom', 'Statut', 'Humeur', 'Argent', 'Ressource', 'CDP', 'Age', 'EDV'
        )
        
        # Données des villageois
        for villageois in village.get_villageois():
            humeurtotal += villageois.get_humeur()
            message += '{:<12} {:<12} {:<10} {:<8} {:<10} {:<6} {:<6} {:<6}\n'.format(
                villageois.get_nom(),
                villageois.get_statut(),
                villageois.get_humeur(),
                villageois.get_argent(),
                villageois.get_ressource(),
                villageois.get_cdp(),
                villageois.get_age(),
                villageois.get_edv()
            )
            
        if nbvillageois != 0:
            humeurmoyen = round(humeurtotal/nbvillageois,2)
        else:
            humeurmoyen = 0
        self.texte_rapport.config(state="normal")
        self.texte_rapport.delete(1.0, tk.END)  # Effacer l'ancien contenu
        self.texte_rapport.insert(tk.END, message,"lightgrey")  # Ajouter le nouveau texte
        self.texte_rapport.config(state="disabled")
        txt_intro = f"Village:{village.get_nom()}\n Nb habitant: {nbvillageois}\n Humeur moyenne: {humeurmoyen}"
        
        self.texte_introrapport.set(txt_intro)
               
        
    def festival(self,image_id = None):
        """
        contre x ressources + argent
        augmente l'humeur de tout les villageois de 1 dans le village selectionner
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        #on modifie les ressource + argent du joueur actuelle
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['festival'][1]))
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['festival'][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        
        village = self.dico_village[image_id]
        #on apelle la methode festival du village
        village.festival()
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu()
        
    def creer_egilse(self,image_id = None, rite = None):
        """
        Creer une eglise dans le village avec le rite de base 'fertilité'
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        village = self.dico_village[image_id] 
                #on modifie les ressource + argent du joueur actuelle
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['creation_eglise'][1]))
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['creation_eglise'][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        if rite == None:
            rite = "fertilité"
        village.creer_eglise(rite) #créer une égilse avec un rite
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu()
    
    def modifier_eglise(self):
        """Ouvre un sous menu dans le village qui donne des info sur l'eglise du village"""
        image_id = self.id_rectangle_selection
        village = self.dico_village[image_id]    
        rite = village.get_rite_egilse()
        self.var_choix.set(rite)
        
        if rite == "fertilité":
            effet_rite = "Le village produit 1 habitant par tour"
        elif rite == 'bonheur':
            effet_rite = "Les villageois gagne 1 de bonheur de plus par tour"
        elif rite == 'production':
            effet_rite = "Les villageois produise 20% de plus par tour"
        else:
            effet_rite = "Erreur : le rite n'existe pas"
            print("Erreur : modifier_eglise() : le rite n'existe pas")
        
        message = f"Bienvenu dans l'égilse de {village.get_nom()}\nUne égilse qui pratique le rite de {rite}\nQui offre les bonus suivant:\n{effet_rite}"
        
        self.texte_introeglise.set(message)
        self.bg_menu_actuelle = "bg_eglise"
        self.update_background(self.dico_images_bg[self.bg_menu_actuelle])
        
        self.affiche_menu(self.widget_menu_joueur,"eglise")
    
    def affiche_rapport_joueur(self):
        """
        Affiche un sous menu avec les inforamtion du joueur selectionner
        """
        image_id = self.id_rectangle_selection
        if image_id != None:
            tags = self.canvas_map.gettags(image_id)
            joueur_nom = tags[1]
        else:
            joueur_nom = "Joueur"
        joueur_class = self.dico_joueurs[joueur_nom]
        message = ""
        message += f"Voici {joueur_class.get_nom()}\n\n"
        if joueur_nom == "Joueur":
            message += "C'est vous\n\n"
        elif joueur_nom in self.dico_joueurs["Joueur"].get_vassal():
            message += "C'est votre Vassal\n\n"
        else:
            message += f"C'est votre Ennemi n°{joueur_nom[-1]}\n\n"
            
        message+= f"Richesse : {joueur_class.get_argent()}\nRessource : {joueur_class.get_ressource()}\n\n"
        
        message += f"Unités :\n\
            {joueur_class.get_fantassin()} fantassin dont {joueur_class.get_fantassin_en_attente()} en attente\n\
            {joueur_class.get_soldat()} fantassin dont {joueur_class.get_soldat_en_attente()} en attente\n\n"
        
        if joueur_class.get_vassaliser_par():
            suzerain = self.dico_joueurs[joueur_class.get_vassaliser_par()].get_nom()
            message += f"Il est le vassal de {suzerain}\n"
        
        if len(joueur_class.get_vassal())> 0:
            message += "Il a pour vassal :\n"
            vassal_class = joueur_class.get_vassal().values()
            for vassal in vassal_class:
                message += f"  {vassal.get_nom()}\n"

        if joueur_class.get_capturer_par():
            message += f"Il est actuellement capturé par :\n  {joueur_class.get_capturer_par()}\n\n"                          
        self.texte_rapport_joueur.set(message)
        self.affiche_menu(self.widget_menu_autre,"rapport_joueur")
    
    def creer_caserne(self,image_id = None):
        """
        Creer une caserne dans le village 
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        village = self.dico_village[image_id] 
                #on modifie les ressource + argent du joueur actuelle
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['creation_caserne'][1]))
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['creation_caserne'][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        village.creer_caserne()
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu()
    
    def entrer_caserne(self):
        self.bg_menu_actuelle = "bg_caserne"
        self.update_background(self.dico_images_bg[self.bg_menu_actuelle])
        self.affiche_menu(self.widget_menu_joueur,"caserne")
        
    def former_fantassin(self,image_id = None):
        """
        convertie un villageois du village selectionner en fantassin prend 1 tour
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['former_fantassin'][1])) 
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['former_fantassin'][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        
        village = self.dico_village[image_id] 
        liste_villageois = village.get_villageois()
        indice = rd.randint(0, len(liste_villageois) - 1)
        village.tuer_villageois(liste_villageois[indice],indice)
        
        joueur = self.dico_joueurs[self.joueur_actuelle]
        joueur.modifier_fantassin_en_attente(1)
        self.barre_menu.update_unite()
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu(self.widget_menu_joueur,"caserne")
        
    
    def former_soldat(self,image_id = None):
        """
        convertie un fantassin  en soldat prend 1 tour
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['former_soldat'][1])) 
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['former_soldat'][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        joueur = self.dico_joueurs[self.joueur_actuelle]
        joueur.modifier_fantassin(-1)
        joueur.modifier_soldat_en_attente(1)
        self.barre_menu.update_unite()
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu(self.widget_menu_joueur,"caserne")
        
    
    def recruter_fantassin(self):
        """
        Pour un plus grand cout donne un fantassin directment 
        """
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['recruter_fantassin'][1]))
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['recruter_fantassin'][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        
        joueur = self.dico_joueurs[self.joueur_actuelle]
        joueur.modifier_fantassin(1)
        self.barre_menu.update_unite()
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu(self.widget_menu_joueur,"caserne")
        
    
    def recruter_soldat(self):
        """
        Pour un plus grand cout donne un soldat directment 
        """
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix['recruter_soldat'][1])) 
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix['recruter_soldat'][0]))
        #on update le barre menu
        self.barre_menu.update_stats()
        
        joueur = self.dico_joueurs[self.joueur_actuelle]
        joueur.modifier_soldat(1)
        self.barre_menu.update_unite()
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu(self.widget_menu_joueur,"caserne")
        
      
        
    def vassaliser(self,joueur1 = None,joueur2 = None, event = False):
        """
        Contre 2* l'argent et les ressource de l'ennemi , vous pouvez le vassaliser.
        
        """    
        if joueur1 == None:
            image_id = self.id_rectangle_selection
            joueur1 = (self.joueur_actuelle,self.dico_joueurs[self.joueur_actuelle])
            tags = self.canvas_map.gettags(image_id)
            nom_vassal = tags[1]
            class_vassal = self.dico_joueurs[nom_vassal]
        else:
            nom_vassal,class_vassal = joueur2
            
            
        joueur1[1].ajouter_vassal(nom_vassal,class_vassal)
        if class_vassal.get_vassaliser_par() != False: #si l'ennemi est deja vassaliser
            ennemi = self.dico_joueurs[class_vassal.get_vassaliser_par()]
            ennemi.supprimer_vassal(nom_vassal) #on vole le vassal a l'ennemi
            
        class_vassal.vassaliser_par(joueur1[0])
        
        if joueur1[1].get_capturer_par() == nom_vassal: #si on vassalise un joueur qui nous a capturer on est automatiquement liberer
            joueur1[1].capturer_par(None)
            joueur1[1].modifier_chevalier(1)
        #pour faciliter de programmation, on dit que quand on se fait vassaliser, on garde ses vassaux  
        if not event:       
            argent_requis = class_vassal.get_argent()
            ressource_requis = class_vassal.get_ressource()
            #les ressources vont dans le neant pour eviter des boucle de vassalisation
            self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(ressource_requis*2))
            self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(argent_requis*2))
            self.barre_menu.update_stats()
        
        if len(joueur1[1].get_vassal()) == (len(self.dico_joueurs)-1): #si le joueur a vassaliser tout les monde
            if event:
                self.fin_du_jeux = True
                self.fin_de_partie(joueur1,"event")
            else:
                self.fin_du_jeux = True
                self.fin_de_partie(joueur1,"vassaliser")
        self.barre_menu.update_unite()
        if not self.fin_du_jeux:
            self.affiche_menu()
        
    def exiger_argent(self,image_id = None):
        """
        Vole 50 argent a votre vassal utilisable 1 seul fois par tour
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(50)
        
        tags = self.canvas_map.gettags(image_id)
        vassal_class = self.dico_joueurs[tags[1]]
        vassal_class.modifier_argent(-50)
        self.barre_menu.update_stats()
        self.dico_vassal_exiger[tags[1]][0] = True
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu()
    
    def exiger_ressource(self,image_id = None):
        """
        Vole 50 argent a votre vassal utilisable 1 seul fois par tour
        """
        if image_id == None:
            image_id = self.id_rectangle_selection
        
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(50)
        
        tags = self.canvas_map.gettags(image_id)
        vassal_class = self.dico_joueurs[tags[1]]
        vassal_class.modifier_ressource(-50)
        self.barre_menu.update_stats()
        self.dico_vassal_exiger[tags[1]][1] = True
        if self.joueur_actuelle == "Joueur":
            self.affiche_menu()
    
    def liberer_joueur(self):
        """
        Lorsque que le chevalier(Le noble) est capturé, Libere le joueur
        """
        
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix["liberer_joueur"][1]))
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix["liberer_joueur"][0]))
        self.barre_menu.update_stats()
        
        joueur = self.dico_joueurs[self.joueur_actuelle]
        #l'ennemi reçois la recompence
        ennemi_nom =  joueur.get_capturer_par()
        ennemi_class = self.dico_joueurs[ennemi_nom]
        ennemi_class.modifier_ressource((self.dico_prix["liberer_joueur"][1]))
        ennemi_class.modifier_argent((self.dico_prix["liberer_joueur"][0]))
        
        joueur.modifier_chevalier(1)
        
        joueur.capturer_par(None)
        self.barre_menu.update_unite()
        self.affiche_menu()
    
    def liberer_vassal(self):
        """
        Libere un vassal capturé (le premier vassal capturer dans votre liste de vassaux)
        """
        self.dico_joueurs[self.joueur_actuelle].modifier_ressource(-(self.dico_prix["liberer_vassal"][1])) 
        self.dico_joueurs[self.joueur_actuelle].modifier_argent(-(self.dico_prix["liberer_vassal"][0]))
        self.barre_menu.update_stats()
        joueur = self.dico_joueurs[self.joueur_actuelle]
        list_vassal = list(joueur.get_vassal().values())
        print("Vos vassaux",list_vassal)
        for vassal in list_vassal:
            if vassal.get_capturer_par() != None: #on verifie que ce soit un vassal capturer
                print("il c'est fait capturer par",vassal.get_capturer_par())
                vassal.modifier_chevalier(1)
                #l'ennemi reçois la recompence
                ennemi_nom =  vassal.get_capturer_par()
                ennemi_class = self.dico_joueurs[ennemi_nom]
                ennemi_class.modifier_ressource((self.dico_prix["liberer_vassal"][1]))
                ennemi_class.modifier_argent((self.dico_prix["liberer_vassal"][0]))              
                vassal.capturer_par(None)
        self.barre_menu.update_unite()
        self.affiche_menu()
    

    
                
    def change_texte(self):
        """
        Modifie le texte de presentation des case 
        """
        image_id = self.id_rectangle_selection
        if image_id != None:
            tags = self.canvas_map.gettags(image_id)
            type_case, appartenance = tags[0:2]
            if tags[1] == "Autre":               
                if type_case == "bruler":
                    message = "Le village a été pris dans un terrible incendie et sera detruit au prochain tour."
            else:
                # Définition des descriptions pour chaque type d'appartenance
                descriptions_appartenance = {
                    "Joueur": "qui vous appartient",
                    "Neutre": "qui n'appartient à personne",
                    
                }
                class_Joueur = self.dico_joueurs["Joueur"]
                for nom,classe in self.dico_joueurs.items():
                    if nom != "Joueur":
                        descriptions_appartenance[nom] = f"appartenant à {classe.get_nom()}"
                        if class_Joueur.get_vassaliser_par() == nom:
                            descriptions_appartenance[nom] += "\nVotre suzerain"
                        if classe.get_vassaliser_par() == "Joueur":
                            descriptions_appartenance[nom] += "\nVotre vassal"
                        
                
                
                if type_case == "village":           
                    nom_village = self.dico_village[image_id].get_nom()
                    
                    message = f"Bienvenue à {nom_village}, un village {descriptions_appartenance[appartenance]}."
                    
                else:
                    # Définition des descriptions pour chaque type de terrain
                    descriptions_type = {
                        "plaine": "une plaine",
                        "foret": "une forêt",
                        "montagne": "une montagne",
                        "lac": "un lac",
                        "village": "un village"
                    }
                
                    message = f"Vous êtes sur {descriptions_type[type_case]} {descriptions_appartenance[appartenance]}."
        else:
            message = "Pour gagner, vous devez soit:\n\n -Vassaliser tous les autres Noble.\n\n -Détruire tous les villages des autres Noble"
        self.texte.set(message)
   
        
   
    
    def creer_fenetre_bloquante_ordre_tour(self):
        """
        cette fenetre sert d'indicateur lorsque les IA joue leur tour (C'était chiant a centré):
            elle indique l'ordre de jeux du tour
            elle indique qui joue actuellement 
        
        "/!\" #TODO les tour d'IA sont tellement rapide que la fenetre n'a pas le temps de s'afficher:
            soit on force les tour d'IA a durée +1seconde (ralentit le jeux pour rien)
            soit on laisse la fenetre telle qu'elle est et elle a le merite d'exister
        """
        
        self.fenetre_bloquante_tour.set(f"Ordre du tour = {self.tour_jeux}  Si cette fenetre ne bouge pas il y'a un probleme")
        nom_joueur = self.dico_joueurs[f"{self.joueur_actuelle}"].get_nom()
        self.fenetre_bloquante_joueur.set(f"Au tour de {nom_joueur}")
        if self.fenetre_bloquante is None:
            fenetre_bloquante = tk.Toplevel(self.root)
            self.fenetre_bloquante = fenetre_bloquante
            fenetre_bloquante.title("Fenêtre Bloquante")
            # Récupérer la taille et la position de la fenêtre principale
            main_window_x = self.root.winfo_rootx()  
            main_window_y = self.root.winfo_rooty() 
            main_window_width = self.root.winfo_width()  
            main_window_height = self.root.winfo_height()  
        
            # Calculer la position pour centrer la fenêtre bloquante par rapport à la fenêtre principale
            x_position = main_window_x + (main_window_width - 400) // 2  # 400 est la largeur de la fenêtre bloquante
            y_position = main_window_y + (main_window_height - 300) // 2  # 300 est la hauteur de la fenêtre bloquante
        
            # Appliquer la position à la fenêtre bloquante
            fenetre_bloquante.geometry(f"400x300+{x_position}+{y_position}")
            # Désactiver les interactions avec la fenêtre principale
            fenetre_bloquante.grab_set()
    
            # Contenu de la fenêtre
            label_tour = tk.Label(self.fenetre_bloquante, textvariable = self.fenetre_bloquante_tour)
            label_tour.pack(padx=20, pady=20)
            label_joueur = tk.Label(self.fenetre_bloquante, textvariable = self.fenetre_bloquante_joueur)
            
            label_joueur.pack(padx=20, pady=20)
    
            # Optionnel : Bouton de test pour fermer
            close_button = tk.Button(self.fenetre_bloquante, text="Fermer", command=self.fermer_fenetre_bloquante_ordre_tour)
            close_button.pack(pady=10)
            
            # Désactiver la fermeture par la croix
            fenetre_bloquante.protocol("WM_DELETE_WINDOW", lambda: None)  # Ne fait rien


    def fermer_fenetre_bloquante_ordre_tour(self):
        """Ferme la fenêtre bloquante si elle existe."""
        if self.fenetre_bloquante is not None:
            self.fenetre_bloquante.destroy()
            self.fenetre_bloquante = None  # Réinitialiser la référence
            
    def creer_fenetre_rapport_debut_tour(self,texte_formate):
        """
        Creer la fenetre qui fait le rapport de debut de tour du Joueur,
        Possede un label qui sert a savoir l'évenement en cours et ses consequences 
        Possede un text qui correspond aux actions de chaque ennemis avant que le joueur n'ai jouer
        """
        fenetre_rapport_debut_tour = tk.Toplevel(self.root)
        fenetre_rapport_debut_tour.title("Rapport de debut de tour")
        fenetre_rapport_debut_tour.grab_set()
        fenetre_rapport_debut_tour.resizable(False, False)
        
        # Récupérer la taille et la position de la fenêtre principale
        fenetre_principale_x = self.root.winfo_rootx()  
        fenetre_principale_y = self.root.winfo_rooty() 
        fenetre_principale_width = self.root.winfo_width()  
        fenetre_principale_height = self.root.winfo_height()  
    
        # Calculer la position pour centrer la fenêtre bloquante par rapport à la fenêtre principale
        x_position = fenetre_principale_x + (fenetre_principale_width - 700) // 2  
        y_position = fenetre_principale_y + (fenetre_principale_height - 500) // 2  
    
        # Appliquer la position à la fenêtre bloquante
        fenetre_rapport_debut_tour.geometry(f"700x500+{x_position}+{y_position}")
        
        # Label en haut
        label = tk.Label(fenetre_rapport_debut_tour, textvariable=self.label_intro_debut_tour, font=self.custom_font)
        label.pack(pady=10)     
        
        # Frame pour contenir la zone de texte et la scrollbar
        frame = tk.Frame(fenetre_rapport_debut_tour)
        frame.pack(pady=10, fill="both", expand=True) 
        
        # Zone de texte
        text_rapport_debut_tour = tk.Text(frame, wrap="word", height=10, width=40)
        
        text_rapport_debut_tour.pack(side="left", fill="both", expand=True) 
        
        text_rapport_debut_tour.tag_configure("bold", font=("Arial", 12, "bold"))
        text_rapport_debut_tour.tag_configure("normal", font=("Arial", 12))
        #On ne veut pas que l'utilisateur modifie le texte
        for text, style in texte_formate:
            if style:
                text_rapport_debut_tour.insert("end", text,"bold")
            else:
                text_rapport_debut_tour.insert("end", text,"normal")
                

                
        text_rapport_debut_tour.config(state="disabled")
    
        # Barre de défilement verticale
        scrollbar = tk.Scrollbar(frame, command=text_rapport_debut_tour.yview)
        scrollbar.pack(side="right", fill="y")
    
        # Lier la barre de défilement à la zone de texte
        text_rapport_debut_tour.config(yscrollcommand=scrollbar.set)
        
        # Bouton pour fermer la fenêtre
        close_button = tk.Button(fenetre_rapport_debut_tour, text="Fermer",font=self.custom_font, command=fenetre_rapport_debut_tour.destroy)
        close_button.pack(pady=10)
    
        
        

    
   
    def fin_de_tour(self):
        """
        Fait 
        """
        
        if self.joueur_actuelle == "Joueur":
            #des que le joueur fini son tour , on clear le rapport
            self.text_rapport_debut_tour = []
            self.text_rapport_debut_tour += [("Aucun Ennemi n'a jouer depuis le tour précedent\n", None)]
            self.tour_joueur = False
             
        joueur = self.dico_joueurs[self.joueur_actuelle]
        
        liste_villages = joueur.get_villages() #renvoie le dico {id village: classe village}
        for image_id, village in list(liste_villages.items()):
            multiplicateur_production = 1
            liste_villageois = village.get_villageois()
            if village.possede_egilse():
                rite = village.get_rite_egilse()
                if rite == 'fertilité':
                    self.ajouter_villageois(image_id,True)
                elif rite == 'bonheur':
                    for villageois in liste_villageois:
                        villageois.gestionhumeur(1)                    
                else:
                    multiplicateur_production = multiplicateur_production*1.2
                    
            for villageois in liste_villageois:
                multiplicateur_final = multiplicateur_production
                villageois.vieillir()#il prenne 1 ans
                villageois.gestionhumeur(1) #les villageois gagne 1 d'humeur pas tour
                humeur = villageois.get_humeur()
                multiplicateur_final = multiplicateur_final*(0.5+humeur/10) #humeur modifie la multiplicateur_production de 0.5 jusqu'a 1.5 par pas de 0.1
                villageois.production(multiplicateur_final)#ils produisent leur CPD* multiplicateur_final
                villageois.manger(11,village)#il mange x ressource pour survivre
                villageois.commerce()#il transforme x% de leur ressource en argent
            village.check_villageois()#verifie si des villageois doivent mourir
        
        #debut du tour de l'autre joueur
        self.prochain_joueur()
        
        
    def prochain_joueur(self):
        """
        Passe au joueur suivant dans la liste de tour de jeux ou creer un nouveau tour si elle est vide
        """
        if not self.fin_du_jeux: #en cas de fin de partie on bloque tout le code
            if self.tour_jeux != []:
                self.joueur_actuelle = self.tour_jeux.pop(0)
                # rendre les unités en attente en debut de tour
                joueur_class = self.dico_joueurs[self.joueur_actuelle]
                joueur_class.rendre_fantassin()
                joueur_class.rendre_soldat()
                joueur_class.rendre_chevalier()
                self.barre_menu.update_unite()
                print("le joueur actuelle est",self.joueur_actuelle)
                
                #Debut d'un nouveau tour pour le joueur
                if self.joueur_actuelle == "Joueur":
                    self.tour_joueur = True
                    for vassal in self.dico_vassal_exiger:
                        self.dico_vassal_exiger[vassal] = [False,False]
                    self.fermer_fenetre_bloquante_ordre_tour()
                    var_menu,cle_menu = self.menu_actif
                    if cle_menu == "village" and self.Evenement.get_evenement_actuel()[0] == "Incendie":
                        self.affiche_menu()
                    elif cle_menu == "rapport":
                        self.update_rapport_villageois()
                    self.affiche_menu(var_menu,cle_menu)                  
                    self.creer_fenetre_rapport_debut_tour(self.text_rapport_debut_tour)
                
                else:
                    self.creer_fenetre_bloquante_ordre_tour()
                    joueur = self.dico_joueurs[self.joueur_actuelle]
                    rapport_IA = self.IA.Tour_IA(joueur, self.joueur_actuelle)
                    if self.text_rapport_debut_tour[0][0][0] == "A":
                        self.text_rapport_debut_tour.pop()
                    self.text_rapport_debut_tour += [(f"Tour de {self.joueur_actuelle} :\n", "bold")]
                    self.text_rapport_debut_tour += [(rapport_IA + "\n\n", None)]
                    self.fin_de_tour()
                    
            else:
                #tout les joueur on fait leur tour, on lance donc un nouveau tour.
                #on melange la liste des joueurs pour definir l'ordre de jeu
                self.nb_de_tour += 1
                liste_joueur = list(self.dico_joueurs.keys())
                rd.shuffle(liste_joueur)
                self.tour_jeux = liste_joueur
                print("Tour de jeux = ",self.tour_jeux)
                #On appelle la fonction qui renvoie et execute un evenement aleatoire 
                self.Evenement.selection_evenement()                                              
                self.prochain_joueur()
                if self.id_rectangle_selection != None:
                    tags = self.canvas_map.gettags(self.id_rectangle_selection)
                    if tags[1][0:6] == "Ennemi":
                        self.affiche_menu()
            
    def fin_de_partie(self, joueur, type_de_fin):
        """
        Lance l'écran de fin de partie avec des messages améliorés.
        texte mis en forme par chatgpt
        """
        # Faire une belle fenêtre
        if self.joueur_actuelle != "Joueur":
            self.fermer_fenetre_bloquante_ordre_tour()
        toplevel = tk.Toplevel(self.root)
        toplevel.title("Fin de la partie")
        toplevel.grab_set()
    
        # Sélectionner l'image et le message en fonction du résultat
        if joueur[0] == "Joueur":  # Victoire du joueur
            img = Image.open("Images/victoire.png").resize((700, 400), Image.LANCZOS)
            if type_de_fin == "destruction":
                message_fin = f"Victoire éclatante ! Vous avez éliminé le dernier village ennemi en {self.nb_de_tour} tour."
            elif type_de_fin == "conquete":
                message_fin = f"Triomphe total ! Vous êtes le dernier survivant sur le champ de bataille en {self.nb_de_tour} tour."
            elif type_de_fin == "vassaliser":
                message_fin = f"Victoire stratégique ! Vous avez soumis tous vos adversaires à votre domination en {self.nb_de_tour} tour."
            elif type_de_fin == "event":
                message_fin = f"Une victoire inattendue ! Les événements vous ont porté au sommet en {self.nb_de_tour} tour."
            else:
                message_fin = "Bravo ! Vous avez remporté la partie en {self.nb_de_tour} tour."
        else:  # Défaite du joueur
            img = Image.open("Images/defaite.png").resize((700, 400), Image.LANCZOS)
            if type_de_fin == "destruction":
                message_fin = f"Défaite cuisante... Votre dernier village a été détruit en {self.nb_de_tour} tour."
            elif type_de_fin == "conquete":
                message_fin = f"Tous vos espoirs se sont éteints... Vous n'êtes plus en lice en {self.nb_de_tour} tour."
            elif type_de_fin == "vassaliser":
                message_fin = f"Vous avez été dominé... Votre règne s'est terminé en vassalité en {self.nb_de_tour} tour."
            elif type_de_fin == "event":
                message_fin = f"Le destin a tranché... Un événement a mis fin à votre règne en {self.nb_de_tour} tour."
            else:
                message_fin = "Malheureusement, vous avez perdu la partie."
    
            # Ajouter un message sur le gagnant si ce n'est pas "aucun"
            if joueur[0] != "aucun":
                message_fin += f"\n{joueur[1].get_nom()} a remporté la victoire."
    
        
    
        img_label = tk.Label(toplevel, width=700, height=400)
        img = ImageTk.PhotoImage(img)         
        img_label.config(image=img)
        img_label.image = img  # Conserver une référence pour éviter la suppression par le garbage collector
        img_label.pack(pady=10)
        
        # Afficher le message et l'image
        label = tk.Label(toplevel, text=message_fin, font=self.custom_font, wraplength=600, justify="center")
        label.pack(pady=10)
      
        close_button = tk.Button(toplevel, text="Retour a l'écran titre",font = self.custom_font, command=self.retour_ecran_titre)
        close_button.pack(pady=10)
    
    def retour_ecran_titre(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        EcranTitre = main.EcranTitre
        self.root.ChangerFenetre(EcranTitre,self.tuto,self.cheat,self.custom_font)
        
    
            
        
        

        


    

