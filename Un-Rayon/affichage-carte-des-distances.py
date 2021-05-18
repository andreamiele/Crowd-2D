#%%
#           FONCTION D'AFFICHAGE DE LA CARTE DES DISTANCES


def echelle(color_begin, color_end, n_vals):
    r1, g1, b1 = color_begin
    r2, g2, b2 = color_end
    degrade = []
    etendue = n_vals - 1
    for i in range(n_vals):
        alpha = 1 - i / etendue
        beta = i / etendue
        r = r1 * alpha + r2 * beta
        g = g1 * alpha + g2 * beta
        b = b1 * alpha + b2 * beta
        degrade.append((r, g, b))
    return degrade






def affichage(m,sortie):
    M,dm=carte_distance(m,sortie)
    coul=echelle((0,0,1),(0,1,0),50)+echelle((0,1,0),(1,0,0),50)
    for i,c in enumerate(M):
        for j,d in enumerate(c):
            if d[1]!="lim":
                plt.plot(i,j,marker='.',markersize=5,color=coul[int(100*(d[0]/(dm+5)))])
                if i>0 and j>0 and i<99 and j<99:
                    a,b=grad(M,(i,j))
                    plt.arrow(i,j,2*a,2*b)
    plt.show()