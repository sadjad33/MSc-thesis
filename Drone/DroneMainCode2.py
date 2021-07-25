from DroneInitCode1 import Reopening_prog


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


R = Reopening_prog(O_k=t_O_k, D_s= t_D_s, initial_network= t_initial_network,
    ants_condition_org= t_ants_condition_org, ants_depot_org= t_ants_depot_org,
    pathtime_remained_org= t_pathtime_remained_org, ants_link_org= t_ants_link_org,
    max_n= t_max_n, big_M= t_big_M, beta= t_beta, rho= t_rho, scale= t_scale)

print(R)




