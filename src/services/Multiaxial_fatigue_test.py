# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 2017

@author: Bruno
"""

import math
from Plane_Projection import planeProject
from Rainflow import rainflow
from Newton_Raphson import newtonRaphson  
from Modelos import fatigueModels


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
                
        projectDamage = fatigueModels(rainflow(planeProject(entrada , degree, 'B')), modelToExecute)

        totalDamage.append([projectDamage, degree])

    print (totalDamage)

    highestDamage = max(totalDamage)
    totalDamage.remove(max(totalDamage))
    secondHighestDamage = max(totalDamage)
    
    print (highestDamage, secondHighestDamage)
