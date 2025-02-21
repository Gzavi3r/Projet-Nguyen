# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 13:46:40 2024

@author: Brice
"""

import random as rd

class Initialisation_Evenement:
    def __init__(self, root, seed, Menu, canvas_map, canvas_menu,barre_menu, dico_village, dico_joueurs,images_tk,label_intro_debut_tour):
        # Transfert des variables
        self.root = root
        rd.seed(seed)
        self.Menu = Menu
        self.canvas_map = canvas_map
        self.canvas_menu = canvas_menu
        self.barre_menu = barre_menu
        self.dico_village = dico_village
        self.dico_joueurs = dico_joueurs
        self.images_tk = images_tk
        self.label_intro_debut_tour = label_intro_debut_tour
        
        # Stocke l'événement actif
        self.evenement_actuel = None
    
    def get_evenement_actuel(self):
        return self.evenement_actuel

    # Exemple d'effets des événements
    def epidemie_general(self):
        nb_mort = 0
        for image_id,village in self.dico_village.items():
            self.canvas_map.itemconfig(image_id, image=self.images_tk['village_epidemie'])
            i= 0
            liste_villageois = village.get_villageois()
            while i < len(liste_villageois):
                villageois = liste_villageois[i]
                if villageois.get_edv()-villageois.get_age()<10:#si un villageois a moins de 10 ans a vivre
                    village.tuer_villageois(villageois,i)
                    nb_mort += 1
                else:
                    i += 1
        return ("Épidémie générale",nb_mort)

    def epidemie_local(self):
        image_id,village = rd.choice(list(self.dico_village.items()))
        self.canvas_map.itemconfig(image_id, image=self.images_tk['village_epidemie'])
        nb_mort = 0
        i= 0
        liste_villageois = village.get_villageois()
        while i < len(liste_villageois):
            villageois = liste_villageois[i]
            if villageois.get_edv()-villageois.get_age()<10:#si un villageois a moins de 10 ans a vivre
                village.tuer_villageois(villageois,i)
                nb_mort += 1
            else:
                i += 1
        return ("Épidémie locale",image_id,village,nb_mort)

    def incendie(self):
        """
        un village est bruler et sera detruit au prochain tour
        """
        image_id,village = rd.choice(list(self.dico_village.items()))
        nom_village = village.get_nom()
        self.canvas_map.dtag(image_id)   
        tags = self.canvas_map.gettags(image_id)
        joueur = self.dico_joueurs[tags[1]]
        self.Menu.detruire_village(image_id,(tags[1],joueur))
        self.canvas_map.itemconfig(image_id, tags = ("bruler","Autre"))
        self.canvas_map.itemconfig(image_id, image=self.images_tk['village_incendie'])
        return ("Incendie",image_id,nom_village,(tags[1],joueur))

    def pillage(self):
        """
        selectionne deux joueur aleatoire et donne 33% des bien de l'un a l'autre
        """
        joueur1,joueur2 = rd.sample(list(self.dico_joueurs.items()),2)
        pillage_argent = joueur2[1].get_argent()//3
        pillage_ressource = joueur2[1].get_ressource()//3
        joueur1[1].modifier_argent(pillage_argent)
        joueur1[1].modifier_ressource(pillage_ressource)
        joueur2[1].modifier_argent(-pillage_argent)
        joueur2[1].modifier_ressource(-pillage_ressource)
        self.barre_menu.update_stats()
        return ("Pillage",joueur1,joueur2,pillage_argent,pillage_ressource)

    def famine(self):
        """
        tout les habitant d'un village on leur CDP*0.5'
        
        """
        village = rd.choice(list(self.dico_village.values()))
        print("Famine",village.get_nom())
        liste_villageois = village.get_villageois()
        for villageois in liste_villageois:
            villageois.modifier_cdp(0.5)
        return ("Famine",village)

    def recolte_abondante(self):
        """
        tout les habitant d'un village on leur CDP*2'
        """
        village = rd.choice(list(self.dico_village.values()))
        liste_villageois = village.get_villageois()
        for villageois in liste_villageois:
            villageois.modifier_cdp(1.5)
        return ("Récolte abondante",village)

    def immigration(self):
        village = rd.choice(list(self.dico_village.values()))
        choix = rd.choices(["Artisan", "Paysan"],[1,2])[0] #chois de soit Artisans avec une probabilité de 1/3 soit Paysans avec une probabilité de 2/3
        village.ajouter_villageois(choix)      
        return ("Immigration",village,choix)
    
    def immigration_massive(self):
        for village in self.dico_village.values():
            choix = rd.choices(["Artisan", "Paysan"],[1,2])[0] #chois de soit Artisans avec une probabilité de 1/3 soit Paysans avec une probabilité de 2/3
            village.ajouter_villageois(choix)   
        return ("immigration massive",)

    def vassalisation(self):
        joueur1,joueur2 = rd.sample(list(self.dico_joueurs.items()),2)
        #joueur2 = ("Joueur",self.dico_joueurs["Joueur"])
        #joueur1 = ("Ennemi 1",self.dico_joueurs["Ennemi 1"])
        nom_vassal,class_vassal = joueur2
        nom_joueur,class_joueur = joueur1
        if class_vassal.get_vassaliser_par() == nom_joueur: #Si le joueur2 est deja un vassal du joueur1
            don_fantassin = rd.randint(0, class_vassal.get_fantassin()//2)
            don_soldat = rd.randint(0, class_vassal.get_soldat()//2)
            class_vassal.modifier_fantassin(-don_fantassin)
            class_vassal.modifier_soldat(-don_soldat)
            class_joueur.modifier_fantassin(don_fantassin)
            class_joueur.modifier_soldat(don_soldat)
            return("Don",nom_joueur,class_joueur,nom_vassal,class_vassal,don_fantassin,don_soldat)
        elif class_joueur.get_vassaliser_par() == nom_vassal: #Si le joueur1 est un vassal du joueur2
            class_vassal.supprimer_vassal(nom_joueur)
            class_joueur.vassaliser_par(False)
            return("affranchissement",nom_joueur,class_joueur,nom_vassal,class_vassal)
            
        else:
            self.Menu.vassaliser(joueur1,joueur2,True)
            return ("Vassalisation",nom_joueur,class_joueur,nom_vassal,class_vassal)

    def rien(self):
        return ("Rien",)

    # Méthode pour réinitialiser les effets de l'événement précédent
    def finir_evenement(self):
        """
        Fonction pour finir ou retablir les evenement en plusieur temps:
                detruire le village incendier
                redonner une CDP normal apres une famine
        """
        if self.evenement_actuel == None:
            return 0
        if self.evenement_actuel[0] == "Incendie":
            self.canvas_map.itemconfig(self.evenement_actuel[1], tags = ("plaine",self.evenement_actuel[3][0]))
            self.canvas_map.itemconfig(self.evenement_actuel[1], image=self.images_tk[f'plaine_{self.evenement_actuel[3][0]}'])
            
        elif self.evenement_actuel[0] == "Famine":
            
            village = self.evenement_actuel[1]
            
            liste_villageois = village.get_villageois()
            for villageois in liste_villageois:
                villageois.modifier_cdp(2)
                
        elif self.evenement_actuel[0] == "Épidémie locale":
            self.canvas_map.itemconfig(self.evenement_actuel[1], image=self.images_tk['village'])
        elif self.evenement_actuel[0] == "Épidémie générale":  
            for image_id in self.dico_village:
                self.canvas_map.itemconfig(image_id, image=self.images_tk['village'])
                
        elif self.evenement_actuel[0] == "Récolte abondante":
            village = self.evenement_actuel[1]
            liste_villageois = village.get_villageois()
            for villageois in liste_villageois:
                villageois.modifier_cdp(2/3)                   
        self.evenement_actuel = None


    def mise_forme_evenement(self, evenement):
        """
        Prend un événements et génère une chaîne cohérente pour le décrire.
    
        :param list_evenement: tuples représentant l'événement.
        :return: Une chaîne formatée décrivant l'événement.
        """
        resultats = ""
    
        type_evenement = evenement[0]

        if type_evenement == "Épidémie générale":
            nb_mort = evenement[1]
            resultats += f"Une épidémie générale a causé la mort de {nb_mort} personnes dans la région."

        elif type_evenement == "Épidémie locale":
            village, nb_mort = evenement[2], evenement[3]
            resultats +=f"Une épidémie a frappé le village de {village.get_nom()}, causant {nb_mort} morts."

        elif type_evenement == "Incendie":
            nom_village, joueur =  evenement[2], evenement[3]
            txt1 = ""
            if joueur[0] == "Joueur":
                txt1 = "(vous)"
            resultats +=f"Un incendie a ravagé le village de {nom_village}, appartenant à {joueur[1].get_nom()}{txt1}."

        elif type_evenement == "Pillage":
            joueur1, joueur2, pillage_argent, pillage_ressource = evenement[1:5]
            txt1 = ""
            txt2 = ""
            if joueur1[0] == "Joueur":
                txt1 = "(vous)"
            if joueur2[0] == "Joueur":
                txt2 = "(vous)"
            resultats += f"{joueur1[1].get_nom()}{txt1} a pillé {pillage_argent} pièces d'or et {pillage_ressource} ressources a {joueur2[1].get_nom()}{txt2}."
            

        elif type_evenement == "Famine":
            village = evenement[1]
            resultats +=f"Une famine a frappé le village de {village.get_nom()}, la production de chaque villageois est réduite de 50%."

        elif type_evenement == "Récolte abondante":
            village = evenement[1]
            resultats +=f"Le village de {village.get_nom()} a bénéficié d'une récolte abondante,la production de chaque villageois est augmenté de 50%."

        elif type_evenement == "Immigration":
            village, choix = evenement[1], evenement[2]
            resultats +=f"Une immigration a eu lieu, attirant un {choix} a {village.get_nom()}"
        
        elif type_evenement == "immigration massive":
            resultats += "Une vague d'immigration massive a frappé toute la région"

        elif type_evenement == "Vassalisation":
            nom_joueur,class_joueur,nom_vassal ,class_vassal = evenement[1:5]
            txt1 = ""
            txt2 = ""
            if nom_joueur == "Joueur":
                txt1 = "(vous)"
            if nom_vassal == "Joueur":
                txt2 = "(vous)"
            resultats += f"{class_vassal.get_nom()}{txt2} a décidé de son plein gré de se vassaliser à {class_joueur.get_nom()}{txt1}."
        
        elif type_evenement == "Don":
            nom_joueur,class_joueur,nom_vassal ,class_vassal,don_fantassin,don_soldat = evenement[1:7]
            txt1 = ""
            txt2 = ""
            if nom_joueur == "Joueur":
                txt1 = "(vous)"
            if nom_vassal == "Joueur":
                txt2 = "(vous)"
            resultats += f"{class_vassal.get_nom()}{txt2} a décidé de prouver sa servitude à {class_joueur.get_nom()}{txt1} et lui a donné {don_fantassin} Fantassins et {don_soldat} Soldats."
        elif type_evenement == "affranchissement":
            nom_joueur,class_joueur,nom_vassal ,class_vassal = evenement[1:5]
            txt1 = ""
            txt2 = ""
            if nom_joueur == "Joueur":
                txt1 = "(vous)"
            if nom_vassal == "Joueur":
                txt2 = "(vous)"
            resultats += f"Dans un élan de bonté,{class_vassal.get_nom()}{txt2} a décidé d'affranchir {class_joueur.get_nom()}{txt1}."
            

        elif type_evenement == "Rien":
            resultats +="Aucun événement notable ne s'est produit."

        else:
            resultats +="/!\Erreur Un événement inconnu s'est produit."
    
        self.label_intro_debut_tour.set(resultats)
        
    # Fonction qui appelle une des fonctions aléatoirement
    def selection_evenement(self):
        # Réinitialiser l'événement précédent
        self.finir_evenement()
        
        # Liste des fonctions disponibles
        fonctions = [
            self.epidemie_general, self.epidemie_local, self.incendie,self.pillage, self.famine, 
            self.recolte_abondante, self.immigration,self.immigration_massive,self.vassalisation, 
            self.rien]
        
        probabilites = [
               0.13,  # Probabilité pour epidemie_general
               0.15, # Probabilité pour epidemie_local
               0.01, # Probabilité pour incendie
               0.15,  # Probabilité pour pillage
               0.10,  # Probabilité pour famine
               0.15, # Probabilité pour recolte_abondante
               0.10,  # Probabilité pour immigration
               0.05, # Probabilité pour immigration_massive
               0.01, # Probabilité pour vassalisation
               0.25  # Probabilité pour rien
           ]

        # Sélection d'une fonction au hasard
        fonction_choisie = rd.choices(fonctions, weights=probabilites, k=1)[0]
        
        # Exécuter l'événement et le stocker
        self.evenement_actuel = fonction_choisie()
        #Mettre a jour l'event de la barre_menu
        self.barre_menu.update_event(self.evenement_actuel[0])
        self.mise_forme_evenement(self.evenement_actuel)
    
    
    
