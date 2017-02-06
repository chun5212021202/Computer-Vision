import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
start = time.time()

BLOCK = 31 #8 11 15 21 31
SEARCH_RANGE = 50 #25 100
imgPATH_A = "ImageData/trucka.bmp"
imgPATH_B = "ImageData/truckb.bmp"
ResultFile = "Result/result"+str(BLOCK)

imgA = cv2.imread(imgPATH_A).astype(int)
imgB = cv2.imread(imgPATH_B).astype(int)

ANCHOR_ROW = [ i*BLOCK for i in range(386//BLOCK) ] + [386-BLOCK]
ANCHOR_COL = [ i*BLOCK for i in range(386//BLOCK) ] + [386-BLOCK]
answer = np.zeros((386//BLOCK+1,386//BLOCK+1,2))




def calblock(row1, column1, row2, cloumn2):
	n = 0
	for i in range(BLOCK):
		for j in range(BLOCK):
			n += abs( imgA.item(row1+i, column1+j, 0) - imgB.item(row2+i, cloumn2+j, 0) )	#abs( imgA[row1+i][column1+j][0]-imgB[row2+i][cloumn2+j][0] )
	return n




def calrange(row , column, _row, _column):
	search_range_row_left = min(SEARCH_RANGE,row)
	search_range_row_right = min(386 - row - BLOCK, SEARCH_RANGE)
	search_range_col_left = min(SEARCH_RANGE,column)
	search_range_col_right = min(386 - column - BLOCK, SEARCH_RANGE)

	temp = 0

	for i in range(-search_range_row_left, search_range_row_right):
		for j in range(-search_range_col_left, search_range_col_right):
			if i==0 and j ==0 :
				temp = calblock(row, column, row + i, column + j)
				answer.itemset((_row,_column,0), i)
				answer.itemset((_row,_column,1), j)

			else :
				if temp>calblock(row, column, row + i, column + j) :
					temp = calblock(row, column, row + i, column + j)
					answer.itemset((_row,_column,0), i)
					answer.itemset((_row,_column,1), j)





if __name__ == '__main__':

	for idxi, i in enumerate(ANCHOR_ROW):
		for idxj, j in enumerate(ANCHOR_COL):
			calrange(i, j, idxi, idxj)
			print "ROW:", i , "  COL:", j,"	", answer[idxi][idxj]
		

	np.savetxt(ResultFile, answer,fmt="%s")




#######################################################
#													  #
#		         		PLOT						  #
#                                                     #
#######################################################
	X, Y = np.meshgrid(np.arange(0, 386, 1), np.arange(0, 386, 1))
	U = np.squeeze(np.delete(answer,1,2))
	V = np.squeeze(np.delete(answer,0,2))


	plt.figure()
	Q = plt.quiver(X[::BLOCK, ::BLOCK], Y[::BLOCK, ::BLOCK], U, -V,
               color='b', units='x',
               linewidths=(2,), edgecolors=('k'), headaxislength=5)
	qk = plt.quiverkey(Q, 0.5, 0.03, 1, r'$1 \frac{m}{s}$',
                   fontproperties={'weight': 'bold'})
	plt.axis([-25, 400, 400, -25])
	plt.title("Motion Vector (block size: "+str(BLOCK)+")")
	plt.show()



	print "########## Total time: ", time.time()-start, " sec ##########"