import networkx as nx
import pdb as pd
import numpy as np
#Importing the edgelist
fh=open('karate.edgelist','rb')
g=nx.read_edgelist(fh)
print g
fh.close()
#Building the adjacency matrix
'''a=nx.adjacency_matrix(g)'''
a=np.array([[1,1,1,0,0],[1,1,1,0,0],[1,1,1,0,0],[0,0,0,1,1],[0,0,0,1,1]])

# this function is for random walk with Resistance and passing the a numpy array to it
def rws(a, epsilon=None, beta=None, stop_value=None):
    

    nodes = a.shape[0]

    if not stop_value:
        stop_value = 1.0 / np.mean(np.sum(a, axis=1))
    if not beta:
        beta = 1.0 / np.mean(np.sum(a, axis=1)) / nodes
    if not epsilon:
        epsilon = 1.0 / np.sum(np.sum(a, axis=1)) / np.mean(np.sum(a, axis=1))

    m,n = a.shape
   # a=a.toarray()
    d=np.eye(m)
   
   
    aa = np.maximum(a,d)

    bb = np.sum(aa, axis=1)
    bb = 1.0 / bb

    cc = np.outer(np.ones((m,1)),bb) * aa

    cc = cc.T


    cc[ np.isnan(cc) ] = 0

    current = np.eye(m)
    newcurrent = current.copy()

    active = np.ones((m,1))

    step = 0
    improve_count = 0
    active_nodes = 0

    improve = np.ones((n,1))
    while np.sum(active) > 0.0:
        print(step, np.sum(active), improve_count)
    	active_nodes = np.sum(active)
    	current = newcurrent

    	curr_act = np.dot(active, np.ones((1,m)))*current
    	curr_stop=(np.dot(active,np.ones((1,m)))-1)*current

    	sel = (((np.dot(current,cc)>0).astype(np.int)-(current>0).astype(np.int))==1).astype(np.int)
    	
    	
    	
    	temp = np.dot(curr_act,cc)-(sel*( np.dot((curr_act>0).astype(np.int),aa) )*beta)
    	temp = temp*(temp>0).astype(np.int)
    	newcurrent = temp


        newcurrent=temp;
        
        newcurrent=newcurrent*(newcurrent>(beta*cc)).astype(np.int)
        
        
        newcurrent=newcurrent-np.dot((current>0).astype(int),aa)*epsilon
        newcurrent=newcurrent*(newcurrent>0).astype(np.int)
     

        newcurrent=newcurrent-curr_stop;
        newcurrent=np.outer((1/np.sum(newcurrent.T, axis=0)).T,np.ones((1,nodes)))*newcurrent #normalize
        
        improve=np.sum(np.abs(current-newcurrent), axis=1)
        
        active=np.reshape( (improve>stop_value).astype(np.int), active.shape )
        
        if active_nodes == np.sum(active):
            improve_count=improve_count+1
        else:
        	improve_count=0
       
        step=step+1

        if improve_count>1:
            break

    
    return current
# This returns the resistance matrix 
resistancematrix=rws(a)
