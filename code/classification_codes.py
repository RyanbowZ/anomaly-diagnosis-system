#暂且先把所有代码放在一个文件里面，之后需要调整再滴滴我

#1.随机森林
#train
from sklearn.ensemble import RandomForestClassifier
clf=RandomForestClassifier(n_estimators=200)
clf.fit(train_x,train_y)
#test
y_pre=clf.predict(test_x.reshape(-1,1))

#2.主成分分析
#train
from sklearn.decomposition import PCA
pca = PCA(n_components=n_components,svd_solver='randomized',whiten=True).fit(X_train)
X_trian_pca = pca.transform(train_x)
clf = pca.fit(X_trian_pca,train_y)
#test
X_test_pca = pca.transform(test_x.reshape(-1,1))
y_pred = clf.predict(X_test_pca)

#3.高斯过程
#train
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()
clf.fit(train_x, train_y)
#test
y_pre = clf.predict(test_x.reshape(-1,1))


#4.K最近邻
#train
from sklearn.neighbors import KNeighborsClassifier
knn=KNeighborsClassifier()
knn.fit(train_x,train_y)
#test
predict_y = knn.predict(test_x.reshape(-1,1))
