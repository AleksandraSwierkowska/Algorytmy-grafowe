import random
import time
import numpy as np
import math
def merge_sort_main(a):
    b = []
    for x in range(len(a)):
        b.append(0)
    merge_sort(a, 0, len(a), b)
    return a[::-1]


def merge_sort(a, l, r, b):
    m = (l + r)//2
    if (m - l) > 0:
        merge_sort(a, l, m, b)

    if (r - m) > 1:
        merge_sort(a, m, r, b)

    i = l
    j = m

    for k in range(l, r):
        if ((i < m) and (j >= r)) or ((i < m) and (j < r) and a[i] <= a[j]):
            b[k] = a[i]
            i = i + 1
        else:
            b[k] = a[j]
            j = j + 1

    for k in range(l, r):
        a[k] = b[k]

def greedy(v,w,c):
    n = len(v) #n-ilość przedmiotów
    weight = [] #lista stosunków v - wartości do w - wag
    for i in range(n):
        weight.append((v[i]/w[i], w[i], i))
    weight = merge_sort_main(weight)
    taken = 0 #zajętość plecaka - ile już włożyliśmy
    ans = [] #odpowiedź
    suma = 0
    for i in range(n):
        place = c - taken  # ile miejsca zostało
        if weight[i][1] <= place:
            ans.append(weight[i][2]) #dodajemy nr przedmiotu
            suma+=v[i]
            taken+=weight[i][1]
    return ans, suma

def dynamic(v, w, c):
    n=len(v)
    K = [[0 for x in range(c + 1)] for x in range(n + 1)] #tworzymy tablicę 0
    for i in range(n + 1):
        for j in range(c + 1):
            if i == 0 or j == 0:
                K[i][j] = 0
            elif w[i - 1] <= j:
                max = v[i - 1] + K[i - 1][j - w[i - 1]]
                if K[i - 1][j] > max:
                    max = K[i - 1][j]
                K[i][j] = max
            else:
                K[i][j] = K[i - 1][j]
    ans = []
    i = n
    x = c
    while i>0 and x>0:
        if K[i][x] != K[i-1][x]:
            ans.append(i-1)
            x-=w[i-1]
        i-=1
    return ans, K[n][c]

tries_number = 10
start_int = 10000
step = 20
cap = round(math.log(start_int+7, 2))
g_time = np.array([0.0] * 15)
g_value = np.array([0.0] * 15)
d_time = np.array([0.0] * 15)
d_value = np.array([0.0] * 15)
for x in range(tries_number):
    capacity = cap
    for i in range(15):
        values = list(range(1, start_int))
        weights = list(range(1, start_int))
        random.shuffle(weights)
        random.shuffle(values)

        start = time.time()
        max = greedy(values, weights, capacity)[1]
        stop = time.time()
        g_time[i]+=stop-start
        g_value[i]+=max
        #print(nmb, len(ans))

        start = time.time()
        max = dynamic(values, weights, capacity)[1]
        stop = time.time()
        d_time[i] += stop - start
        d_value[i] += max
        #print(nmb, len(ans))

        capacity+=step
        print(x,i)

g_time/=tries_number
g_value/=tries_number
d_time/=tries_number
d_value/=tries_number

error = (d_value-g_value)/d_value

print(list(g_time))
#print(list(g_value))
print(list(d_time))
#print(list(d_value))
print(list(error))
