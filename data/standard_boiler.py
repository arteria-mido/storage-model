
class StandardBoilerModel:
    #unit in kW
    totalChargeCapacity = 90.00
    maxCapacity = 120

    theoretical_cap = []
    actual_cap, stored_energy = ([0.00], [0.00])

    def __init__(self):
        print('instance created')

    @classmethod
    def setAssumedCap(cls, hour:float) -> float:
        assumedCap = cls.totalChargeCapacity if hour <= 6.0 else 0
        return assumedCap
    
    @classmethod
    def calcTheoreticalCap(cls) -> None:
        cls.theoretical_cap = [cls.setAssumedCap(h) for i in range(365) for h in range(1, 25)]
        # print(len(cls.theoretical_cap))

    @classmethod
    def calcActualCap(cls, index: int) -> float:
        pass

    @classmethod
    def calcResidualEnergy(cls) -> float:
        pass

# StandardBoilerModel.calcTheoreticalCap()
    
