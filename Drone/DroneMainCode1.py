from random import random
from math import exp


def shortest_path(origin, car_network_sp):
    # CarNetwork = [link no.,  i,  j,  t]
    '''If there are n nodes and m links in the network,
    the numbering of nodes and links should start from 0 and continue to n-1 (or m-1).'''
    t = [item[3] for item in car_network_sp]  # 3rd. column of the network is link's travel time
    numofnodes = len(set([item[1] for item in car_network_sp] + [item[2] for item in car_network_sp]))
    numoflinks = len(car_network_sp)
    proposal = []
    ol = 0
    i = origin
    time = [float('inf') for i in range(numofnodes)]  # all nodes time is infinity
    check_subset = [node for node in range(numofnodes)]  # Uninvestigated Nodes Susbet
    label = [-1 for i in range(numofnodes)]
    time[origin] = 0
    del check_subset[origin]
    counter = 1

    while True:
        g = len(check_subset)
        if len(check_subset) == 0:
            # label[origin] = origin
            break
        # 1. updating and Labling next node
        for j in range(numoflinks):
            if car_network_sp[j][1] == i:
                if time[car_network_sp[j][2]] > time[i] + car_network_sp[j][3]:
                    label[car_network_sp[j][2]] = i  # yani labele gere ghablesh ro bezar "i".
                    time[car_network_sp[j][2]] = time[i] + car_network_sp[j][3]
        # 2. Finding min t
        min_time = time[check_subset[0]]  # primary min time amount
        min_time_node = check_subset[0]  # min time primary place of array --- shomare gere
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
        # 3. Remove investigated node
        for h in range(g):
            if check_subset[h] == i:
                v = h
        del check_subset[v]
        counter += 1

    return time, label



def survival_function(t_w):
    return(.8 - ((t_w)/900))

# nodes = set([link[1] for link in initial_network]
#             + [link[2] for link in initial_network])

### Step 1 - Calculation of initial pheromone and visibility for damaged links:

# visibility of each damaged link:
def link_visibility(O_k_lv, D_s_lv, initial_network_lv, big_M_lv):
    #   Vl = Σ[(Ok*Ds)/(tks_b)] - Σ[(Ok*Ds)/(tks_-l)]
    # this function returns an array of l item (Vl).
    vis = []
    base = 0
    for i, ok in enumerate(O_k_lv):
        for j, ds in enumerate(D_s_lv):
            if i != j and ok != 0:
                tks_b = shortest_path(origin=i, car_network_sp=initial_network_lv)[0][j]
                base += (ok * ds) / (tks_b)
    damaged_links_lv = [item for item in initial_network_lv if item[-1] != 0]
    for l in damaged_links_lv:
        #    creating a network without l:
        no_l_network = [item[:] for item in initial_network_lv]
        #    print(initial_network)
        no_l_network[l[0]][3] = big_M_lv
        #    print(no_l_network)
        no_l = 0
        for i, ok in enumerate(O_k_lv):
            for j, ds in enumerate(D_s_lv):
                if i != j and ok != 0:
                    tks_no_l = shortest_path(origin=i, car_network_sp=no_l_network)[0][j]
                    #                print(f'k= {i+1}, s= {j+1}')
                    no_l += (ok * ds) / (tks_no_l)
        #                print(f'tks= {tks_no_l}')
        #    print(f'l= ({l[1]+1}, {l[2]+1}) , no_l= {no_l}')
        vis.append(base - no_l)
    #    vis = [visibility of first dmgd link, ..., visibility of last dmgd link]
    #    visibility should not be greater than 1:
    scaled_visibility = []
    for item in vis:
        scaled_visibility.append(item / max(vis))
    return (scaled_visibility)



### Step 2 - Calculating the probability of selecting links for ants:


def utility(tau_u, link_visibility_u, beta_u, scale_u):
    utility_u = [[0 for time in links] for links in tau_u]
    # utility function:
    for i, link in enumerate(tau_u):
        for j, tau_nl in enumerate(link):
            utility_u[i][j] = (tau_nl + beta_u * link_visibility_u[i]) * scale_u
    # u matrix is like tau (with l rows and n columns)
    return utility_u


def L(n_L, i_L, n_network_L, damaged_links_L, big_M_L):
    # it gets n (time) as input and returns L array
    # L is an array of i items (nodes of the network)
    # each item is an array, which contains nodes that
    # can be accessed at time n from node i. (just first nodes
    # of damaged links)

    ## IT RETURNS THE ARRAY OF ACCESSIBLE DAMAGED LINKS
    ## FOR REOPENING FOR THE ANTS IN NODE I AT TIME N

    L_array = []
    network = n_network_L[n_L]
    shortest_time_i = shortest_path(origin= i_L, car_network_sp= network)[0]
    for link in damaged_links_L:
        if shortest_time_i[link[1]] < big_M_L:
            L_array.append(link)
    return (L_array)


def chosen_link(n_p, i_p, tau_p, n_network_p,
    damaged_links_p, big_M_p, link_visibility_p,
    beta_p, scale_p):
    # this function returns one of the "damaged_links" which is chosen
    # by an ant in depot node i at the time n
    # it takes n (time) and i (ant depot) as input
    u_n = [utility(tau_u= tau_p, link_visibility_u= link_visibility_p,
        beta_u= beta_p, scale_u= scale_p)[links][n_p] 
    for links in range(len(damaged_links_p))]
    prob = []
    L_node = L(n_L=n_p, i_L=i_p, n_network_L= n_network_p,
        damaged_links_L= damaged_links_p, big_M_L= big_M_p)
    p_denominator = 0
    for link in L_node:
        link_index = damaged_links_p.index(link)
        p_denominator += exp(u_n[link_index])
    for link in L_node:
        link_index = damaged_links_p.index(link)
        prob.append(exp(u_n[link_index]) / p_denominator)

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
            cum_prob.append(p + cum_prob[i - 1])

    rnd = random()
    
    for i, p in enumerate(cum_prob):
        if rnd < p:
            chosen = L_node[i]
            break
    #print(f'prob= {prob}')
    #print(f'random= {rnd}')
    return chosen


def Reopening_prog(O_k, D_s, initial_network, big_M, max_n,
    ants_condition_org, ants_depot_org, pathtime_remained_org,
    ants_link_org, beta, rho, scale):
    ### Step 3 - Allocate ants and determine the reopening program (yn):

    iteration = 0
    G_best = 0
    all_G = []
    same_G = 0

    link_vis = link_visibility(O_k_lv= O_k, D_s_lv= D_s, 
        initial_network_lv= initial_network, big_M_lv= big_M)


    # initial pheromone tau(0) of each damaged link:
    # tau is a matrix with l rows and n columns
    tau = [[1 for times in range(max_n)] for link in initial_network if link[-1] != 0]


    while True:
        iteration += 1

        print('T=', iteration)

        # finding damaged links in the network
        damaged_links = [item for item in initial_network if item[-1] != 0]
        copy_damaged_links = [item for item in initial_network if item[-1] != 0]
        
        n_network = [[link.copy() for link in initial_network]]    
        for item in n_network:
            for link in item:
                if link[-1]!=0:
                    link[-2]=link[-1]
                link.pop()

        ants_condition = ants_condition_org.copy()
        ants_depot = ants_depot_org.copy()                  # ant condition = 1
        pathtime_remained = pathtime_remained_org.copy()    # ant condition = 2
        ants_link = ants_link_org.copy()                    # ant condition = 3
        link_with_ant = [[0 for times in range(max_n)] for link in damaged_links]
        link_time_to_finish = [item[-1] for item in initial_network]
        ants_link_result = [[0 for times in range(max_n)] for ants in ants_link]
        ant_choose = []

        for n in range(max_n):
            #print(f'time= {n}, ant state= {ants_condition}')
            for ant_no, ant_state in enumerate(ants_condition):
                if not damaged_links:
                    pass
                else:
                    if ant_state == 1:
                        #print(f'time= {n}')
                        #print(f'ant_no= {ant_no}')
                        depot = ants_depot[ant_no]
                        open_link = chosen_link(n_p= n, i_p= depot,
                            n_network_p= n_network, big_M_p= big_M, 
                            tau_p= tau, damaged_links_p= damaged_links, 
                            link_visibility_p= link_vis, 
                            beta_p= beta, scale_p= scale)
                        ant_choose.append([ant_no, n, open_link])
                        #print('open_link=', open_link)
                        start_node = open_link[1]
                        ants_link[ant_no] = open_link[0]
                        time_to_link = shortest_path(origin= depot,
                                                     car_network_sp= n_network[n])[0][start_node]
                        if time_to_link == 0:
                            ants_condition[ant_no] = 3
                            link_time_to_finish[ants_link[ant_no]] -= 1
                        else:
                            ants_condition[ant_no] = 2
                            pathtime_remained[ant_no] = time_to_link - 1
                        link_with_ant[damaged_links.index(open_link)][n] += 1
                    elif ant_state == 2:
                        if pathtime_remained[ant_no] <= 0:
                            ants_condition[ant_no] = 3
                            link_time_to_finish[ants_link[ant_no]] -= 1
                            #print('here we go')
                        else:
                            pathtime_remained[ant_no] -= 1
                        dmg_index = copy_damaged_links.index(initial_network[ants_link[ant_no]])
                        link_with_ant[dmg_index][n] += 1
                    elif ant_state == 3:
                        if link_time_to_finish[ants_link[ant_no]] > 0:
                            link_time_to_finish[ants_link[ant_no]] -= 1
                        if link_time_to_finish[ants_link[ant_no]] <= 0:
                            # If the first ant (from two ants working on one link) completes the   
                            # reopening operation, the second ant moves to another link at the same time.
                            for other_ants_no in range(len(ants_condition)):
                                if ants_link[ant_no] == ants_link[other_ants_no]:
                                    ants_condition[other_ants_no] = 1
                                    ants_depot[other_ants_no] = initial_network[ants_link[other_ants_no]][2]
                                    # print(initial_network[ants_link[ant_no]])
                                    # print('damaged_links=', damaged_links)
                            if initial_network[ants_link[ant_no]] in damaged_links:
                                damaged_links.remove(initial_network[ants_link[ant_no]])
                        dmg_index = copy_damaged_links.index(initial_network[ants_link[ant_no]])
                        link_with_ant[dmg_index][n] += 1

                    for i in range(len(ants_link)):
                        ants_link_result[i][n] = ants_link[i]
                    
            # updating n_network
            n_network.append([])
            for link in initial_network:
                link_tmp = link.copy()
                n_network[n + 1].append(link_tmp)
                if link_tmp in damaged_links:
                    n_network[n + 1][-1][3] = n_network[n + 1][-1][4]
                n_network[n + 1][-1].pop()



        # for i in ants_link_result:
        #     for j in i:
        #         antnetw.write(str(j) + "\t")
        #     antnetw.write('\n')
        # antnetw.write('\n')

            #print('n_network=', n_network[-1])

        ### Step 4 - Calculate travel time between each origin-destination at any time:

        tks_matrix = []
        for n in range(max_n):
            tks_matrix.append([])
            for i, ok in enumerate(O_k):
                for j in range(len(D_s)):
                    if i != j and ok != 0:
                        tksn = shortest_path(origin= i, car_network_sp= n_network[n])[0][j]
                        tks_matrix[-1].append(tksn)

        ### Step 5 - Calculate the objective function:

        G = 0
        Dks = []

        for i, ok in enumerate(O_k):
            for j, ds in enumerate(D_s):
                if i != j and ok != 0:
                    Dks.append(ds)

        for n in range(max_n):
            for s, t_ks in enumerate(tks_matrix[n]):
                if t_ks <= big_M:
                    G += Dks[s] * survival_function(n + t_ks)
        all_G.append(round(G))
        print(round(G))

        ### Step 6- Determining the pheromone of the links:
        G_y0 = 8648
        if G >= G_best:
            G_best = round(G)
            link_with_ant_best = [[j for j in i] for i in link_with_ant]
            delta_tau = (G_best - G_y0)/10000

        for link in range(len(tau)):
            for n in range(len(tau[link])):
                if link_with_ant_best[link][n] > 0:
                    tau[link][n] = rho * tau[link][n] + delta_tau
                else:
                    tau[link][n] *= rho
        

        # Additional Step- Avoiding local optima
        if len(all_G) > 3 and all_G[-1] == all_G[-2] == all_G[-3] == (G_best):
            same_G += 1
            
            # 2nd. stagnation (when the optimal solution is repeated
            # for 3 times) is stopping criteria
            if same_G > 1:
                break

            # calculating average tau of each n:
            avg_tau = []
            tmp_avg = 0
            for n in range(max_n):
                for link in range(len(tau)):
                    tmp_avg += (1/len(tau)) * tau[link][n]
                avg_tau.append(tmp_avg)
                tmp_avg = 0
            # round_to_tenths = [round(num, 3) for num in tau[0]]
            # print(round_to_tenths)
            
            # pheromone of links below the average level is added to avg. phr.,
            # and subtract avg. phr. from those above the average level.
            for link in range(len(tau)):
                for n in range(len(tau[link])):
                    if tau[link][n] > avg_tau[n]:
                        tau[link][n] -= avg_tau[n]
                    else:
                        tau[link][n] += avg_tau[n]
     

        # if iteration > 31:
        #     break

    print(G_best)
    print(ant_choose)


### step 0 - initializing:

t_initial_network = [
    [0, 0, 1, 4, 0],
    [1, 1, 0, 4, 60],
    [2, 0, 2, 8, 0],
    [3, 2, 0, 8, 50],
    [4, 1, 2, 3, 30],
    [5, 2, 1, 3, 0]
    ]


# here is Ok (rescue teams in node k) and Ds (demand in node s):
t_O_k = [1, 2, 0]
t_D_s = [58.3, 11.68, 131.25]

t_ants_condition_org = [1, 1, 1]
t_ants_depot_org = [1, 1, 0]          # ant condition = 1
t_pathtime_remained_org = [0, 0, 0]   # ant condition = 2
t_ants_link_org = [-1, -1, -1]        # ant condition = 3

# total time
t_max_n = 80

# travel time for damaged links in network:
t_big_M = 15

# ant system parameters:
t_beta = .4
t_rho = .5
t_scale = 5


Reopening_prog(O_k=t_O_k, D_s= t_D_s, initial_network= t_initial_network,
    ants_condition_org= t_ants_condition_org, ants_depot_org= t_ants_depot_org,
    pathtime_remained_org= t_pathtime_remained_org, ants_link_org= t_ants_link_org,
    max_n= t_max_n, big_M= t_big_M, beta= t_beta, rho= t_rho, scale= t_scale)



