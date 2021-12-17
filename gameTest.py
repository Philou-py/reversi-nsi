import numpy as np

#Docstring patern:
#
#   """""
#   Function: 
#   Input: 
#   Return:
#   """""


tray= np.array([[0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,1,2,0,0,0],
                    [0,0,0,2,1,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]])
    
def trayDisplay(self): #Fonction de débug
        """""
        Function: Display the tray 
        Input: None
        Return: The actual tray
        """""
        print(self.tray)

def colorChange(self, x:int, y:int):
        """""
        Function: change the value of the cell a the x;y coordinate
        input: x coordinate, y coordinate
        return: none
        """""
        #on fait d'abord toute la logique pour 1 joueur et quand tout marchera on
        #poura rajouter le deuxième joueur
        self.tray[y,x]=1

def turn(self, x:int, y:int):
        """""
        Function: Calculate the cell that must be turned around
        Input: none
        Return: none
        """""
        #ici c'est la partie qui va être la plus compliqué
        #ce sera l'algo qui va calculer les pions qui doivent êtres retournés
        #je t'avoue que j'ai la méthode théorique mais je vois pas trop comment l'appliqué
        print(self.tray[x,y], self.tray[x+1,y])
        if self.tray[x+1,y] == self.tray[x,y]:
            print("test")

t=tray()

