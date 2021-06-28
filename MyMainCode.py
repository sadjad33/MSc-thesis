from azinfunctions import *
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

# finding damaged links in the network
damaged_links = [item for item in initial_network if item[-1] != 0]


### step 1 - Calculation of initial pheromone and visibility for damaged links:
# initial pheromone tau(0) of each damaged link:
tau = [1 for link in damaged_links]

# visibility of each damaged link:
def link_visibility():
#	Vl = Σ[(Ok*Ds)/(tks_b)] - Σ[(Ok*Ds)/(tks_-l)]
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
	return(vis)