def grad(distances,c):
    a,b=c
    a,b=int(a),int(b)
    if distances[(a-1,b)][1]==1:
        if distances[(a+1,b)][1]==1:
            x=0
        else:
            x=distances[(a+1,b)][0]-distances[(a,b)][0]
    elif distances[(a+1,b)][1]==1:
        x=distances[(a,b)][0]-distances[(a-1,b)][0]
    else:
        x=(distances[(a+1,b)][0]-distances[(a-1,b)][0])/2
    if distances[(a,b-1)][1]==1:
        if distances[(a,b+1)][1]==1:
            y=0
        else:
            y=distances[(a,b+1)][0]-distances[(a,b)][0]
    elif distances[(a,b+1)][1]==1:
        y=distances[(a,b)][0]-distances[(a,b-1)][0]
    else:
        y=(distances[(a,b+1)][0]-distances[(a,b-1)][0])/2
    if x**2+y**2>0:
        n=sqrt(x**2+y**2)
        x,y=x/n,y/n
    return((x,y))
##
def G(i,j,q,N,h): #vecteurs unitaires entre les différents points multiplié par le coefficient d'Euler
    res=np.zeros(2*N)
    a,b,c,d=q[2*i],q[2*i+1],q[2*j],q[2*j+1]
    norme=sqrt((a-c)**2+(b-d)**2)
    res[2*i],res[2*i+1]=h*(c-a)/norme,h*(d-b)/norme
    res[2*j],res[2*j+1]=h*(a-c)/norme,h*(b-d)/norme
    return(res)
##
def dis(i,j,q,r):  #distance entre deux points (en prenant en compte leur rayon)
    a,b,c,d=q[2*i],q[2*i+1],q[2*j],q[2*j+1]
    return(sqrt((a-c)**2+(b-d)**2)-2*r)
##
def vdist(q,r,N):  #toutes les distances
    res=[dis(i,j,q,r) for j in range(1,N) for i in range(j)]
    return(np.array(res))
##
def proj(u): #projeté sur R+
    n=len(u)
    res=np.array([0.]*n)
    for i,c in enumerate(u):
        if c>0:
            res[i]=c
    return(res)
##
def uzawa(us,q,h,N,r):
    if N>1:
        C=np.array([G(i,j,q,N,h) for j in range(1,N) for i in range(j)]) #matrice C de la méthode (c'est bien ça j'ai vérifié)
        rho=1/(N**2*h**2)                                                 #coefficient rho de la méthode
        lam=np.zeros(N*(N-1)//2)                                         #lambda de la méthode
        condition=True
        dist=vdist(q,r,N)
        while condition:
            v=us-np.dot(np.transpose(C),lam)                             #us est la vitesse souhaitée
            lam=proj(lam+rho*(np.dot(C,v)-dist))
            condition=False
            for c in vdist(q+h*v,r,N):
                if c<-r/10:
                    condition=True
    else:
        v=us
    return(v)
##
def vitesse_souhaitee(distance,vitesses,q,n):
    a=[]
    for i in range(n):
        a.append(vitesses[int(q[2*i])][int(q[2*i+1])])
    res=[]
    for c in a:
        a,b=c
        res.append(a)
        res.append(b)
    return(-1*np.array(res))
##
def gestion_graphique(mat,q,taille,N,sortie,vitesses):
    plt.clf()
    for i in range(1,taille):
        for j in range(1,taille):
            if mat[(i,j)][1]==1:
                plt.plot(i,j,marker='+',color='black')
    for i in range(N):
        plt.plot(q[2*i],q[2*i+1],marker='o',markersize=4,color='b')
    for c in sortie:
        a,b=c
        plt.plot(a,b,marker='*',color='r')

#%%
#           FONCTION DE SIMULATION


def simulation(mat,sortie,q0):
    q=[]
    for c in q0:
        a,b=c
        q.append(a)
        q.append(b)
    distances=carte_distance(mat,sortie)[0]
    N=len(q0)
    taille=len(mat)-1
    vitesses=[[(0,0)]*(taille+1)]+[[(0,0)]+[grad(distances,(i,j)) for j in range(1,taille)]+[(0,0)] for i in range(1,taille)]+[[(0,0)]*(taille+1)] # les trucs en + sont là pour les bords où la vitesse doit être nulle
    k=0
    #GIF_parts
    filenames = []

    
    while N!=0:
        k+=1
        gestion_graphique(mat,q,taille,N,sortie,vitesses)
        us=vitesse_souhaitee(distances,vitesses,q,N)
        v=uzawa(us,q,0.2,N,1)
        q=q+0.2*v
        sortis=[]
        for i in range(N):
            if (int(q[2*i]),int(q[2*i+1])) in sortie or (int(q[2*i])+1,int(q[2*i+1])) in sortie or (int(q[2*i]),int(q[2*i+1])+1) in sortie or (int(q[2*i])+1,int(q[2*i+1])+1) in sortie: #i est arrivé à la sortie
                sortis.append(i)
        if sortis!=[]:#il y a besoin d'actualiser q
            nouveau=[]
            for i in range(N):
                if i in sortis:
                    N-=1
                else:
                    nouveau.append(q[2*i])
                    nouveau.append(q[2*i+1])
            q=np.array(nouveau)
        
        #GIF_Parts_b    
        filename = 'C:\TIPE\Simulations\Images\Simulation_{}.png'.format(k)
        filenames.append(filename)
        #GIF_Parts_e 
        
        plt.savefig(filename)               #Sauvegarder le fichier dans le répertoire
        
        #GIF_Parts_b    
    with imageio.get_writer('C:\TIPE\Simulations\GIFs\GIF_Simulation.gif', mode='I') as writer:
       for filename in filenames:
           image = imageio.imread(filename)
           writer.append_data(image)
        #GIF_Parts_e    