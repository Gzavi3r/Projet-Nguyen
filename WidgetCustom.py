# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 21:40:32 2024

@author: Brice
"""

import tkinter as tk

#j'ai trouvé la methode principale sur https://stackoverflow.com/questions/30489308/creating-a-custom-widget-in-tkinter et j'ai continué de me renseigner sur d'autre site

class Spinbox_Custom(tk.Frame):
    """
    Permet de créer une spinbox avec plusieur niveau d'indentation et qui accepte que la valeur minimal == valeur maximal
    """
    def __init__(self, master, from_, to, font=None, command=None, bg=None, **kwargs):
        super().__init__(master, **kwargs)
        # Modifie les valeurs de la frame
        self.config(relief="sunken", bd=2, bg=bg)
        
        self.min_value = from_
        self.max_value = to
        self.current_value = from_
        self.font = font
        self.command = command  # La fonction à appeler lors du changement de valeur
        self.bg = bg
        
        # Label pour afficher la valeur
        self.label = tk.Label(self,relief="ridge",bd = 2, text=str(self.current_value), width=3, bg='white', font=self.font)
        self.label.grid(row=1, column=2)
        
        
        # Créer une image sur 1 pixel pour pouvoir ajuster la taille des boutons au pixel près (n'a pas l'air de marcher sur Linux)
        #j'ai trouvé cette methode sur https://stackoverflow.com/questions/66391266/is-it-possible-to-reduce-a-button-size-in-tkinter
        self.pixel = tk.PhotoImage(width=1, height=1)

        # Bouton pour diminuer la valeur (pas 1)
        self.decrease_button = tk.Button(
            self, text="↓", image=self.pixel, compound="center", width=10, height=8,
            command=lambda n=1: self.decrease(n)
        )
        self.decrease_button.grid(row=2, column=0)

        pas1 = tk.Label(self, text="1", width=2, font=self.font, bg=self.bg)
        pas1.grid(row=1, column=0)

        # Bouton pour augmenter la valeur (pas 1)
        self.increase_button = tk.Button(
            self, text="↑", image=self.pixel, compound="center", width=10, height=8,
            command=lambda n=1: self.increase(n)
        )
        self.increase_button.grid(row=0, column=0)

        # Bouton pour diminuer la valeur (pas 5)
        self.decrease_button_5 = tk.Button(
            self, text="↓", image=self.pixel, compound="center", width=10, height=8,
            command=lambda n=5: self.decrease(n)
        )
        self.decrease_button_5.grid(row=2, column=1)

        pas5 = tk.Label(self, text="5", width=1, font=self.font, bg=self.bg)
        pas5.grid(row=1, column=1)

        # Bouton pour augmenter la valeur (pas 5)
        self.increase_button_5 = tk.Button(
            self, text="↑", image=self.pixel, compound="center", width=10, height=8,
            command=lambda n=5: self.increase(n)
        )
        self.increase_button_5.grid(row=0, column=1)

    def decrease(self, pas):
        if self.current_value - pas >= self.min_value:
            self.current_value -= pas
        else:
            self.current_value = self.min_value
        self.update_label()
        if self.command:
            self.command()  # Appel de la fonction command

    def increase(self, pas):
        if self.current_value + pas <= self.max_value:
            self.current_value += pas
        else:
            self.current_value = self.max_value
        self.update_label()
        if self.command:
            self.command()  # Appel de la fonction command

    def update_label(self):
        self.label.config(text=str(self.current_value))

    def get(self):
        return self.current_value
    
class Button_Custom(tk.Canvas):
    """
    Créé un bouton avec:
        text_config = un tuple avec (le texte principal, la couleur, la police)
        valeur1 = un tuple avec (la valeur de gauche, la couleur, la police)
        image1 = une image tkinter qui sera palcée à droite de valeur1
        valeur2 = un tuple avec (la valeur de droite, la couleur, la police)
        image2 = une image tkinter qui sera palcée à droite de valeur2
    
    les autres parametres sont identique à ceux des boutons tkinter classique     

    la methode _calcul_width calcule automatiquement la largeur du bouton si elle n'est pas explicitement donnée 
    la methode _draw_text créé et place automatiquement les widgets pour afficher le texte et les images
    

    la methode .set_state(state) correspond a .config(state)
    la methode .get_text() revoie le texte principal de text_config
    la methode .get_state() renvoie l'etat actuelle du bouton (normal ou disabled) 
    
    """
    def __init__(self, parent, text, valeur1= None, image1=None, valeur2=None, image2=None, width = None, height=25, bg="white", command=None, state=tk.NORMAL, **kwargs):
        self.command = command
        self.text_config = text
        self.valeur1 = valeur1
        self.image1 = image1
        self.valeur2 = valeur2
        self.image2 = image2
        self.default_bg = bg
        self.disabled_bg = "#e0e0e0"  # Couleur de fond désactivée
        self.separateur = ("/","black","Arial 20")
        self.default_text_color = text[1]
        if self.valeur1 != None:
            self.default_val1_color = valeur1[1]
            self.default_val2_color = valeur2[1]
        self.disabled_text_color = "#a0a0a0"  # Texte grisé pour état désactivé
        self.state = state

        super().__init__(parent, height=height, bg=bg, highlightthickness=0, **kwargs)
        self.config(relief="raised", bd=2)
        
        if width == None:
            self.calcul_width()
        else:
            self.config(width = width)

        self._draw_text()
        self.bind_events()
        
    def bind_events(self):
        """Associe les événements au bouton."""
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)


    def set_state(self, state):
        """Change l'état du bouton entre NORMAL et DISABLED."""
        self.state = state
        if self.state == tk.DISABLED:
            self["bg"] = self.disabled_bg
            self.text_config = (self.text_config[0], self.disabled_text_color, self.text_config[2])  # Change couleur texte
            if self.valeur1 != None:
                self.valeur1 = (self.valeur1[0], self.disabled_text_color, self.valeur1[2])
                self.separateur = (self.separateur[0], self.disabled_text_color, self.separateur[2])
                self.valeur2 = (self.valeur2[0], self.disabled_text_color, self.valeur2[2])
            
            self.unbind("<Button-1>")
        else:
            self["bg"] = self.default_bg
            self.text_config = (self.text_config[0], self.default_text_color, self.text_config[2])  # Restaure couleur texte
            if self.valeur1 != None:
                self.valeur1 = (self.valeur1[0], self.default_val1_color, self.valeur1[2])
                self.separateur = (self.separateur[0], "black", self.separateur[2])
                self.valeur2 = (self.valeur2[0], self.default_val2_color, self.valeur2[2])
            self.bind_events()

        self._draw_text()  # Redessiner le bouton

    def calcul_width(self):
        """Calcule la largeur nécessaire pour tout le contenu."""
        
        x_offset = 3
        if self.valeur1 != None:
            elements = [self.text_config, self.valeur1, self.valeur2]
        else:
            elements = [self.text_config]
        for element in elements:
            texte, _, font = element
            text_id = self.create_text(0, 0, text=texte, anchor="w", font=font, tags="tmp")
            bbox = self.bbox(text_id)
            x_offset += bbox[2] - bbox[0] + 5  # Largeur du texte + marge
            self.delete("tmp")
        if self.valeur1 != None:
            x_offset += self.image1.width() + self.image2.width() + 10  # Marge pour les images
        self.config(width = x_offset) 

    def _draw_text(self):
        """Dessine le texte avec la police et la couleur donnée ."""
        self.delete("all")

        x_offset = 3
        y_offset = self.winfo_reqheight() // 2

        # Texte principal
        texte, color, font = self.text_config
        text_id = self.create_text(x_offset, y_offset, text=texte, anchor="w", fill=color, font=font)
        bbox = self.bbox(text_id)
        x_offset = bbox[2] + 3
        if self.valeur1 != None:
            # Valeur 1 et image 1
            texte, color, font = self.valeur1
            text_id = self.create_text(x_offset, y_offset, text=texte, anchor="w", fill=color, font=font)
            bbox = self.bbox(text_id)
            x_offset = bbox[2] + 3
            self.create_image(x_offset, y_offset - 13, anchor=tk.NW, image=self.image1)
            x_offset += self.image1.width() + 2
            texte, color, font = self.separateur
            text_id = self.create_text(x_offset, y_offset, text=texte, anchor="w", fill=color, font=font)
            bbox = self.bbox(text_id)
            x_offset = bbox[2] + 3
    
            # Valeur 2 et image 2
            texte, color, font = self.valeur2
            text_id = self.create_text(x_offset, y_offset, text=texte, anchor="w", fill=color, font=font)
            bbox = self.bbox(text_id)
            x_offset = bbox[2] + 4
            self.create_image(x_offset, y_offset - 13, anchor=tk.NW, image=self.image2)

    def _on_click(self, event):
        """Gestion du clic."""
        if self.state == tk.DISABLED:
            return
        self["relief"] = "sunken"
        

    def _on_release(self, event):
        """Réinitialise le relief après le clic."""
        if self.state == tk.DISABLED:
            return
        self["relief"] = "raised"
        # Vérifie si la souris est toujours sur le bouton
        widget_under_mouse = self.winfo_containing(event.x_root, event.y_root)
        if widget_under_mouse == self:
            if self.command:
                self.command()



    def get_text(self):
        """Récupère le texte actuel."""
        return self.text_config[0]
    
    def get_state(self):
        return self.state
    
    def manque_argent(self):
        """met la valeur1 en rouge"""
        self.valeur1 = (self.valeur1[0], "red", self.valeur1[2])
        self._draw_text()
    
    def manque_ressource(self):
        """met la valeur2 en rouge"""
        self.valeur2 = (self.valeur2[0], "red", self.valeur2[2])
        self._draw_text()
    
    def set_valeur(self,valeur1,valeur2):
        self.valeur1 = valeur1
        self.valeur2 = valeur2
        self._draw_text()
   