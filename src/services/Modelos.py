# -*- coding: utf-8 -*-
"""
Lista de todos os modelos para cálculo

@author: Bruno
"""

import math
from Newton_Raphson import newtonRaphson

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

    beta = 4.414 * 10 ** -3
    B = -0.12
    gama = 0.41
    C = -0.51
    delta = 0.002
    errorAdmissible = 0.001 
    
    inputValue = [beta, B, gama, C, delta, errorAdmissible]
    print (newtonRaphson(inputValue))

    saidaRainflow = [[218.44940750499848], [988.5564285209284], [-250.33172476842924]]
    modelToExecute = 'SWT'
  
    print (fatigueModels(saidaRainflow, modelToExecute))