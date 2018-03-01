# -*- coding: utf-8 -*-
"""
Projeção de planos A e B

@author: Bruno
"""

import math

def planeProject(data, tetaDegree, planeToExecute):
    
    stressX = data[0]
    stressY = data[1]
    shear = data[2]
    pressure = data[3]

    lenData = len(stressX)
    teta = (tetaDegree * math.pi) / 180.
    history = None

    # Case A plane - stress based
    if planeToExecute == 'A':
        mainA=[]
        auxiliarA=[]

        cos2Teta = math.cos(2 * teta)
        cosTetaSqr = math.cos(teta) ** 2
        sen2Teta = math.sin(2 * teta)
        senTetaSqr = math.sin(teta) ** 2

        for i in range(lenData):
            
            mainAPoint = shear[i] * cos2Teta + ( (stressY[i] - stressX[i]) * sen2Teta ) / 2
            mainA.append(mainAPoint) 

            auxiliarAPoint = shear[i] * sen2Teta + stressX[i] * cosTetaSqr + stressY[i] * senTetaSqr
            auxiliarA.append(auxiliarAPoint)

        history = [mainA , auxiliarA]

    # Case B plane - stress based
    elif planeToExecute == 'B':
        
        mainB=[]
        auxiliarB=[]

        cos2Teta = math.cos(2 * teta)
        cosTetaSqr = math.cos(teta) ** 2
        sen2Teta = math.sin(2 * teta)
        senTetaSqr = math.sin(teta) ** 2

        for i in range(lenData):
            
            mainBPoint = (stressX[i] * cosTetaSqr + stressY[i] * senTetaSqr + shear[i] * sen2Teta) / 2.
            mainB.append(mainBPoint) 
            auxiliarB.append(mainBPoint)   

        history = [mainB , auxiliarB]

    else:
        print('PLANO {} ! ERA PARA SER A ou B'.format(planeToExecute))
        import sys
        sys.exit(-1)
    
    
    return history



if __name__ == "__main__":
    
    stressX = [250, -150, 250]
    stressY = [0, 0, 0]
    shear = [100, 100, 100]
    pressure = [0, 0, 0]

    entrada = [stressX, stressY, shear, pressure]
    planeToExecute = 'A'
    
    print (planeProject(entrada, 0, planeToExecute))