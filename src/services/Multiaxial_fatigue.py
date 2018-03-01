# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 2017

@author: Bruno
"""



import math


s = []

''' Math function
'''
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
    

def rainflow1D(history):
    
    activeList=[]

    #mainNominal = []
    #maxMainNominal = 0

    # mainStack será tensão para LE e deformação para EP
    mainStack = 0

    minStack = 1
    maxStack = 2


    halfCycleRange=[]
    halfCyclePeak=[]
    halfCycleValley=[]

    column1 = history[0]
    column2 = history[1]
    
    column1Size = len(column1)

    for i in range(column1Size):
        
        # adiciona novo PICO ou VALE ao final da lista ativa activeList
        newPoint = [column1[i] , column2[i] , column2[i]]
        activeList.append(newPoint)                        
        # atualiza lista ativa: k -> k+=1
        k = len(activeList) - 1

        if k >= 2:
            
            if ((activeList[k-1][mainStack] < activeList[k-2][mainStack]) and (activeList[k-2][mainStack] <= activeList[k][mainStack])) \
                    or ((activeList[k-1][mainStack] > activeList[k-2][mainStack]) and (activeList[k-2][mainStack] >= activeList[k][mainStack])):
                
                # faz-se as contas TODAS
                mainRange = abs(activeList[k-2][mainStack] - activeList[k-1][mainStack])
                auxiliaryPeak = max(activeList[k-2][maxStack] , activeList[k-1][maxStack])
                auxiliaryValley = min(activeList[k-2][minStack] , activeList[k-1][minStack])

                #conta 1/2
                halfCycleRange.append(mainRange)
                halfCyclePeak.append(auxiliaryPeak)
                halfCycleValley.append(auxiliaryValley)

                if k > 2:

                    # critério (b) - conta + 1/2 ciclo de Sk-2 a Sk-1
                    halfCycleRange.append(mainRange)
                    halfCyclePeak.append(auxiliaryPeak)
                    halfCycleValley.append(auxiliaryValley)

                    # retain max/min among last entries
                    activeList[k-3][minStack] = min([activeList[k-3][minStack] , activeList[k-2][minStack] , activeList[k-1][minStack]])
                    activeList[k-3][maxStack] = max([activeList[k-3][maxStack] , activeList[k-2][maxStack] , activeList[k-1][maxStack]])

                    # remove ciclo contado - k-=2
                    del activeList[k-2:k]                                                                     #Como deletar melhor????
                    
                    
                else:

                    # critério (a) - conta 1/2 ciclo de Sk-2 a Sk-1

                    # retain max/min among last entries
                    activeList[k-3][minStack] = min([activeList[k-3][minStack] , activeList[k-2][minStack]])
                    activeList[k-3][maxStack] = max([activeList[k-3][maxStack] , activeList[k-2][maxStack]])

                    # remove 1/2 ciclo contado (k-=1)
                    del activeList[k-2]
                    

            # filtra valores que não são picos ou vales
            elif ((activeList[k-1][mainStack] >= activeList[k-2][mainStack]) and (activeList[k][mainStack] <= activeList[k-1][mainStack])) \
                    or ((activeList[k-1][mainStack] <= activeList[k-2][mainStack]) and (activeList[k][mainStack] >= activeList[k-1][mainStack])):
                del activeList[k-1]

    
    # critério (c) - conta 1/2 ciclo de pares restantes
    k = len(activeList) - 1
    while k >= 1:
        # faz-se as contas TODAS
        mainRange = abs(activeList[k-2][mainStack] - activeList[k-1][mainStack])                              #cuidado com abs() - fazer func própria
        auxiliaryPeak = max(activeList[k-2][maxStack] , activeList[k-1][maxStack])
        auxiliaryValley = min(activeList[k-2][minStack] , activeList[k-1][minStack])
                        
        # conta 1/2 ciclo de S[k-2] a S[k-1]
        halfCycleRange.append(mainRange)
        halfCyclePeak.append(auxiliaryPeak)
        halfCycleValley.append(auxiliaryValley)

        # remove 1/2 ciclo contado e atualiza k (k-=1)
        del activeList[k-2]
        k = len(activeList) - 1
                
    countedCycles = [halfCycleRange, halfCyclePeak, halfCycleValley]
    return countedCycles
    
    
def newtonRaphson(inputValue):
     
    beta = inputValue[0]
    B = inputValue[1]
    gama = inputValue[2]
    C = inputValue[3]
    delta = inputValue[4]
    errorAdmissible = inputValue[5]   
    
    icognita = min( math.log(delta / beta) / B , math.log(delta / gama) / C )

    errorGoal = 1

    i=1
    while errorGoal > 0:
        expB = beta * math.exp( B * icognita )
        expC = gama * math.exp( C * icognita )

        icognita -= ( expB + expC ) / ( B * expB + C * expC ) * math.log( ( expB + expC ) / delta )

        errorGoal = ( expB *  ( 1 + errorAdmissible ) ** B + expC *  ( 1 + errorAdmissible)  ** C  - delta ) / ( expB + expC - delta ) 

        i += 1
        if i > 999:
            print ('NAO CONVERGE')
            break

    return icognita


def fatigueModels(countedCycles, modelToExecute):

    B = 3.0
    C = 20.0 * 10**11

    mainRange = countedCycles[0]
    auxiliaryPeak = countedCycles[1]
    auxiliaryValley = countedCycles[2]

    lenCount = len(mainRange)
    cummulatedDamage = 0

    # Modelo de Goodman
    if modelToExecute == 'Goodman':
        ultimateTensileStrength = 440

        sigmaNormalRange = []
        for i in range(lenCount):
            sigmaNormalRange.append(auxiliaryPeak[i] - auxiliaryValley[i])        
        sigmaNormalMax = auxiliaryPeak
        

        for i in range(lenCount):       
            damageParameter = (sigmaNormalRange[i] /2) / ( 1 - ((sigmaNormalMax[i] - (sigmaNormalRange[i] /2)) / ultimateTensileStrength ))
            eventDamage = (damageParameter ** B) /C /2.

            cummulatedDamage += eventDamage

    # Modelo de Findley
    elif modelToExecute == 'Findley':
        alfaFindley = 0.5
        shearA = mainRange
        sigmaNormalMax = auxiliaryPeak
        constantes = 0.58 * 0.577
        bMinor = -0.12

        for i in range(lenCount):       
            damageParameter = shearA[i] / 2. + alfaFindley * sigmaNormalMax[i]
            eventDamage = ( constantes / damageParameter ) ** ( 1/ bMinor)

            cummulatedDamage += eventDamage

    # Modelo de SWT
    elif modelToExecute == 'SWT':
        beta = 4.414 * 10 ** -3
        B = -0.12
        gama = 0.41
        C = -0.51
        delta = 0.002
        errorAdmissible = 0.001 
        
        inputValue = [beta, B, gama, C, delta, errorAdmissible]

        for i in range(lenCount):       
            damageParameter = newtonRaphson(inputValue)
            eventDamage = 1 / ( math.exp(damageParameter))

            cummulatedDamage += eventDamage

    return cummulatedDamage
    
    
    
if __name__ == "__main__":
    
    stressX = [629, 629]
    stressY = [0, 0]
    shear = [629, -629]
    pressure = [0, 0]

    entrada = [stressX, stressY, shear, pressure]

    modelToExecute = 'SWT'

    totalDamage=[]
    for i in range(18):
        
        degree = i * 10              
                
        projectDamage = fatigueModels(rainflow1D(planeProject(entrada , degree, 'B')), modelToExecute)

        totalDamage.append([projectDamage, degree])

    print (totalDamage)

    highestDamage = max(totalDamage)
    totalDamage.remove(max(totalDamage))
    secondHighestDamage = max(totalDamage)
    
    print (highestDamage, secondHighestDamage)







# #totalDamage=[]
    # highestDamage = [-1, 0]
    # secondHighestDamage = [-1, 0]
    # for i in range(17):
        
    #     degree = i * 10              
                
    #     projectDamage = fatigueModels(rainflow1D(planeProject(entrada , degree, 'A')))

    #     #totalDamage.append([projectDamage, degree])
    #     highestDamage = max(highestDamage, [projectDamage, degree])
    #     secondHighestDamage = max(secondHighestDamage, [projectDamage, degree]) if secondHighestDamage < highestDamage else secondHighestDamage

    # #print totalDamage

    # #highestDamage = max(totalDamage)
    # #totalDamage.remove(highestDamage)
    # #secondHighestDamage = highestDamage
    
    