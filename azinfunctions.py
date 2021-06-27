from scipy.optimize import linprog

def shortest_path(origin,car_network_sp):
	# CarNetwork = [link no.,  i,  j,  a,  b,  x,  t,  length]
	'''If there are n nodes and m links in the network,
	the numbering of nodes and links must start from 0 and continue to n-1 (or m-1).'''
	t = [item[3] for item in car_network_sp] #3rd. column of the network is link's travel time
	numofnodes = len(set([item[1] for item in car_network_sp]+[item[2] for item in car_network_sp]))
	numoflinks = len(car_network_sp)
	proposal = []
	ol = 0
	i = origin
	time = [float('inf') for i in range(numofnodes)] #all nodes time is infinity
	check_subset = [node for node in range(numofnodes)] #Uninvestigated Nodes Susbet
	label = [-1 for i in range(numofnodes)]
	time[origin] = 0
	del check_subset[origin]
	counter = 1

	while True:
		g = len(check_subset)
		if len(check_subset) == 0:
			#label[origin] = origin
			break
		#1. updating and Labling next node	
		for j in range(numoflinks): 
			if car_network_sp[j][1] == i:
				if time[car_network_sp[j][2]] > time[i] + car_network_sp[j][3]:
					label[car_network_sp[j][2]] = i #yani labele gere ghablesh ro bezar "i".
					time[car_network_sp[j][2]] = time[i] + car_network_sp[j][3]
		#2. Finding min t
		min_time = time[check_subset[0]] #primary min time amount
		min_time_node = check_subset[0] #min time primary place of array --- shomare gere
		for h in range(g):
			if time[check_subset[h]] < min_time:
				min_time = time[check_subset[h]]
				min_time_node = check_subset[h]
				ol = len(proposal)
			for ku in range(len(proposal)):
				if proposal[ku] == min_time_node:
					break
			proposal = []
			proposal = list(set(proposal))
			ol = len(proposal)

		for h in range(g):	
			if time[check_subset[h]] != float('inf') and min_time_node != check_subset[h]:
				ol += 1
				proposal.append(check_subset[h])
		proposal = list(set(proposal))
		ol = len(proposal)
		if min_time == float('inf'):
			for re in range(ol):
				if time[proposal[re]] < min_time:
					min_time = time[proposal[re]]
					min_time_node = proposal[re]
		i = min_time_node
		g = len(check_subset)
		if i not in check_subset:
			break
		#3. Remove investigated node
		for h in range(g): 
			if check_subset[h] == i:
				v = h
		del check_subset[v]
		counter += 1


	return (time, label)


#here are 2 test network for checking the shortest path function:
'''network = [
	[0, 0, 1, 4],
	[1, 0, 2, 4],
	[2, 1, 2, 1],
	[3, 2, 3, 1],
	[4, 1, 3, 3],
	[5, 1, 0, 4],
	[6, 2, 0, 4],
	[7, 2, 1, 1],
	[8, 3, 2, 1],
	[9, 3, 1, 3],]
'''
'''network = [
	[0, 0, 1, 50],
	[1, 1, 3, 100],
	[2, 0, 3, 120],
	[3, 1, 2, 60],
	[4, 3, 2, 50],
	[5, 3, 5, 125],
	[6, 3, 4, 70],
	[7, 5, 4, 70],
	[8, 2, 4, 90],
	[9, 1, 0, 50],
	[10, 3, 1, 100],
	[11, 3, 0, 120],
	[12, 2, 1, 60],
	[13, 2, 3, 50],
	[14, 5, 3, 125],
	[15, 4, 3, 70],
	[16, 4, 5, 70],
	[17, 4, 2, 90],
	]'''
'''print(shortest_path(car_network_sp = network, origin = 0))'''

def all_or_nothing(car_network_aon, ODq):
	# ODQ is only one row: ( [i j demand] )
	# CarNetwork = [link no.,  i,  j,  a,  b,  x,  t,  length]
	'''If there are n nodes and m links in the network,
	the numbering of nodes and links must start from 0 and continue to n-1 (or m-1).'''
	numofnodes = len(set([item[1] for item in car_network_aon]+[item[2] for item in car_network_aon]))
	numoflinks = len(car_network_aon)
	flow = [0 for link in range(numoflinks)]
	lbl = shortest_path(origin=ODq[0], car_network_sp=car_network_aon)[1]
	# why ODq[0]? cause it wants to find shortest path TREE from root i
	path = [ODq[1]]
	'''path = sequence of shortest path nodes
	(and destination is first node. next node is destination's lable)'''
	# Making Sequence of nodes
	for node in range(numofnodes):
		path.append(lbl[path[-1]])
		if lbl[path[-1]] == -1:
			break

	# Assign demand to shortest path
	for node in range(len(path) - 1):
		for j in range(numoflinks):
			if car_network_aon[j][2] == path[node] and car_network_aon[j][1] == path[node + 1]:
				flow[j] = ODq[2]

	return(flow)


'''print(all_or_nothing(car_network_aon=network, ODq=[0, 2, 5]))'''
def transportation(k, s, car_network_t):
	'''this function solves a transportation problem
	from k nodes to s nodes with known supply & demand '''
	# k = [node no., teams in node, p]
	# s =[node no., As, gs, qs, Ds]
	t = [item[3] for item in car_network_t] #3rd. column of the network is link's travel time
	numofnodes = len(set([item[1] for item in car_network_t]+[item[2] for item in car_network_t]))
	numoflinks = len(car_network_t)
	label = [[0 for item in range(numofnodes)] for item in range(len(k))]
	time = [[0 for item in range(numofnodes)] for item in range(len(k))]
	wq = [[0 for item in range(len(s))] for item in range(len(k))]
	
	for j in range(len(k)):
		time[j], label[j] = shortest_path(car_network_sp= car_network_t, origin= k[j][0])

	for i in range(len(k)):
		for j in range(len(s)):
			wq[i][j] = time[i][s[j][0]]

	f = []
	for i in range(len(s)):
		for j in wq:
			f.append(j[i])

	aeq = [[0 for item in range(len(s)*len(k))] for item in range(len(k)+len(s))]

	for o in range(len(k)):
		for l in range(len(s)):
			aeq[o][l * len(k) + o] = 1

	for u in range(len(s)):
		for il in range(len(k)):
			aeq[u + len(k)][u * len(k) + il] = 1
	
	beq = [item[1] for item in k]
	for item in s:
 		beq.append(item[4])

	bound = [(0, None) for i in range(len(s)*len(k))]

 	
	x = linprog(f, A_eq=aeq, b_eq=beq, bounds=bound).x

	ty = 0
	fr = 0

	demand = []

	for we in range(len(s)):
		for re in range(len(k)):
			if round(x[fr], 2) > 0:
				demand.append([k[re][0], s[we][0], round(x[fr], 2)])
				ty += 1
			fr += 1

	return(demand, time, wq)
'''network = [
	[0, 0, 1, 4],
	[1, 0, 2, 4],
	[2, 1, 2, 1],
	[3, 2, 3, 1],
	[4, 1, 3, 3],
	[5, 1, 0, 4],
	[6, 2, 0, 4],
	[7, 2, 1, 1],
	[8, 3, 2, 1],
	[9, 3, 1, 3],]

ka = [
	[0, 10, .5],
	[2, 6, .5]
	]
es = [
	[0, 0, 0, 0, 1],
	[1, 0, 0, 0, 7],
	[2, 0, 0, 0, 3],
	[3, 0, 0, 0, 5],
	]

tr = transportation(k= ka, s= es, car_network_t= network)
print(tr[0])'''


