class KnapSack:
     def __init__(self, IndividualsQuantity:int, ItemsQuantity:int, ItemsBeneficits, ItemsWeights, MaxCapacity:int, crossingRate: float, mutationRate:float, evaluativeMethod:str):
         self.IndividualsQuantity = IndividualsQuantity
         self.ItemsQuantity = ItemsQuantity 
         self.ItemsBeneficits = ItemsBeneficits
         self.ItemsWeights =  ItemsWeights
         self.MaxCapacity = MaxCapacity
         self.crossingRate = crossingRate
         self.mutationRate = mutationRate 
         self.evaluativeMethod = evaluativeMethod
    
    
    
        