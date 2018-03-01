# -*- coding: utf-8 -*-
"""
Rainflow 1D para uso em Goodman e planos A e B separadamente

@author: Bruno
"""


    
def rainflow(history):
    
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

        '''
        # cálculo de laços
        strainInput = activeList[k][mainNominal]
        if abs(strainInput) >= abs(maxMainNominal):
            mainStrain = funcNeuber(strainInput)
            mainStress = funcRamberg(mainStrain)
            maxMainNominal = mainStress
        else:
            #find max(strainJ) #pico_ou_vale & strainJNext <=> strainInput
                deltaStrain = funcNeuber(strainInput - strainJ)
                mainStrain = strainJ + deltaStrain
                mainStress = stressJ + funcRamberg(deltaStrain)            
        '''


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
    
    
if __name__ == "__main__":
    
    #saidaPlaneProjection = [main channel, auxiliary channel]
    saidaPlaneProjection = [[100.0, 200.0, 100.0, 100.0, 100.0, 100.0], [250.0, -150.0, 250.0, 0.0, 10.0, 25.0]]

    print (rainflow(saidaPlaneProjection))