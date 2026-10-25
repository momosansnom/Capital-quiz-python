import matplotlib.pyplot as plt
import numpy as np
from random import randint

# Chargement de l'image de la carte
carte = plt.imread('carte.jpg')
carac = np.shape(carte)

# Ouverture du fichier csv en mode lecture
F     = open('Donnees.csv','r') 
D   = []
cap = []
for ligne in F: # Parcours du fichier ligne par ligne
    L = ligne.split(",")
    D.append(L)
    cap.append(L[1])

# Conversion de de latitude(str) en degrés(float)
def Lat_str2degre(latt):
    val = latt.split("°")
    t   = val[1].split("'")
    tab = [int(val[0]),int(t[0])]
    if t[1]=='N':
        phi = tab[0]+tab[1]/60
    elif t[1]=='S':
        phi = -(tab[0]+tab[1]/60)
    return phi

# Conversion de de longitude(str) en degrés(float)
def Long_str2degre(longt):
    val = longt.split("°")
    t   = val[1].split("'")
    tab = [int(val[0]),int(t[0])]
    if t[1][0]=='E':
        tetha = tab[0]+tab[1]/60
    elif t[1][0]=='W':
        tetha = -(tab[0]+tab[1]/60)
    return tetha

# Passage des coordonnées géographiques (latitude ,longitude) au repère de l'image (ligne, colonne)
def GPS2image(la,lon):
    l = -carac[0]/180*la+carac[0]/2
    c = carac[1]/360*lon+carac[1]/2
    return l,c

# Passage repère de l'image (ligne, colonne) aux coordonnées géographiques (latitude ,longitude) 
def image2GPS(l,c):
    la  = -180/carac[0]*l+90
    lon = 360/carac[1]*c-180
    return lon,la

# Calcul de la distance d'un arc de cercle sur la sphère terrestre
def distance(theta):
    r = 6371
    d = r*theta
    return d

# Conversion des coordonnées GPS en coordonnées cartésiennes
def GPS2coord(lat,long):
    r = 6371
    latrad  = lat*2*np.pi/360
    longrad = long*2*np.pi/360
    x = r*np.cos(latrad)*np.cos(longrad)
    y = r*np.cos(latrad)*np.sin(longrad)
    z = r*np.sin(latrad)
    return x,y,z

# Calcul de l'angle theta entre les 2 points via le produit scalaire
def angle(latA,longA,latB,longB):
    r = 6371
    coord1 = GPS2coord(latA,longA)
    coord2 = GPS2coord(latB,longB)
    theta  = np.arccos((coord1[0]*coord2[0]+coord1[1]*coord2[1]+coord1[2]*coord2[2])/(r**2))
    return theta

# Calcul global de la distance la plus courte entre les 2 points
def LongArc(latA,longA,latB,longB):
    thetaglob = angle(latA,longA,latB,longB)
    dis       = distance(thetaglob)
    return dis

# Variables d'état du jeu
etat      = 0
score_tot = 0
nb_tours  = 0

# Choix aléatoire de la capital à deviner
chx_idx   = randint(0, len(D)-1) 

# Boucle pour les clics sur la carte
def on_key(event):
    if event.key in ['q', 'escape']:
        plt.close()
    print(f"vous avez joué pendant {nb_tours} tours avec un score total de {score_tot}")
    
def onclick(event):
    global etat, score_tot, nb_tours, chx_idx
    
    if event.xdata is None or event.ydata is None:
        return
    # Evaluation de la réponse
    if etat == 0:
        l_joueur, c_joueur = event.ydata, event.xdata
        lon_joueur, lat_joueur = image2GPS(l_joueur, c_joueur)
        
        lat_reelle = Lat_str2degre(D[chx_idx][2])
        lon_reelle = Long_str2degre(D[chx_idx][3])
        l_reel, c_reel = GPS2image(lat_reelle, lon_reelle)
        
        dist = LongArc(lat_reelle, lon_reelle, lat_joueur, lon_joueur)
        score_tot += dist
        nb_tours += 1
        
        plt.plot([c_reel], [l_reel], 'ro', label="Capitale")
        plt.plot([c_joueur], [l_joueur], 'bo', label="Votre choix")
        plt.plot([c_reel, c_joueur], [l_reel, l_joueur], 'k--')
        
        plt.title(f"{cap[chx_idx]} - Distance : {dist:.0f} km\nScore : {score_tot/nb_tours:.0f}")
        plt.legend()
        plt.draw()
        
        etat = 1
    # Réinitialisation et nouvelle manche    
    elif etat == 1:
        plt.clf()
        plt.imshow(carte)
        chx_idx = randint(0, len(D)-1)
        plt.title(f"{cap[chx_idx]} ?")
        plt.draw()
        etat = 0

# Affichage initial de la carte et de la capital à trouver
fig = plt.figure()
plt.imshow(carte)
plt.title(f"{cap[chx_idx]} ?")
fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()


