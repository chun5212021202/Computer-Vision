import cv2
import numpy as np
import matplotlib.pyplot as plt

lena_shift = cv2.imread('lena.jpg', 0)
lena = np.asarray( np.delete( np.delete(lena_shift, 0 ,0), 0, 1 ) ,dtype=np.float64)#511,511
lena_shift = np.asarray( np.delete(np.delete(lena_shift, -1, 0),- 1, 1) ,dtype=np.float64)#511,511

print lena.shape
print lena_shift.shape





height, width = lena.shape
iteration = 64	#1 4 16 64
Lambda = 10	#0.1 1 10

Ex = np.zeros((height-1, width-1),dtype=np.float64)#510,510
Ey = np.zeros((height-1, width-1),dtype=np.float64)#510,510
Et = np.zeros((height-1, width-1),dtype=np.float64)#510,510

for j in range(height-1) :
	for i in range(width-1) :

		x = 0.25*( lena.item((i+1,j)) + lena_shift.item((i+1,j)) + lena.item((i+1,j+1)) + lena_shift.item((i+1,j+1)) ) - 0.25*( lena.item((i,j)) + lena_shift.item((i,j)) + lena.item((i,j+1)) + lena_shift.item((i,j+1)) )
		y = 0.25*( lena.item((i,j+1)) + lena_shift.item((i,j+1)) + lena.item((i+1,j+1)) + lena_shift.item((i+1,j+1)) ) - 0.25*( lena.item((i,j)) + lena_shift.item((i,j)) + lena.item((i+1,j)) + lena_shift.item((i+1,j)) )
		t = 0.25*( lena_shift.item((i,j)) + lena_shift.item((i,j+1)) + lena_shift.item((i+1,j)) + lena_shift.item((i+1,j+1)) ) - 0.25*( lena.item((i,j)) + lena.item((i,j+1)) + lena.item((i+1,j)) + lena.item((i+1,j+1)) )

		Ex.itemset( (i,j), x )
		Ey.itemset( (i,j), y )
		Et.itemset( (i,j), t )



U = np.zeros((iteration, height-1, width-1),dtype=np.float64)
V = np.zeros((iteration, height-1, width-1),dtype=np.float64)


for n in range(iteration) :
	U_bar = cv2.boxFilter(U[n-1], -1, (3,3))
	V_bar = cv2.boxFilter(V[n-1], -1, (3,3))
	#print U_bar
	#print V_bar
	for j in range(height-1) :
		for i in range(width-1) :

			u = U_bar.item((i,j)) - ( Ex.item((i,j))*U_bar.item((i,j)) + Ey.item((i,j))*V_bar.item((i,j)) + Et.item((i,j)) ) * Ex.item((i,j)) / ( 1 + Lambda*(Ex.item((i,j))**2 + Ey.item((i,j))**2 ) )
			v = V_bar.item((i,j)) - ( Ex.item((i,j))*U_bar.item((i,j)) + Ey.item((i,j))*V_bar.item((i,j)) + Et.item((i,j)) ) * Ey.item((i,j)) / ( 1 + Lambda*(Ex.item((i,j))**2 + Ey.item((i,j))**2 ) )
			U.itemset( (n,i,j), u )
			V.itemset( (n,i,j), v )
	print 'iter: ' , n

print U[-1]
print V[-1]

cv2.imshow('a',U[-1]**2+V[-1]**2)
cv2.imwrite('64_10.png',U[-1]**2+V[-1]**2)
cv2.waitKey(0)
"""
#######################################################
#													  #
#		         		PLOT						  #
#                                                     #
#######################################################
X, Y = np.meshgrid(np.arange(0, 520, 1), np.arange(0, 520, 1))



plt.figure()
Q = plt.quiver(X, Y, U[-1], V[-1],
            color='b', units='x',
            linewidths=(0.5,), edgecolors=('k'), headaxislength=0.5)
qk = plt.quiverkey(Q, 0.5, 0.03, 1, r'$1 \frac{m}{s}$',
            fontproperties={'weight': 'bold'})
plt.axis([-25, 550, -25, 550])
plt.title("1")
plt.show()
"""
