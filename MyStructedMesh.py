import numpy as np
import matplotlib.pyplot as plt

class Mesh(object):
    
    def __init__(self, size):
        """Constructor"""
        # размерность сетки
        self.size = size
        
        # координаты x и y 
        x = np.linspace(0, 1, self.size)
        y = np.linspace(0, 1, self.size)
        
        # все вершины
        self.vertices = []
        for x_idx in range(0, np.size(x)):
            for y_idx in range(0, np.size(y)):
                self.vertices.append([y[y_idx], x[x_idx]])
        
        # набор идентификаторов вершин, в которыйх сходятся диагонали большой квадратной сетки
        # далее называю узлами
        self.nodes = []
        
        # набор троек идентификаторов вершин соединенные в треуголькики
        self.simplices = []

    def add_new_simplex(self, vertex_id, i):
        if i == 0:
            return [vertex_id - self.size - 1, vertex_id - self.size, vertex_id]
        if i == 1:
            return [vertex_id - self.size, vertex_id - self.size + 1, vertex_id]
        if i == 2:
            return [vertex_id - self.size + 1, vertex_id, vertex_id + 1]
        if i == 3:
            return [vertex_id, vertex_id + 1, vertex_id + self.size + 1]
        if i == 4:
            return [vertex_id, vertex_id + self.size, vertex_id + self.size + 1]
        if i == 5:
            return [vertex_id, vertex_id + self.size - 1, vertex_id + self.size]
        if i == 6:
            return [vertex_id - 1, vertex_id, vertex_id + self.size - 1]
        if i == 7:
            return [vertex_id - self.size - 1, vertex_id - 1, vertex_id]
    
                    
    def simplices_generation(self):
        for vertex_id_0 in range(1, self.size, 2):
            for vertex_id_nsize in range(self.size + vertex_id_0, len(self.vertices), self.size*2):
                self.nodes.append(vertex_id_nsize)
                # последняя строка, не добавляются верхние половины диагоналей
                if vertex_id_nsize > len(self.vertices) - self.size:
                    self.simplices.append(self.add_new_simplex(vertex_id_nsize, 0))
                    self.simplices.append(self.add_new_simplex(vertex_id_nsize, 7))
                    # последняя строка, последний столбец, не добавляются верхние и правая половины диагоналей
                    if vertex_id_0 != self.size - 1:
                        self.simplices.append(self.add_new_simplex(vertex_id_nsize, 1))
                        self.simplices.append(self.add_new_simplex(vertex_id_nsize, 2))
                
                # последний столбец, не добавляются правые половины диагоналей
                elif vertex_id_0 == self.size - 1:
                    self.simplices.append(self.add_new_simplex(vertex_id_nsize, 0))
                    for i in range(5,8):
                        self.simplices.append(self.add_new_simplex(vertex_id_nsize, i))
                # добавляются все половины диагоналей
                else: 
                    for i in range(8):
                        self.simplices.append(self.add_new_simplex(vertex_id_nsize, i))


class AdaptiveMesh(Mesh):
    
    def generation_additional_simplices(self, r, x0, y0):
        # проходим по всем узлам, лежащим внутри окружности
        #print(self.nodes_in_circle(r, x0, y0))
        for node in self.nodes_in_circle(r, x0, y0):
            new_simplex_it = 0   
            # строим новую вершину на середине полудиагонали, если внешний угол входит в окружность 
            for new_vertex_it in range(4):  
                if self.in_circle(self.diagonal_vertex(node, new_vertex_it), r, x0, y0):
                    new_vertex_id = self.add_new_vertex(node, self.diagonal_vertex(node, new_vertex_it)) 
                    # строим 4 новых треугольника
                    for it in range(4):
                        self.add_additional_simplex(node, new_vertex_id, new_simplex_it)
                        new_simplex_it += 1
                else:
                    new_simplex_it += 4
    
    # идентификатор внешнего угла большого квадрата
    def diagonal_vertex(self, node, i):
        if i == 0:
            return node - self.size + 1
        if i == 1:
            return node + self.size + 1
        if i == 2:
            return node + self.size - 1
        if i == 3:
            return node - self.size - 1
    
    def add_new_vertex(self, vertex_id_1, vertex_id_2):
        self.vertices.append([self.midpoint_coordinate(vertex_id_1,vertex_id_2,0), self.midpoint_coordinate(vertex_id_1,vertex_id_2,1)])
        return len(self.vertices) - 1
    
    # формула вычисления координаты середины отрезка
    def midpoint_coordinate(self, vertex_id_1, vertex_id_2, dim):
        return (self.vertices[vertex_id_1][dim] + self.vertices[vertex_id_2][dim]) / 2
    
    # проверка, находится ли точка внутри окружности
    def in_circle(self, vertex_id, r, x0, y0):
        if (self.vertices[vertex_id][0] - x0)**2 + (self.vertices[vertex_id][1] - y0)**2 <= r**2:
            return True
        else:
            return False
    
    # составить набор узлов, которые находятся внутри окружности
    def nodes_in_circle(self, r, x0, y0):
        temp = []
        for vertex_id in self.nodes:
            if self.in_circle(vertex_id, r, x0, y0):
                temp.append(vertex_id)
        return temp
    
    def add_additional_simplex(self, node, new_vertex_id, i):
        if i == 0:
            self.simplices.append([node - self.size, node - self.size + 1, new_vertex_id])
        if i == 1:
            self.simplices.append([node - self.size + 1 , node + 1, new_vertex_id])
        if i == 2:
            self.simplices.append([node, node + 1, new_vertex_id])
        if i == 3:
            self.simplices.append([node - self.size, node, new_vertex_id])
        if i == 4:
            self.simplices.append([node, node + 1, new_vertex_id])
        if i == 5:
            self.simplices.append([node + 1, node + self.size + 1, new_vertex_id])
        if i == 6:
            self.simplices.append([node + self.size, node + self.size + 1, new_vertex_id])
        if i == 7:
            self.simplices.append([node, node + self.size, new_vertex_id])
        if i == 8:
            self.simplices.append([node, node + self.size, new_vertex_id])
        if i == 9:
            self.simplices.append([node + self.size - 1, node + self.size, new_vertex_id])
        if i == 10:
            self.simplices.append([node - 1, node + self.size - 1, new_vertex_id])
        if i == 11:
            self.simplices.append([node - 1, node, new_vertex_id])
        if i == 12:
            self.simplices.append([node - 1, node, new_vertex_id])
        if i == 13:
            self.simplices.append([node - self.size - 1, node - 1, new_vertex_id])
        if i == 14:
            self.simplices.append([node - self.size - 1, node - self.size, new_vertex_id])
        if i == 15:
            self.simplices.append([node - self.size, node, new_vertex_id])
                
 
if __name__ == "__main__":
    size = 100
    r, x0, y0 = 0.2, 0.5, 0.5
    mesh = AdaptiveMesh(size)
    mesh.simplices_generation()
    mesh.generation_additional_simplices(r, x0, y0)
    
    Data = np.array(mesh.vertices, dtype=float)
    plt.figure(figsize=(50, 50))   
    plt.triplot(Data[:, 0], Data[:, 1], mesh.simplices, color='r')
    plt.scatter(Data[:, 0], Data[:, 1], color='k')
    
    plt.show()