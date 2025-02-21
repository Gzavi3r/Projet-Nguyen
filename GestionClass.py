# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 15:27:57 2024

@author: Brice
"""

import random as rd
rd.seed(0)

class Personne:
    """
    Initialise une personne avec un nom choisi aléatoirement, une espérance de vie, un âge,
    des ressources initiales et un montant d'argent.
    """
    noms_possibles = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi"]
    
    """
    :param pres: Le nombre initial de ressources de la personne.
    :param parg: Le montant initial d'argent de la personne.
    :param liste_nom: Liste des noms possibles pour la personne (optionnel).
    """

    def __init__(self, pres, parg, liste_nom = noms_possibles):
        """
        Initialise une personne avec un nom choisi aléatoirement, une espérance de vie, un âge,
        des ressources initiales et un montant d'argent.
        
        :param pres: Le nombre initial de ressources de la personne.
        :param parg: Le montant initial d'argent de la personne.
        :param liste_nom: Liste des noms possibles pour la personne (optionnel).
        """
        self.statut = type(self).__name__
        self.nom = rd.choice(liste_nom)
        
        self.ressource = pres
        self.argent = parg


    def __str__(self):
        """
        Retourne une représentation textuelle de la personne.
        
        :return: Une chaîne décrivant le nom, le statut, les ressources et l'argent de la personne.
        """
        return f"Je m'appelle {self.nom} et je suis un(e) {self.statut}.\n" \
               f"J'ai {self.ressource} ressource(s) et {self.argent} pièce(s)."
    
    def get_nom(self):
        """
        Retourne le nom de la personne.

        :return: Le nom de la personne.
        """
        return self.nom
    
    def get_argent(self):
        """
        Retourne le montant d'argent de la personne.
        
        :return: Le montant d'argent de la personne.
        """
        return self.argent
    
    def get_statut(self):
        """
        Retourne le statut de la personne.
        
        :return: Le statut de la personne (ex : Artisan, Paysan, etc.).
        """
        return self.statut
    
    def get_ressource(self):
        """
        Retourne le nombre de ressources de la personne.
        
        :return: Le nombre de ressources de la personne.
        """
        return self.ressource
    
    def modifier_ressource(self, montant):
        """
        Modifie les ressources de la personne en ajoutant ou en soustrayant un montant donné.
        Lève une exception si les ressources deviennent négatives.
        
        :param montant: Le montant à ajouter (positif) ou à retirer (négatif).
        :raises ValueError: Si le résultat est inférieur à zéro.
        """
        if montant+self.ressource<0:
            raise ValueError(f"{self.nom} : Ressources insuffisantes!")
        self.ressource += montant

    def modifier_argent(self, montant):
        """
        Modifie le montant d'argent de la personne en ajoutant ou en soustrayant un montant donné.
        Lève une exception si l'argent devient négatif.
        
        :param montant: Le montant à ajouter (positif) ou à retirer (négatif).
        :raises ValueError: Si le résultat est inférieur à zéro.
        """
        if montant+self.argent<0:
            raise ValueError(f"{self.nom} : Argent insuffisants!")
        self.argent += montant


            
       
class Roturier(Personne):
    """
    Classe représentant un Roturier, héritant de la classe Personne.
    Un Roturier possède une capacité de production, une humeur, une espérance de vie, et un âge.
    """

    def __init__(self, pres, parg, pcdp):
        """
        Initialise un Roturier avec des ressources, de l'argent, une capacité de production,
        une humeur initiale, une espérance de vie et un âge aléatoires.
        
        :param pres: Le nombre initial de ressources du Roturier.
        :param parg: Le montant initial d'argent du Roturier.
        :param pcdp: La capacité de production du Roturier.
        """
        Personne.__init__(self, pres, parg)  # Appel au constructeur de Personne avec argent = 0
        self.cdp = pcdp  # Capacité de production
        self.humeur = 5
        self.edv = rd.randint(30, 100)
        self.age = rd.randint(15, 25)
        self.doit_mourir = False
        self.en_revolte = False
        
      
        
    def __str__(self):
        """
        Retourne une représentation textuelle du Roturier.
        
        :return: Une chaîne décrivant le nom, le statut, les ressources, l'argent, et la capacité de production.
        """
        return Personne.__str__(self) + f"\nJe produit {self.cdp} ressource par ans"
    
    def get_doit_mourir(self):
        """
        Indique si le Roturier doit mourir.
        
        :return: True si le Roturier doit mourir, sinon False.
        """
        return self.doit_mourir
    
    def get_en_revolte(self):
        """
        Indique si le Roturier est en révolte.
        
        :return: True si le Roturier est en révolte, sinon False.
        """
        return self.en_revolte
    
    def fin_de_revolte(self):
        """
        Met fin à l'état de révolte du Roturier.
        """
        self.en_revolte = False
    
    def get_humeur(self):
        """
        Retourne l'humeur actuelle du Roturier.
        
        :return: L'humeur du Roturier (valeur entre 0 et 10).
        """
        return self.humeur
    
    def get_cdp(self):
        """
        Retourne la capacité de production du Roturier.
        
        :return: La capacité de production du Roturier.
        """
        return self.cdp
    
    def get_age(self):
        """
        Retourne l'âge actuel du Roturier.
        
        :return: L'âge du Roturier.
        """
        return self.age
    
    def get_edv(self):
        """
        Retourne l'espérance de vie du Roturier.
        
        :return: L'espérance de vie du Roturier.
        """
        return self.edv
    
    def modifier_cdp(self,multiplicateur):
        """
        Modifie la capacité de production du Roturier en la multipliant par un facteur donné.
        
        :param multiplicateur: Le facteur multiplicatif pour la capacité de production.
        """
        self.cdp = int(self.cdp*multiplicateur)
        
    def production(self,multiplicateur):
        """
        Augmente les ressources du Roturier en fonction de sa capacité de production
        et d'un facteur multiplicatif.
        
        :param multiplicateur: Le facteur multiplicatif appliqué à la capacité de production.
        """
        self.ressource += int(self.cdp*multiplicateur)
    
    def gestionhumeur(self, pnbr):
        """
        Ajuste l'humeur du Roturier et vérifie si cela déclenche une révolte.
        
        :param pnbr: La quantité à ajouter ou soustraire à l'humeur.
        """
        self.humeur += pnbr
        if self.humeur <= 0:
            self.en_revolte = True
        elif self.humeur >10:
            self.humeur = 10
            
    def manger(self,quantite,village):
        """
        Permet au Roturier de consommer une quantité donnée de ressources. Si les ressources
        ne suffisent pas, il tente d'en acheter dans le village. Si cela échoue, il peut mourir.
        
        :param quantite: La quantité de ressources à consommer.
        :param village: L'objet village où le Roturier peut tenter d'acheter des ressources.
        """
        if quantite<=self.ressource:
            self.gestion("Ressource", -quantite)
        else:
            if quantite > self.argent:
                print(f"{self.nom} n'a pas asser d'argent pour acheter a manger")
                self.doit_mourir = True
            else:
                riche = self.trouve_riche(quantite,village)
                if riche == None:           
                    print(f"{self.nom} n'a pas trouver de ressource dans le village pour manger")
                    self.doit_mourir = True
                else:                
                    self.achete(quantite)
                    riche.vend(quantite)
                    self.gestion("Ressource", -quantite)
    
    def trouve_riche(self,quantite,village):
        """
        Cherche un villageois riche dans le village qui possède suffisamment de ressources
        pour vendre la quantité demandée.
        
        :param quantite: La quantité de ressources requises.
        :param village: L'objet village contenant les villageois.
        :return: Le villageois trouvé ou None si aucun ne convient.
        """
        liste_villageois = village.get_villageois()
        riche = None
        nb_richesse = 0
        for villageois in liste_villageois:
            nb_ressource = villageois.get_ressource()
            #si le villageois a 2 fois la quantiter de ressource requise(il faut qu'il mange lui aussi) et qu'il est plus riche que le riche selectionner
            if nb_ressource >= quantite*2 and nb_ressource > nb_richesse:
                riche = villageois
                nb_richesse = nb_ressource
        return riche
        
    
    def commerce(self):
        """
        Effectue une transaction commerciale où le Roturier convertit un pourcentage
        de ses ressources en argent, simulant une vente.
        """
        diviseur = rd.randint(2,3)
        nb = self.ressource//diviseur
        self.vend(nb)
            
    def gestion(self, ptype, pnbr):
        """
        Gère les modifications des ressources ou de l'argent du Roturier.
        
        :param ptype: Le type de ressource à modifier ("Argent" ou "Ressource").
        :param pnbr: La quantité à ajouter ou soustraire.
        """
        if ptype == "Argent":
            self.modifier_argent(pnbr)
        elif ptype == "Ressource":
            self.modifier_ressource(pnbr)
        else:
            print(f"Erreur dans gestion: Type '{ptype}' non reconnu.")

    def vend(self, pnbr):
        """
        Permet au Roturier de vendre une quantité de ressources pour obtenir de l'argent.
        
        :param pnbr: La quantité de ressources à vendre.
        """
        if pnbr <= self.ressource:
            self.gestion("Ressource", -pnbr)
            self.gestion("Argent", pnbr)
        else:
            print(f"Erreur dans vend: Quantité de ressources insuffisante ({self.ressource} disponibles).")

    def achete(self, pnbr):
        """
        Permet au Roturier d'acheter une quantité de ressources en dépensant de l'argent.
        
        :param pnbr: La quantité de ressources à acheter.
        """
        if pnbr <= self.argent:
            self.gestion("Ressource", pnbr)
            self.gestion("Argent", -pnbr)
        else:
            print(f"Erreur dans achete: Quantité d'argent insuffisante ({self.argent} disponibles).")

    def vieillir(self):
        """
        Incrémente l'âge du Roturier d'un an et vérifie s'il atteint son espérance de vie.
        """
        self.age += 1
        if self.age >= self.edv:
            self.doit_mourir = True


        
    
 
        
class Paysan(Roturier):
    """
    Classe représentant un paysan, héritant de la classe Roturier.
    Le paysan commence avec 0 argent et une capacité de production (cdp) 
    """

    def __init__(self, pres, pcdp):
        """
        Initialise un paysan avec :
            - 0 argent
            - une capacité de production (cdp) 
        """
        Roturier.__init__(self, pres, 0, pcdp)  # Appel au constructeur de Roturier avec argent = 0
    
        
class Artisan(Roturier):
    """
    Classe représentant un Artisan, héritant de la classe Roturier.
    L'Artisan commence avec 10 unités d'argent et une capacité de production (cdp)
    ajustée à 1.2 fois celle passée en paramètre.
    """
    def __init__(self, pres, pcdp):
        """
        Initialise un Artisan avec les attributs suivants :
        - Nom hérité de Roturier.
        - 10 unités d'argent.
        - Une capacité de production (cdp) ajustée à +20% de celle donnée.

        :param pres: Nom ou identifiant de l'Artisan.
        :param pcdp: Capacité de production initiale.
        """
        Roturier.__init__(self, pres, 10, int(pcdp*1.2))  # Appel au constructeur de Roturier avec argent = 10 et a un boost de prod de 20%     


class Village:
    """
    Classe représentant un village avec un nom aléatoire, une liste de villageois (Paysan ou Artisan),
    des infrastructures, et des mécanismes de gestion (révoltes, impôts, festivals, etc.).
    
    La classe village premet aussi de superviser les classes Paysan et Artisan 
    """
    noms_villages_1 = ["","Saint"]
    noms_villages_2 = ["Montville", "Lavalys", "Bourgson", "Rivendell", "Castelroc", "Grenval", "Marest", "Beaurivage"]
    rivières = [
    "","sur la Seine", "sur la Loire", "sur le Rhône", "sur la Garonne", "sur la Dordogne",
    "sur le Rhin", "sur la Meuse", "sur l'Escaut", "sur la Moselle", "sur le Doubs",
    "sur la Vienne", "sur la Saône", "sur le Tarn", "sur l'Allier", "sur l'Aude",
    "sur la Marne", "sur l'Oise", "sur le Lot", "sur le Verdon", "sur la Vilaine"
    ]

    def __init__(self,pprod):
        """
        Initialise un village avec un nom généré aléatoirement, une liste vide de villageois,
        et des paramètres de base (production, infrastructures, etc.).
        
        :param pprod: Niveau de production initial du village.
        """
        self.nom = f"{rd.choice(self.noms_villages_1)} {rd.choice(self.noms_villages_2)} {rd.choice(self.rivières)}"
        self.liste_villageois = []
        self.production = pprod
        self.has_egilse = False
        self.has_caserne = False
        self.rite_egilse = None
        self.revolte_village = [False,{}] #un booleen pour savoir si le village est en revolte, et un dico avec en cle son indice dans la liste_villageois et en valeur sa class Roturier 
    
    def get_revolte_village(self):
        """Retourne les informations sur la révolte en cours."""
        return self.revolte_village
    
    def finir_revolte_village(self):
        """Met fin à la révolte dans le village."""
        self.revolte_village = [False,{}]
        
        
        
    def check_villageois(self):
        """
        Vérifie l'état de tous les villageois et retire ceux qui doivent mourir.
        """
        i= 0
        while i < len(self.liste_villageois):
            villageois = self.liste_villageois[i]
            if villageois.get_doit_mourir():
                #on ne bouge pas i car la liste se decale sur l'indice du villageois supprimer
                self.tuer_villageois(villageois,i)
            else:
                i += 1
    
    def tuer_villageois(self,villageois,indice):
        """
        Supprime un villageois de la liste des villageois.
        
        :param villageois: Villageois à supprimer.
        :param indice: Indice du villageois dans la liste.
        """
        del villageois
        del(self.liste_villageois[indice])
        
        
        
        
    
    def possede_egilse(self):
        """Retourne True si le village possède une église."""
        return self.has_egilse
    
    def possede_caserne(self):
        """Retourne True si le village possède une caserne."""
        return self.has_caserne
    
    def creer_caserne(self):
        """Ajoute une caserne au village."""
        self.has_caserne = True
    
    def get_rite_egilse(self):
        """Retourne le rite de l'église du village."""
        return self.rite_egilse
        
    def get_nom(self):
        """Retourne le nom du village."""
        return self.nom
    
    
    def get_villageois(self):
        """Retourne la liste des villageois du village."""
        return self.liste_villageois
    
    def creer_eglise(self,rite):
        """
        Ajoute une église au village avec un rite défini.
        
        :param rite: Rite religieux à associer à l'église.
        """
        self.has_egilse = True
        self.rite_egilse = rite
        
    def modifier_rite_egilse(self,rite):
        """Modifie le rite de l'église existante."""
        self.rite_egilse = rite

    def ajouter_villageois(self, ptype):
        """
        Ajoute un villageois (Paysan ou Artisan) au village.
        
        :param ptype: Type de villageois à ajouter ("Paysan" ou "Artisan").
        """
        if ptype == "Paysan":
            nouveau_villageois = Paysan(0, self.production)  # Crée un paysan avec 0 ressource de départ
        elif ptype == "Artisan":
            nouveau_villageois = Artisan(0, self.production)  # Crée un artisan avec 0 ressource de départ
        else:
            print("Type de villageois non reconnu. Utilisez 'Paysan' ou 'Artisan'.")
            return

        self.liste_villageois.append(nouveau_villageois)
        print(f"{nouveau_villageois.nom} a été ajouté au village {self.nom}.")

    def festival(self):
        """Organise un festival qui augmente l'humeur de tous les villageois de +1."""
        for villageois in self.liste_villageois:
            villageois.gestionhumeur(1)
        print(f"Festival au village {self.nom} ! L'humeur de chaque villageois a augmenté de +1.")


    def impot(self):
        """
        Collecte les impôts auprès de chaque villageois.
            - Prend la moitié de l'argent d'un paysan
            - Prend un quart de l'argent d'un artisan        
        Retourne :
            - Le total d'argent et de ressources collectés.
        """
        tmp = [0,0]
        for indice,villageois in enumerate(self.liste_villageois):
            if isinstance(villageois, Paysan):
                argent_impot = villageois.get_argent() // 2  # Moitié de l'argent
                ressource_impot = villageois.get_ressource() // 2
            elif isinstance(villageois, Artisan):
                argent_impot = villageois.get_argent() // 4  # Quart de l'argent
                ressource_impot = villageois.get_ressource() // 4
            else:
                print(f"Erreur impot {self.nom}")
                
            villageois.gestionhumeur(-1)
            if villageois.get_en_revolte():
                self.revolte_village[0] = True
                self.revolte_village[1][indice] = villageois
            villageois.gestion("Argent", -argent_impot)  # Déduit le montant de l'argent du villageois
            villageois.gestion("Ressource", -ressource_impot)
            tmp[0] += argent_impot  # Ajoute le montant collecté au trésor du village
            tmp[1] += ressource_impot

        return tmp
    
    

    def __str__(self):
        """
        Représentation textuelle du village, incluant ses villageois.
        """
        description_villageois = "\n".join(str(v) for v in self.liste_villageois)
        return f"Village: {self.nom}\nProduction: {self.production}\nVillageois:\n{description_villageois}" if self.liste_villageois else f"Village: {self.nom} (aucun villageois)"
    
    
class Noble(Personne):
    """
    Classe représentant un noble, qui possède des villages et peut avoir des vassaux (autres nobles).
    
    Permet aussi de superviser la classe village
    """

    noms_nobles = ["Lord Byron", "Lady Morgane", "Duc Armand", "Comtesse Lyra", "Marquis Quentin"]
    

    
    def __init__(self, pres, parg, liste_nom = noms_nobles ):
        """
        Initialise un noble avec un nom choisi aléatoirement, des unités militaires de base,
        ainsi que des listes vides pour les villages et les vassaux.

        :param pres: Le nombre initial de ressources du noble.
        :param parg: Le montant initial d'argent du noble.
        :param liste_nom: Liste des noms possibles pour le noble (optionnel).
        """
        Personne.__init__(self, pres, parg, liste_nom)
        self.villages = {}
        self.vassaux = {}
        
        self.Est_vassal_de = False #soit false soit le nom du maitre
        self.Est_capture_par = False #soit false soit le nom de l'ennemi
        self.fantassin = 10
        self.fantassin_en_attente = 0 #designe le nobre de fantassin en formation/ blesser et qui ne serons utilisable qu'au prochain tour 
        self.soldat = 0
        self.soldat_en_attente = 0 #idem
        self.chevalier = 1 #les chevalier represente le nobles ils on un traitement special comparé aux autre unités
        self.chevalier_en_attente = 0
        
    def get_fantassin(self):
        """
        Retourne le nombre actuel de fantassins disponibles.
        
        :return: Nombre de fantassins prêts.
        """
        return self.fantassin
    
    def modifier_fantassin(self,valeur):
        """
        Modifie le nombre de fantassins disponibles en ajoutant ou en soustrayant une valeur donnée.
        
        :param valeur: Nombre à ajouter ou à retirer aux fantassins.
        """
        self.fantassin = self.fantassin + valeur
        
    def get_fantassin_en_attente(self):
        """
        Retourne le nombre de fantassins en attente (formation ou blessés).
        
        :return: Nombre de fantassins en attente.
        """
        return self.fantassin_en_attente
        
    def modifier_fantassin_en_attente(self,valeur):
        """
        Modifie le nombre de fantassins en attente en ajoutant ou en soustrayant une valeur donnée.
        
        :param valeur: Nombre à ajouter ou à retirer aux fantassins en attente.
        """
        self.fantassin_en_attente = self.fantassin_en_attente + valeur
    
    def rendre_fantassin(self):
        """
        Transfère les fantassins en attente vers les fantassins disponibles et remet le compteur d'attente à zéro.
        """
        self.fantassin += self.fantassin_en_attente
        self.fantassin_en_attente = 0
    
    def get_soldat(self):
        """
        Retourne le nombre actuel de soldats disponibles.
        
        :return: Nombre de soldats prêts.
        """
        return self.soldat
    
    def modifier_soldat(self,valeur):
        """
        Modifie le nombre de soldats disponibles en ajoutant ou en soustrayant une valeur donnée.
        
        :param valeur: Nombre à ajouter ou à retirer aux soldats.
        """
        self.soldat = self.soldat + valeur
        
    def get_soldat_en_attente(self):
        """
        Retourne le nombre de soldats en attente (formation ou blessés).
        
        :return: Nombre de soldats en attente.
        """
        return self.soldat_en_attente
    
    def modifier_soldat_en_attente(self,valeur):
        """
        Modifie le nombre de soldats en attente en ajoutant ou en soustrayant une valeur donnée.

        :param valeur: Nombre à ajouter ou à retirer aux soldats en attente.
        """
        self.soldat_en_attente = self.soldat_en_attente + valeur
    
    def rendre_soldat(self):
        """
        Transfère les soldats en attente vers les soldats disponibles et remet le compteur d'attente à zéro.
        """
        self.soldat += self.soldat_en_attente
        self.soldat_en_attente = 0
    
    def get_chevalier(self):
        """
        Retourne le nombre actuel de chevaliers disponibles.
        
        :return: Nombre de chevaliers prêts.
        """
        return self.chevalier
    
    def modifier_chevalier(self,valeur):
        """
        Modifie le nombre de chevaliers disponibles en ajoutant ou en soustrayant une valeur donnée.
        
        :param valeur: Nombre à ajouter ou à retirer aux chevaliers.
        """
        self.chevalier = self.chevalier + valeur
    
    def get_chevalier_en_attente(self):
        """
        Retourne le nombre de chevaliers en attente (formation ou blessés).
        
        :return: Nombre de chevaliers en attente.
        """
        return self.chevalier_en_attente
        
    def modifier_chevalier_en_attente(self,valeur):
        """
        Modifie le nombre de chevaliers en attente en ajoutant ou en soustrayant une valeur donnée.
        
        :param valeur: Nombre à ajouter ou à retirer aux chevaliers en attente.
        """
        self.chevalier_en_attente = self.chevalier_en_attente + valeur
    
    def rendre_chevalier(self):
        """
        Transfère les chevaliers en attente vers les chevaliers disponibles et remet le compteur d'attente à zéro.
        """
        self.chevalier += self.chevalier_en_attente
        self.chevalier_en_attente = 0
        
    def get_villages(self):
        """
        Retourne la liste des villages appartenant au noble.
        
        :return: Dictionnaire des villages, où les clés sont les identifiants des villages.
        """
        return self.villages
    
    def get_vassal(self):
        """
        Retourne la liste des vassaux du noble.
        
        :return: Dictionnaire des vassaux, où les clés sont les noms des vassaux.
        """
        return self.vassaux
    
    def capturer_par(self,joueur):
        """
        Définit le joueur qui a capturé le noble.
        
        :param joueur: Nom ou instance du joueur ayant capturé le noble.
        """
        self.Est_capture_par = joueur
    
    def get_capturer_par(self):
        """
        Retourne le joueur qui a capturé le noble, ou False si le noble n'est pas capturé.
        
        :return: Nom ou instance du joueur, ou False.
        """
        return self.Est_capture_par
        
    def vassaliser_par(self,joueur):
        """
        Définit le joueur comme suzerain du noble (vassalisation).
        
        :param joueur: Nom ou instance du joueur devenant suzerain.
        """
        self.Est_vassal_de = joueur
        
    def get_vassaliser_par(self):
        """
        Retourne le suzerain du noble, ou False si le noble n'est pas vassalisé.
        
        :return: Nom ou instance du suzerain, ou False.
        """
        return self.Est_vassal_de

    def ajouter_village(self, image_id ,village):
        """
        Ajoute un village à la liste des villages du noble.

        :param image_id: Identifiant unique du village.
        :param village: Instance de la classe Village à ajouter.
        :raises ValueError: Si l'objet fourni n'est pas une instance de Village.
        """
        if isinstance(village, Village):
            self.villages[image_id] = village
            print(f"{village.nom} a été ajouté au domaine de {self.nom}.")
        else:
            print("Erreur : Seuls les objets de type Village peuvent être ajoutés.")
    
    def detruire_village(self,image_id):
        """
        Détruit un village appartenant au noble et le retire de la liste des villages.
        
        Laisse le garbage collector détruire les villageois dans ce village
        
        :param image_id: Identifiant unique du village à détruire.
        :raises KeyError: Si l'identifiant du village n'existe pas dans la liste.
        """
        village = self.villages[image_id]
        
        
        del village
        del self.villages[image_id]
    
    def supprimer_vassal(self,nom_vassal):
        """
        Supprime un vassal de la liste des vassaux du noble.
        
        :param nom_vassal: Nom du vassal à supprimer.
        :raises KeyError: Si le nom du vassal n'existe pas dans la liste.
        """
        del self.vassaux[nom_vassal]

    def ajouter_vassal(self,nom_vassal ,class_vassal):
        """
        Ajoute un vassal (autre noble) à la liste de vassaux du noble.

        :param vassal: Instance de la classe Noble à ajouter comme vassal.
        """
        if isinstance(class_vassal, Noble):
            self.vassaux[nom_vassal] = class_vassal
            print(f"{class_vassal.nom} est maintenant un vassal de {self.nom}.")
        else:
            print("Erreur : Seuls les objets de type Noble peuvent être ajoutés comme vassaux.")

    def afficher_domaine(self):
        """
        Affiche les villages et vassaux du noble.
        fait par ChatGPT
        """
        # Affiche les villages
        if self.villages:
            description_villages = "\n".join(f"- {village.nom}" for village in self.villages.values())
            domaine = f"Villages de {self.nom} :\n{description_villages}"
        else:
            domaine = f"{self.nom} ne possède aucun village."
    
        # Affiche les vassaux
        if self.vassaux:
            description_vassaux = "\n".join(f"- {vassal.nom}" for vassal in self.vassaux.values())
            vassaux = f"Vassaux de {self.nom} :\n{description_vassaux}"
        else:
            vassaux = f"{self.nom} ne possède aucun vassal."
    
        return f"{domaine}\n\n{vassaux}"
    

    def __str__(self):
        return Personne.__str__(self)    
  