
# -- encoding:utf-8 --
"""
Create by ibf on 2018/5/8
"""
 
from scipy.linalg import norm, pinv
import numpy as np
 
from matplotlib import pyplot as plt
 
from sklearn.cluster import KMeans
 
np.random.seed(28)
 
 
# TODO: 基于TensorFlow实现实现一下RBF神经网络的结构。
 
class RBF:
    """
    RBF径向基神经网络
    """
 
    def __init__(self, input_dim, num_centers, out_dim):
        """
        初始化函数
        :param input_dim: 输入维度数目
        :param num_centers: 中间的核数目
        :param out_dim:输出维度数目
        """
        self.input_dim = input_dim
        self.out_dim = out_dim
        self.num_centers = num_centers
        # 初始化产生一个中心点坐标列表(占位用的)
        self.centers = [np.random.uniform(-1, 1, input_dim) for i in range(num_centers)]
 
        self.beta = 8
        # 初始化一个权重列表
        self.W = np.random.random((self.num_centers, self.out_dim))
 
    def _basisfunc(self, c, d):
        return np.exp(-self.beta * norm(c - d) ** 2)
 
    def _calcAct(self, X):
        # calculate activations of RBFs
        G = np.zeros((X.shape[0], self.num_centers), float)
 
        for ci, c in enumerate(self.centers):
            print(ci,c)
            for xi, x in enumerate(X):
                # print(xi,x)
                G[xi, ci] = self._basisfunc(c, x)
 
        print(np.asarray(G).shape)
        return G
 
    def train(self, X, Y):
        """
        进行模型训练
        :param X: 矩阵，x的维度必须是给定的n * input_dim
        :param Y: 列的向量组合，要求维度必须是n * 1
        :return:
        """
        # 随机初始化中心点(permutation API的作用是打乱顺序，如果给定的是一个int类型的数据，那么打乱range(int)序列)
        temp=np.random.permutation(X.shape[0])
        rnd_idx = temp[:self.num_centers]
        self.centers = [X[i] for i in rnd_idx]
        # a=[]
        # for i in rnd_idx:
        #     a.append(X[i,:])
        #
        # self.centers.append(a)
 
        # 基于KMeans进行中心点获取
        kmeans_x = np.hstack((X, Y))
        print(np.asarray(kmeans_x).shape)
        # kmeans_x = X
        kmeans = KMeans(n_clusters=self.num_centers)
        kmeans.fit(kmeans_x)
        centers = np.asarray(kmeans.cluster_centers_[:, 0]).reshape((self.num_centers, 1))
        self.centers = centers
 
        print("中心点坐标:")
        print(self.centers)
 
        # calculate activations of RBFs
        # 相当于计算RBF中的激活函数值
        G = self._calcAct(X)
 
        # calculate output weights (pseudoinverse)
        # 计算权重(pinv API：计算矩阵的逆) ==> Y=GW ==> W = G^-1Y
        self.W = np.dot(pinv(G), Y)
 
    def test(self, X):
        """ X: matrix of dimensions n x indim """
        G = self._calcAct(X)
        Y = np.dot(G, self.W)
        return Y
 
 
# 构造数据
n = 1000
x = np.linspace(-1, 1, n).reshape(n, 1)
y = np.sin(3 * (x + 0.5) ** 3 - 1)
# y = y + np.random.normal(0, 0.1, n).reshape(n, 1)
 
# RBF神经网络
# 参数分别为：输入层的神经元数目、隐藏的神经元数目(中心点的数目)、输出层的神经元数目
rbf = RBF(1, 10, 1)
rbf.train(x, y)
z = rbf.test(x)
 
# plot original data
plt.figure(figsize=(12, 8))
# 展示原始值，黑色
plt.plot(x, y, 'k-')
 
# plot learned model
# 展示预测值
plt.plot(x, z, 'r-', linewidth=2)
 
plt.xlim(-1.5, 1.5)

# ————————————————
# 版权声明：本文为CSDN博主「txb_doyourbest」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/txb_doyourbest/article/details/106261046