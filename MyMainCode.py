from azinfunctions import *
import random
from math import exp
### step 0 - initializing:
# CarNetwork = [link no., i, j, t, h]
# here is '3 node 6 link network':
initial_network = [
	[0, 0, 1, 4, 0],
	[1, 1, 0, 4, 60],
	[2, 0, 2, 8, 0],
	[3, 2, 0, 8, 50],
	[4, 1, 2, 3, 30],
	[5, 2, 1, 3, 0]
	]
# here is Ok (rescue teams in each node k) and Ds (demand in each node s):
O_k = [1, 2, 0]
D_s = [58.3, 11.68, 131.25]
# travel time for damaged links in network:
big_M = 30

max_n = 80
beta = .5
rho = .5

# finding damaged links in the network
damaged_links = [item for item in initial_network if item[-1] != 0]


### step 1 - Calculation of initial pheromone and visibility for damaged links:
# initial pheromone tau(0) of each damaged link:
tau = [[1 for times in range(max_n)] for link in damaged_links]
# tau is matrix with l rows and n columns

# visibility of each damaged link:
def link_visibility():
	#	 Vl = Σ[(Ok*Ds)/(tks_b)] - Σ[(Ok*Ds)/(tks_-l)]
	# this function returns an array of l item (Vl).
	vis = []
	base = 0
	for i, ok in enumerate(O_k):
	    for j, ds in enumerate(D_s):
	        if i != j: 
	            tks_b = shortest_path(origin= i, car_network_sp= initial_network)[0][j]
	            base += (ok * ds)/(tks_b)

	for l in damaged_links:
	#	 creating a network without l:
	    no_l_network = [item[:] for item in initial_network]
	#    print(initial_network)
	    no_l_network[l[0]][3] = big_M
	#    print(no_l_network)
	    no_l = 0
	    for i, ok in enumerate(O_k):
	        for j, ds in enumerate(D_s):
	            if i != j and ok != 0:
	                tks_no_l = shortest_path(origin= i, car_network_sp= no_l_network)[0][j]
	#                print(f'k= {i+1}, s= {j+1}')
	                no_l += (ok * ds)/(tks_no_l)
	#                print(f'tks= {tks_no_l}')
	#    print(f'l= ({l[1]+1}, {l[2]+1}) , no_l= {no_l}')
	    vis.append(base - no_l)
	#	 vis = [visibility of first dmgd link, ..., visibility of last dmgd link]
	# 	 visibility should not be greater than 1
	scaled_visibility = []
	for item in vis:
		scaled_visibility.append(item/max(vis))
	return(scaled_visibility)

def utility():
	# utility function:
	u = []
	for i, link in enumerate(tau):
		u.append([])
		for tau_nl in link:
			u[i].append(tau_nl + rho * link_visibility[i])
	# u matrix is like tau matrix
	return(u)




def ant_choose_link(pmnl):
	''' pmnl is a cumulative multidimensional matrix of probability of choosing link l
	by ant m in time n
	pmnl = [[p101, p102, p103],
			[p201, p202, p203],
			[p301, p302, p303]]
	'''
	choosen_link = []
	for ant in pmnl:
		rnd = random.random()
		if rnd <= ant[0]:
			choosen_link.append(0)
		elif rnd <= ant[1]:
			choosen_link.append(1)
		elif rnd <= ant[2]:
			choosen_link.append(3)
	'''this func. returns an array called "choosen link"
	choosen_link[m] = the link which is choosen by ant m for reopening'''
	return(choosen_link)


