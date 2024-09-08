import numpy as np

class ParametersInformation:
    data = {
        "1": {
            "N":                    400,        #individualsQuantity
            "n":                    200,        #genotypeLength
            "evaluativeMethod":     "r",        #Reparation
            "alpha":                1/2,        #α
            "w_range":              np.arange(1,21),     
            "b_range":              np.arange(10, 101),
            "crossingRate":         0.8,
             "mutationRate":        0.02
        },
        "2": {
            "N":                    400,        #individualsQuantity
            "n":                    200,        #genotypeLength
            "evaluativeMethod":     "p",        #Punishment
            "alpha":                1/2,        #α
            "w_range":              np.arange(1,21),     
            "b_range":              np.arange(10, 101),
            "crossingRate":         0.8,
            "mutationRate":         0.02
        },
        "3": {
            "N":                    1000,       #individualsQuantity
            "n":                    500,        #genotypeLength
            "evaluativeMethod":     "r",        #Reparation
            "alpha":                1/2,        #α
            "w_range":              np.arange(1,21),     
            "b_range":              np.arange(10, 101),
            "crossingRate":         0.8,
            "mutationRate":         0.02
        },
        "4": {
            "N":                    1000,       #individualsQuantity
            "n":                    500,        #genotypeLength
            "evaluativeMethod":     "p",        #Punishment
            "alpha":                1/2,        #α
            "w_range":              np.arange(1,21),     
            "b_range":              np.arange(10, 101),
            "crossingRate":         0.8,
            "mutationRate":         0.02
        },
        "5": {
            "N":                    1500,       #individualsQuantity
            "n":                    750,        #genotypeLength
            "evaluativeMethod":     "p",        #Punishment
            "alpha":                1/2,        #α
            "w_range":              np.arange(1,21),     
            "b_range":              np.arange(10, 101),
            "crossingRate":         0.8,
            "mutationRate":         0.02
        },
        "6": {
            "N":                    2000,       #individualsQuantity
            "n":                    1000,       #genotypeLength
            "evaluativeMethod":     "p",        #Punishment
            "alpha":                1/2,        #α
            "w_range":              np.arange(1,21),     
            "b_range":              np.arange(10, 101),
            "crossingRate":         0.8,
            "mutationRate":         0.02
        }
    }



