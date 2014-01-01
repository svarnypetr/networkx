import networkx as nx
from itertools import combinations


__author__ = """Huston Hedinger (h@graphalchemist.com)"""
__all__ = ['dispersion_centrality']


def dispersion_centrality(G, u, v=None, exclude_nodes=None, normalized=True):
    """ A python implementation of 'dispersion' as defined by Lars Backstrom
    and Jon Kleinberg here: http://arxiv.org/pdf/1310.6753v1.pdf
    
    Parameters
    ----------
    G : graph
      A NetworkX graph
    u : node, required
      the ego node of the network
    v : node, optional
      Return only the dispersion value for node v
    exclude_nodes : list of nodes, optional
      Exclude nodes from score
    normalized : bool, optional
      If True (default) normalize by the embededness of the nodes (u and v).
    """

    G_u = G
    dispersion = dict.fromkeys(G_u, 0)

    for v in G_u:
        if v == u:
            continue
        u_nbrs = G[u]
        ST = set(n for n in G[v] if n in u_nbrs)
        
        embededness = len(ST)

        possib = combinations(ST, 2)
        total = 0
        #each possible path between s and t
        for p in possib:
            s = p[0]
            t = p[1]
            neighbors_s = G_u[s]
            neighbors_t = G_u[t]
            Q = []
            for n in neighbors_s:
                #if one of the neigbors is t, no dispersion tick
                if (n == t):
                    score = False
                    break
                #if one of the neighbors is not the ego node, or the node we are
                #scoring dispersion for, add them to the que    
                elif (n != u) and (n != v):
                    Q.append(n)
                #if one of the neigbors is ego or test node, continue because dispersion
                #allows them to connect to other nodes in the network
                elif (n == u) or (n == v):
                    score = True
            #traverse the nodes in the Q       
            if score:
                while Q:
                    i = Q.pop(0)
                    #make sure that s is not directly connected to t
                    #s--t
                    if (i == t):
                        score = False
                        break
                    #make sure that s does not share a neighbor with t
                    #s--i--t
                    elif i in neighbors_t:
                        score = False
                        break
                    #continue looping

            #if score is true for the 's' 't' on the possible path called 'p'
            #add a 1 for dispersion
            if score:
                total += 1

        if normalized == True:
            if embededness != 0:
                norm_disp = (total/embededness)
            elif embededness == 0:
                norm_disp = total
            dispersion[v] = {'norm_disp' : norm_disp}
        else:
            dispersion[v] = {'abs_disp': total}
    return dispersion
