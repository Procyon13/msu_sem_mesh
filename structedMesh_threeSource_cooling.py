import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import time
from datetime import timedelta
import math


def InCircle(X, Y, X0, Y0, A):
    if (X - X0)**2 + (Y - Y0)**2 <= A**2:
        return True
    else:
        return False
    
def NewPoint(X, Y, X_Left, X_Right, Y_Left, Y_Right, i):
    if i == 0:
        return [(X + X_Left) / 2, (Y + Y_Right) / 2]
    if i == 1:
        return [X, (Y + Y_Right) / 2]
    if i == 2:
        return [(X + X_Right) / 2, (Y + Y_Right) / 2]
    if i == 3:
        return [(X + X_Right) / 2, Y]
    if i == 4:
        return [(X + X_Right) / 2, (Y + Y_Left) / 2]
    if i == 5:
        return [X, (Y + Y_Left) / 2]
    if i == 6:
        return [(X + X_Left) / 2, (Y + Y_Left) / 2]
    if i == 7:
        return [(X + X_Left) / 2, Y]
    
def RemoveDuplicates(Points):
    temp_set = set()
    temp_points = []
    
    for point in Points:
        t = tuple(point)
        if t not in temp_set:
            temp_points.append(point)
            temp_set.add(t)
            
    return temp_points

def DataSource(X, Y, X0, Y0, A):
    rez = []
    new_point = []
    
    for x_idx in range(0, np.size(X)):
        for y_idx in range(0, np.size(Y)): 
            if A != 0:
                if InCircle(X[x_idx], Y[y_idx], X0, Y0, A) and x_idx + 1 != np.size(X) and y_idx + 1 != np.size(Y):
                    for i in range(8):
                        new_point = NewPoint(X[x_idx], Y[y_idx], X[x_idx-1], X[x_idx+1], Y[y_idx-1], Y[y_idx+1], i)
                        if InCircle(new_point[0], new_point[1], X0, Y0, A):
                            rez.append(new_point) 
            else:
                rez.append([X[x_idx], Y[y_idx]])
    
    return np.array(RemoveDuplicates(rez), dtype=float)

def DataSource_reduce(Data, X0, Y0, A, H):
    rez = []
    
    if A - H > 0: 
        for num_point in range(0, np.size(Data, 0)):
            if InCircle(Data[num_point][0], Data[num_point][1], X0, Y0, A-H):
                rez.append([Data[num_point][0], Data[num_point][1]])
    else:
        rez = np.zeros((1, 2))
    
    return np.array(rez, dtype=float)



x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)

#???????????????????? ???????????? ?????????????????????? 1, 2 ?? 3
x0_1, y0_1 = 0.5, 0.5
x0_2, y0_2 = 0.3, 0.7
x0_3, y0_3 = 0.8, 0.8
#???????????? ?????? ?????????????????????? 1, 2 ?? 3
r1, r2, r3 = 0., 0., 0.
#??????, ?? ?????????????? ???????????? ???????????? ?????? ?????????????????????? 1, 2 ?? 3
h1, h2, h3 = 0.07, 0.05, 0.01

#???????????????????????? ???????????? ?????? ????????????????
max_r = 0.5
#?????????? ????????????????
i = 0

#???????????? ??????????????????????
size_fig = 50

#?????????????????????????????????? ??????????
DataSructedMesh = DataSource(x, y, 0, 0, 0)

#?????????????? ??????????????
start_time = time.time()


#????????????????????
while max(r1, r2, r3) < max_r_it:
    DataCircle_1 = DataSource(x, y, x0_1, y0_1, r1)
    DataCircle_2 = DataSource(x, y, x0_2, y0_2, r2)
    DataCircle_3 = DataSource(x, y, x0_3, y0_3, r3)
    Data = np.array(RemoveDuplicates(np.vstack([DataSructedMesh, DataCircle_1, DataCircle_2, DataCircle_3])), dtype=float)
    
    simplices = Delaunay(Data).simplices
    
    plt.figure(figsize=(size_fig, size_fig))
    plt.triplot(Data[:, 0], Data[:, 1], simplices, color='r')
#     plt.scatter(Data[:, 0], Data[:, 1], color='r')
#     plt.savefig('image_structedMesh_threeSource_cooling/test_' + str(i) + '.png')
    plt.show()
    
    print('R1 = ', r1, ', R2 = ', r2, ', R3 = ', r3)
    r1 = round(r1 + h1, 2)
    r2 = round(r2 + h2, 2)
    r3 = round(r3 + h3, 2)
    
    i += 1
    

#????????????????????
while max(r1, r2, r3) > 0:
    if r1 > 0:
        DataCircle_1 = DataSource_reduce(DataCircle_1, x0_1, y0_1, r1, h1)
    if r2 > 0:
        DataCircle_2 = DataSource_reduce(DataCircle_2, x0_2, y0_2, r2, h2)
    if r3 > 0:
        DataCircle_3 = DataSource_reduce(DataCircle_3, x0_3, y0_3, r3, h3)
    Data = np.array(RemoveDuplicates(np.vstack([DataSructedMesh, DataCircle_1, DataCircle_2, DataCircle_3])), dtype=float)
    
    simplices = Delaunay(Data).simplices
    
    plt.figure(figsize=(size_fig, size_fig))
    plt.triplot(Data[:, 0], Data[:, 1], simplices, color='b')
#     plt.scatter(Data[:, 0], Data[:, 1], color='r')
    
    plt.savefig('image_structedMesh_threeSource_cooling/test_' + str(i) + '.png')
    i -= 1
    
    plt.show()
    
    r1 = round(r1 - h1, 2)
    r2 = round(r2 - h2, 2)
    r3 = round(r3 - h3, 2)
    print('R1 = ', r1, ', R2 = ', r2, ', R3 = ', r3)
    
    
#?????????? ?????????????????? ?????????????? ???? ??????????    
elapsed_time_secs = time.time() - start_time
msg = "Execution took: %s secs" % timedelta(seconds=round(elapsed_time_secs))
print(msg)