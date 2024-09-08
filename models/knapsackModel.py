class KnapSack:
     def __init__(self, ItemsQuantity:int, IndividualsQuantity:int, ItemsBeneficits, ItemsWeights, MaxCapacity:int, crossingRate: float, mutationRate:float, evaluativeMethod:str):
         self.ItemsQuantity = ItemsQuantity
         self.IndividualsQuantity = IndividualsQuantity 
         self.ItemsBeneficits = ItemsBeneficits
         self.ItemsWeights =  ItemsWeights
         self.MaxCapacity = MaxCapacity
         self.crossingRate = crossingRate
         self.mutationRate = mutationRate 
         self.evaluativeMethod = evaluativeMethod
    
    
    
        