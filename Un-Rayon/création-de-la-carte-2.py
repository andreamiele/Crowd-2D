from tkinter import *

class CreerCarte:
    """interface graphique pour donner une carte"""
    

    def __init__(self):
        self.affichage=Tk() #la fenetre graphique
        self.affichage.title('Dessinons ensemble une map')
        self.etat=0          #à quel stade on en est
        self.prems=True      #si le point que l'on place est le premier d'un segment
        self.points=[]       #les points délimitant des murs
        self.sorties=[]      #idem pour des sorties
        self.debut=(0,0)     #un premier point que l'on garde en mémoire
        self.sorties_finale=[]
        self.carte_finale=np.array([[(0,2) for i in range(250)] for j in range(250)])
        self.mecs=[]
        
        #Modif perso
        
        #fin
        self.bouton=Button(self.affichage, text="passer à la sortie", command=self.suivant)
        self.bouton.pack()
        
        self.canvas = Canvas(self.affichage, width=250, height=250,bg='papaya whip', cursor="cross")
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>",self.point)
        self.affichage.mainloop()
    
    
    def point(self,event):
        x,y=event.x,event.y
        if self.prems and self.etat!=2:
            self.debut=(x,y)
            self.prems=False
        elif self.etat!=2:
            if self.etat==0:
                self.canvas.create_line(self.debut,(x,y), fill='midnight blue')
            else:
                self.canvas.create_line(self.debut,(x,y),fill='forest green')
            self.prems=True
        else:
            self.mecs.append((x,y))
            self.canvas.create_oval((x-1,y-1,x+1,y+1),outline='deep pink')
        if self.etat==0:
            self.points.append((x,y))
        elif self.etat==1:
            self.sorties.append((x,y))
    
    
    def suivant(self):
        #modif
        if self.etat==0:
            
            self.bouton["text"]="placer les gens"
            #Modif perso
            
            
            
            
            
            self.etat=1
        elif self.etat==1:
            self.bouton["text"]="quitter"
            #Modif perso
           
            self.etat=2
        else:
            self.affichage.destroy()
            while self.points!=[]:
                d=self.points.pop()
                c=self.points.pop()
                ajout_ligne(self.carte_finale,c,d)
            while self.sorties!=[]:
                sortie_complete(self.sorties_finale,self.sorties)
            affichage(self.carte_finale,self.sorties_finale)
            simulation(self.carte_finale,self.sorties_finale,self.mecs)

##
def ajout_ligne(mat,c,d):
    a,b=c
    x,y=d
    if x<a:
        a,b,x,y=x,y,a,b
    if x==a:
        for j in range(b,y+1):
            mat[(a,j)][1]=1
    elif y-b>x-a:
        for j in range(b,y+1):
            mat[(int(a+(x-a)*(j-b)/(y-b)),j)][1]=1
    elif y-b>a-x:
        for i in range(a,x+1):
            mat[(i,int(b+(y-b)*(i-a)/(x-a)))][1]=1
    else:
        for j in range(y,b+1):
            mat[(int(a+(x-a)*(j-b)/(y-b)),j)][1]=1
##
def sortie_complete(s,out):
    d=out.pop()
    c=out.pop()
    a,b=c
    x,y=d
    if x<a:
        a,b,x,y=x,y,a,b
    if x==a:
        for j in range(b,y+1):
            s.append((a,j))
    elif y-b>x-a:
        for j in range(b,y+1):
            s.append((int(a+(x-a)*(j-b)/(y-b)),j))
    elif y-b>a-x:
        for i in range(a,x+1):
            s.append((i,int(b+(y-b)*(i-a)/(x-a))))
    else:
        for j in range(y,b+1):
            s.append((int(a+(x-a)*(j-b)/(y-b)),j))
            
CreerCarte()