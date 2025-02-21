# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 15:39:59 2024

@author: Brice
"""
import random as rd

class Initialisation_IA():
    
    def __init__(self,root,seed,Menu,Guerre,taille_map,taille_image,canvas_map,canvas_menu,barre_menu,dico_village,dico_joueurs,images_tk ,dico_valeur,dico_prix):
        #on transfere les variable du titre vers ici 
        self.root = root
        rd.seed(seed)
        self.Menu = Menu
        self.Guerre = Guerre
        self.taille_map = taille_map
        self.taille_image = taille_image
        self.canvas_map = canvas_map
        self.canvas_menu = canvas_menu
        self.barre_menu = barre_menu
        self.dico_village = dico_village
        self.dico_joueurs = dico_joueurs
        self.images_tk = images_tk
        self.dico_valeur = dico_valeur
        self.dico_prix = dico_prix

    def Tour_IA(self,joueur_class,joueur_nom):
        """
        L'IA ne sera pas très développée
        Le tour type d'une IA va etre:
            Taxer tout ses villages
            vas essayer de conquerir entre 0 et 3 cases (attaque si une des cases a un propriétaire)
            vas essayer de construire un village
            Va faire une action aléatoire dans un de ses villages
        elle va empiler toute ces actions dans une liste
                
        """
        list_action = [] #vas contenir une liste de str qui von représenter les action de l'ia
        
        self.Menu.taxer_multiple_village()
        case_attaquable = self.get_case_attaquable(joueur_nom)
        n = rd.randint(0,len(case_attaquable))%4
        case_attaquable = rd.sample(case_attaquable,n)
        
        for cases in case_attaquable:
            tags = self.canvas_map.gettags(cases)
            if tags[1] == "Neutre":
                #Conquerire

                if joueur_class.get_argent()>=self.dico_prix["conquete"][0] and joueur_class.get_ressource()>=self.dico_prix["conquete"][1]:
                    self.Menu.conquerir(cases)
                    list_action += [("Conquete",)]
                else:
                    list_action += [("Manque_ressource_conquete",)]
            else:
                joueur2_nom = tags[1]
                #attaque
                #on verifie si lIA a des unité
                if joueur_class.get_fantassin()+joueur_class.get_soldat()+joueur_class.get_chevalier() > 0:
                    cout_argent = 30+joueur_class.get_fantassin()*5 + joueur_class.get_soldat()*10 + joueur_class.get_chevalier() * 20
                    cout_ressource = 30+joueur_class.get_fantassin()*5 + joueur_class.get_soldat()*10 + joueur_class.get_chevalier() * 20
                    #on verifie si elle a les ressources
                    if joueur_class.get_argent()>=cout_argent and joueur_class.get_ressource()>=cout_ressource:
                        joueur2_class = self.dico_joueurs[joueur2_nom]
                        list_unite_joueur2 = [joueur2_class.get_fantassin(),joueur2_class.get_soldat(),joueur2_class.get_chevalier()]
                        list_unite_joueur1 = [joueur_class.get_fantassin(),joueur_class.get_soldat(),joueur_class.get_chevalier()]
                        rapport_guerre = self.Guerre.simuler_guerre(joueur_nom,list_unite_joueur1,joueur2_nom,list_unite_joueur2,cout_argent,cout_ressource)
                        self.Menu.consequance_attaque(cases,rapport_guerre,None)
                        list_action += [(f"Attaque_{joueur2_nom}",rapport_guerre)]
                    else:
                        list_action += [("Manque_ressource_attaque",)]
                else:
                    list_action += [("Manque_unite",)]
          
        if joueur_class.get_argent() >= self.dico_prix["creation_village"][0] and joueur_class.get_ressource() >= self.dico_prix["creation_village"][1]:
            
            id_plaine = self.get_plaine_joueur(joueur_nom)
            village_cree = False
            i = 0
            while i<3 and not village_cree:
                print("check place")
                id_case = rd.choice(id_plaine)
                if self.Menu.check_creation_village(id_case):
                    self.Menu.creation_village(id_case)
                    list_action += [("village_cree",)]
                    village_cree = True
                i+=1
            if not village_cree:
                list_action += [("Manque_place_village",)]
        else:
            list_action += [("Manque_ressource_village",)]
            
        list_choix = ["taxer","festival","ajouter_villageois","egilse","caserne"]
        action = rd.choice(list_choix)
        village = rd.choice(list(joueur_class.get_villages().items()))
        if action == "taxer":
            self.Menu.taxer(village[0])
            list_action += [("taxer",village)]
            
        elif action == "festival":
            if joueur_class.get_argent() >= self.dico_prix["festival"][0] and joueur_class.get_ressource() >= self.dico_prix["festival"][1]:
                self.Menu.festival(village[0])
                list_action += [("festival",village)]
            else:
                list_action += [("Manque_ressource_festival",)]
                
        elif action == "ajouter_villageois":
            if joueur_class.get_argent() >= self.dico_prix["venir_villageois"][0] and joueur_class.get_ressource() >= self.dico_prix["venir_villageois"][1]:
                self.Menu.ajouter_villageois(village[0])
                list_action += [("ajouter_villageois",village)]
            else:
                list_action += [("Manque_ressource_ajouter_villageois",)]
        
        elif action == "egilse":
            #si le village n'a pas d'eglise
            if not village[1].possede_egilse():
                if joueur_class.get_argent() >= self.dico_prix["creation_eglise"][0] and joueur_class.get_ressource() >= self.dico_prix["creation_eglise"][1]:
                    rite = rd.choice(["fertilité","bonheur","production"])
                    self.Menu.creer_egilse(village[0],rite)
                    list_action += [("Cree_eglise",village)]
                else:
                    list_action += [("Manque_ressource_cree_eglise",)]
            #si le village a une eglise, il va juste changer de rite
            else:
                rite = rd.choice(["fertilité","bonheur","production"])
                village[1].modifier_rite_egilse(rite)
                list_action += [("Modifier_rite",village)]
        
        elif action == "caserne":
            #si le village n'a pas de caserne
            if not village[1].possede_caserne():
                if joueur_class.get_argent() >= self.dico_prix["creation_caserne"][0] and joueur_class.get_ressource() >= self.dico_prix["creation_caserne"][1]:
                    self.Menu.creer_caserne(village[0])
                    list_action += [("Cree_caserne",village)]
                else:
                    list_action += [("Manque_ressource_cree_caserne",)]
            #si le village a une caserne, on va recruter une unite
            else:
                unite = rd.choice(["recruter_fantassin","recruter_soldat"])
                if joueur_class.get_argent() >= self.dico_prix[unite][0] and joueur_class.get_ressource() >= self.dico_prix[unite][1]:
                    if unite == "recruter_fantassin":
                        self.Menu.recruter_fantassin()
                        list_action += [("recruter_fantassin",)]
                    else:
                        self.Menu.recruter_soldat()
                        list_action += [("recruter_soldat",)]
                else:
                    list_action += [("Manque_ressource_recruter_unite",)]
        else:
            print(f"/!\Erreur : action de {joueur_nom} non reconnu")

        return self.mise_forme_texte(joueur_nom,list_action)
    
    def mise_forme_texte(self, joueur_nom, list_action):
        """
        Crée un texte cohérent décrivant les actions effectuées par l'IA.
        code généré par ChatGPT
    
        Arguments :
            joueur_nom (str) : Nom du joueur IA.
            list_action (list) : Liste des actions effectuées par l'IA. Chaque action est une tuple contenant un nom d'action et éventuellement des détails.
    
        Retourne :
            str : Texte décrivant les actions de l'IA.
        """
        msg = ""
        nb_conquete = 0
        for action in list_action:
            if action[0] == "Conquete":
                nb_conquete += 1
                
            elif action[0].startswith("Attaque_"):
                adversaire = action[0].split("_")[1]
                if adversaire == "Joueur":
                    adversaire += "(vous)"
                victoire = action[1][10]
                msg += f"\t- A attaqué {adversaire} : {'Victoire !' if victoire == joueur_nom else 'Défaite.'}.\n"
            
           
            elif action[0] == "village_cree":
                msg += "\t- A créé un nouveau village.\n"
           
           
            elif action[0] == "taxer":
                village = action[1]
                msg += f"\t- A taxé le village {village[1].get_nom()}.\n"
                
            elif action[0] == "festival":
                village = action[1]
                msg += f"\t- A organisé un festival dans le village {village[1].get_nom()}.\n"
            
            elif action[0] == "ajouter_villageois":
                village = action[1]
                msg += f"\t- A ajouté des villageois au village {village[1].get_nom()}.\n"
           
            elif action[0] == "Cree_eglise":
                village = action[1]
                msg += f"\t- A créé une église dans le village {village[1].get_nom()}.\n"
            
            elif action[0] == "Cree_caserne":
                village = action[1]
                msg += f"\t- A créé une caserne dans le village {village[1].get_nom()}.\n"
           
            elif action[0] == "recruter_fantassin":
                msg += "\t- A recruté un fantassin.\n"
            elif action[0] == "recruter_soldat":
                msg += "\t- A recruté un soldat.\n"
            
        if nb_conquete > 0:
            msg += f"\t- A conquis {nb_conquete} cases neutre.\n"
        
        if msg == "":
            msg += "\t- N'a rien fait durant son tour"
                
        return msg

    

    def get_case_attaquable(self,joueur_nom: str):
        """
        Renvoie une liste des ID des cases qui sont directement à côté des cases appartenant à 'joueur_nom'.
        
        Meme réflexion que dans le code de GestionMenu.check_adjacent()
        
        Args:
            joueur_nom (str): Le nom du joueur (exemple : "Joueur", "Ennemi 1").
        
        Returns:
            List[int]: Une liste des IDs des cases adjacentes attaquables.
        """
        attaquable_cases = []
        visited = set()  # Pour éviter de visiter plusieurs fois la même case
        
        joueur_cases = self.canvas_map.find_withtag(joueur_nom)
        
        for case_id in joueur_cases:
            coords = self.canvas_map.coords(case_id)
            x, y = coords[0], coords[1]
            
    
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
                    
                    for adj_id in overlapping_items:
                        # Vérifier que la case adjacente n'est pas déjà visitée et qu'elle n'appartient pas au joueur
                        if adj_id <= self.taille_map*self.taille_map and adj_id not in visited and not self.canvas_map.gettags(adj_id)[1] == joueur_nom:
                            attaquable_cases.append(adj_id)
                            visited.add(adj_id)
    
        return attaquable_cases
    
    def get_plaine_joueur(self, joueur_nom):
        """
        Retourne une liste des IDs des cases de type "plaine" appartenant au joueur donné.
    
        """
        plaine = []
    
        # Récupérer tous les IDs des cases appartenant au joueur
        case_joueur = self.canvas_map.find_withtag(joueur_nom)
    
        # Parcourir les IDs pour trouver ceux qui ont le tag "plaine"
        for case_id in case_joueur:
            if "plaine" in self.canvas_map.gettags(case_id):
                plaine.append(case_id)
    
        return plaine

        