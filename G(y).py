m_matrix = [
    [   [17, [4, 8, 30, 30]],   #a #21
        [33, [4, 7, 30, 3]],    #b
        [57, [4, 7, 4, 3]],     #c
        [81, [4, 7, 4, 3]]],    #d
    [   [17, [4, 8, 30, 30]],   #a #22
        [40, [4, 7, 30, 3]],    #b
        [54, [4, 7, 4, 3]],     #c
        [81, [4, 7, 4, 3]]],    #d
    [   [17, [4, 8, 30, 30]],   #a #23
        [42, [4, 7, 30, 3]],    #b
        [51, [4, 7, 11, 3]],    #c
        [81, [4, 7, 4, 3]]],    #d
    [   [30, [4, 8, 30, 30]],   #a #24
        [32, [4, 7, 30, 3]],    #b
        [53, [4, 7, 4, 3]],     #c
        [81, [4, 7, 4, 3]]]     #d
        ]
D = [11.67, 131.25, 58.3, 131.25]
g_lst = []
counter = 20

def P4_solving(M):
    '''   M = [
            [upper_bound a, [t12(a), t13(a), t21(a), t23(a)]]
            [upper_bound b, [t12(b), t13(b), t21(b), t23(b)]]
            [upper_bound c, [t12(c), t13(c), t21(c), t23(c)]]
            [upper_bound d, [t12(d), t13(d), t21(d), t23(d)]]
        ]
    '''
    G = 0
    for i in M:
        if M.index(i) == 0:
            lower = 0
        else:    
            lower = upper
        upper = i[0]
        ks = 0
        for tks in i[1]:
            if tks != 30:
                Ds = D[ks]
                for x in range(lower, upper):
                    G += Ds*(.8 - ((x + tks)/900))
            ks += 1
    return(G)    

for M1 in m_matrix:
    counter += 1
    g_lst.append([counter ,round(P4_solving(M1))])
print(g_lst)