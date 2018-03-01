# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 2017

@author: Bruno
"""

import math

from Modelos import fatigueModels
from Newton_Raphson import newtonRaphson
from Plane_Projection import planeProject
from Rainflow import rainflow

if __name__ == "__main__":
    stressX = [629, 629]
    stressY = [0, 0]
    shear = [629, -629]
    pressure = [0, 0]

    entrada = [stressX, stressY, shear, pressure]

    # Parametros
    modelToExecute = 'SWT'
    planeToExecute = 'B'
    degreeStep = 10

    totalDamage=[]
    for degree in range(0, 180, degreeStep):

        projectedEntryData = planeProject(entrada , degree, planeToExecute)

        countedCycles = rainflow(projectedEntryData)

        projectDamage = fatigueModels(countedCycles, modelToExecute)

        totalDamage.append([projectDamage, degree])

    print (totalDamage)

    highestDamage = max(totalDamage)
    totalDamage.remove(max(totalDamage))
    secondHighestDamage = max(totalDamage)
    
    print (highestDamage, secondHighestDamage)
