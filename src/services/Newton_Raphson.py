# -*- coding: utf-8 -*-
"""
Acha minimo de funcao biparabolica usando metodo newton raphson

@author: Bruno
"""
import math

def newtonRaphson(inputValue):
     
    beta = inputValue[0]
    B = inputValue[1]
    gama = inputValue[2]
    C = inputValue[3]
    delta = inputValue[4]
    errorAdmissible = inputValue[5]   
    
    icognita = min( math.log(delta / beta) / B , math.log(delta / gama) / C )

    # expB = beta * math.exp( B * icognita )
    # expC = gama * math.exp( C * icognita )
    # errorGoal = ( expB *  ( 1 + errorAdmissible ) ** B + expC *  ( 1 + errorAdmissible)  ** C  - delta ) / ( expB + expC - delta ) 
    errorGoal = 1

    i=1
    while errorGoal > 0:
        print (icognita)
        expB = beta * math.exp( B * icognita )
        expC = gama * math.exp( C * icognita )

        icognita -= ( expB + expC ) / ( B * expB + C * expC ) * math.log( ( expB + expC ) / delta )

        errorGoal = ( expB *  ( 1 + errorAdmissible ) ** B + expC *  ( 1 + errorAdmissible)  ** C  - delta ) / ( expB + expC - delta ) 

        i += 1
        if i > 6:
            print (i)
            break

    return icognita


if __name__ == "__main__":
    
    beta = 4.414 * 10 ** -3
    B = -0.12
    gama = 0.41
    C = -0.51
    delta = 0.002
    errorAdmissible = 0.001 
    
    inputValue = [beta, B, gama, C, delta, errorAdmissible]
    
    print (newtonRaphson(inputValue))