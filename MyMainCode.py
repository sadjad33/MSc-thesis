from azinfunctions import shortest_path
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


n_network = [
	[[0, 0, 1, 4],
	[1, 1, 0, 60],
	[2, 0, 2, 8],
	[3, 2, 0, 50],
	[4, 1, 2, 30],
	[5, 2, 1, 3]]
	]

ants_condition = [1, 1, 1]

ants_depot = [1, 1, 0] 		# ant condition = 1
ants_inpath = [-1, -1, -1] 	# ant condition = 2
ants_link = [-1, -1, -1] 	# ant condition = 3



nodes = set([link[1] for link in initial_network] 
		+ [link[2] for link in initial_network])
	# here is Ok (rescue teams in node k) and Ds (demand in node s):
O_k = [1, 2, 0]
D_s = [58.3, 11.68, 131.25]
	# travel time for damaged links in network:
big_M = 30

max_n = 8
beta = .5
rho = .5

	# finding damaged links in the network
damaged_links = [item for item in initial_network if item[-1] != 0]


### Step 1 - Calculation of initial pheromone
		# and visibility for damaged links:
	# initial pheromone tau(0) of each damaged link:
tau = [[1 for times in range(max_n)] for link in damaged_links]
	# tau is a matrix with l rows and n columns

	# visibility of each damaged link:
def link_visibility():
	#	Vl = Σ[(Ok*Ds)/(tks_b)] - Σ[(Ok*Ds)/(tks_-l)]
		# this function returns an array of l item (Vl).
		#
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
	# 	 visibility should not be greater than 1:
	scaled_visibility = []
	for item in vis:
		scaled_visibility.append(item/max(vis))
	return(scaled_visibility)

### Step 2 - Calculating the probability of selecting links for ants:


def utility():
	u_array = [[0 for i in links] for links in tau]
	# utility function:
	for i, link in enumerate(tau):
		for j, tau_nl in enumerate(link):
			u_array[i][j] = (tau_nl + beta * link_visibility()[i])
	# u matrix is like tau
	# (with l rows and n columns)
	return(u_array)


def L(n_L, i_L):
	# 	it gets n (time) as input and returns L array
		# L is an array of i items (nodes of the network)
		# each item is an array, which contains nodes that 
		# can be accessed at time n from node i. (just first nodes
		# of damaged links)

		## IT RETURNS THE ARRAY OF ACCESSIBLE DAMAGED LINKS 
		## FOR REOPENING FOR THE ANTS IN NODE I AT TIME N

	L_array = []
	network = n_network[n_L]
	shortest_time_i = shortest_path(origin= i_L, car_network_sp= network)[0]
	for link in damaged_links:
		if shortest_time_i[link[1]] < big_M:
			L_array.append(link)
	return(L_array)

def choosen_link(n_p, i_p):
	#	it takes n (time) and i (ant depot) as input
	u_n = [utility()[links][n_p] for links in range(len(tau))]
	prob = []
	L_node = L(n_L= n_p, i_L= i_p)
	p_denominator = 0
	for link in L_node:
		link_index = damaged_links.index(link)
		p_denominator += exp(u_n[link_index])
	for link in L_node:
		link_index = damaged_links.index(link)
		prob.append(exp(u_n[link_index])/p_denominator)

	# "prob" is an array contains probability of
	# damaged links for choosing in time n, by ants 
	# which are depoted in node i.
	''' prob = p(l) = [p1, p2]'''

	# creating cumulative probability array from prob array
	cum_prob = []
	for i, p in enumerate(prob):
		if i == 0:
			cum_prob.append(p)
		else:
			cum_prob.append(p + cum_prob[i-1])

	rnd = random()

	for i, p in enumerate(cum_prob):
		if rnd < p:
			choosen = L_node[i]
			break
	return(choosen)
	# this function returns one of the "damaged_links" which is choosen
	# by an ant in depot node i at the time n
	



for n in range(max_n):
	for ant_no, ant_state in enumerate(ants_condition):
		if ant_state = 1:
			depot = ants_depot[ant_no]
			open_link = choosen_link(n_p= n, i_p= depot)
			start_node = open_link[1]
			time_to_link = shortest_path(origin= depot, 
				car_network_sp= n_network[n])[0][start_node]
			if time_to_link == 0:
				ants_condition[ant_no] = 3
			else:
				ants_condition[ant_no] = 2


		elif ant_state = 2:

		elif ant_state =3:

