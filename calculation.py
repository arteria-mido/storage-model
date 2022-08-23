"""
storage-model is a minimal module which calculates actual boiler capacity and energy in boiler
based on theoretical capacity and warm water demand.
the module takes an excel (file format: .xlsx) file as input data and outputs a json file.

this module uses standard python lists
TODO 1: to be converted to numpy arrays
TODO 2: classes to be sorted into own separate modules and imported here
"""
import pandas as pd
# import numpy as np
import json
# from data.standard_boiler import StandardBoilerModel

# EXCELDATA = 'D:/Arteria/Storage-model/data/storage_model.xlsx'
# OUTPUTDIR = 'D:/Arteria/Storage-model/data/'

EXCELDATA = './data/storage_model.xlsx'
OUTPUTDIR = './data/'

class StandardHeatingProfile:
    """
    stores information on energy demand for heating and hot water (household and commercial)
    (german: Standardlastprofile Wärme (Heizung & Warmwasser))
    loads data from input excel file (profile to be found in sheet 'Zeitreihen')
    """
    q = 1000.0
    adapted_bww = []

    @classmethod
    def loadAdaptedDataProfile(cls) -> None:
        """
        loads column 'BWW HH [kW] adaptiert' in excel sheet 'Zeitreihen'
        and stores in class list adapted_bww
        """
        zeitreihen = pd.read_excel(EXCELDATA, sheet_name='Zeitreihen', header=5, usecols=['BWW HH [kW] adaptiert'])
        cls.adapted_bww = zeitreihen.values.flatten().tolist()
        # print(len(zeitreihen.values.flatten().tolist()))

class HotWaterPump:
    """
    stores energy demand (electricity) for hot water provided by hot water pump (Wärmepumpe)
    unit: kWh
    """
    dmd_e = 28096

class HotWaterDemand(StandardHeatingProfile, HotWaterPump):
    """
    calculates hot water demand (on an hourly basis) in kW
    values are stored in class variable hwd
    """
    hwd = []

    @classmethod
    def calcHotWaterDemand(cls) -> None:
        """
        takes values stored in adapted_bww list (StandardHeatingProfile) and electric demand (HotWaterPump)
        and calculates energy demand for hot water supply
        """
        if len(cls.adapted_bww): # if data have been loaded
            cls.hwd = list(map(lambda n : cls.dmd_e / cls.q * n, cls.adapted_bww))
            # print(cls.hwd[0:5])

class StandardBoiler:
    """
    calculates and returns theoretical capacity, actual capacity and energy in boiler
    on an hourly basis when hot water demand is provided 
    """
    #unit in kW
    totalChargeCapacity = 90.00
    maxCapacity = 120

    theoretical_cap = []
    actual_cap, stored_energy = ([0.00], [0.00])

    @classmethod
    def setTheoreticalCap(cls, hour:float) -> float:
        t_cap = cls.totalChargeCapacity if hour <= 6.0 else 0
        return t_cap
    
    @classmethod
    def loadTheoreticalCap(cls) -> None:
        """
        fills theoretical_cap list with data for a full year
        QUESTION: should it be hardcoded to a year? 
        - or should the number of days be passed as argument?
        - or should this list correspond to column 'Zeitstempel' 
        (which means 'Zeitstempel' should be loaded and processed too)?
        """
        cls.theoretical_cap = [cls.setTheoreticalCap(h) for day in range(365) for h in range(1, 25)]

    @classmethod
    def calcActualCap(cls, index: int) -> float:
        remaining_e = cls.stored_energy[index-1] - HotWaterDemand.hwd[index]
        if (remaining_e + cls.theoretical_cap[index] >= cls.maxCapacity): actualCap = cls.maxCapacity - remaining_e
        else: actualCap = cls.theoretical_cap[index]
        return actualCap

    @classmethod
    def calcResidualEnergy(cls, index: int) -> float:
        residual_e = cls.stored_energy[index-1] - HotWaterDemand.hwd[index] + cls.actual_cap[index]
        return residual_e

    @classmethod
    def loadOutputData(cls) -> None:
        StandardHeatingProfile.loadAdaptedDataProfile()
        HotWaterDemand.calcHotWaterDemand()
        cls.loadTheoreticalCap()
        for i in range(1, len(cls.theoretical_cap)):
            cls.actual_cap.append(cls.calcActualCap(i))
            cls.stored_energy.append(cls.calcResidualEnergy(i))
        # print('printed from class {}'.format(cls.__name__))
        # print(cls.stored_energy[0:5])
        # print(cls.actual_cap[8736:8744])

    @classmethod
    def prepareJsonOutput(cls) -> dict:
        """
        packs output data into a json file format
        'timestamps' is deliberately left empty for now (because values for 'Zeitstempel' are all the same)
        but will be filled with actual timestamps to aid visualisation
        """
        outputJson = {}
        outputJson['timestamps'] = []
        outputJson['actual load cap'] = cls.actual_cap
        outputJson['residual energy'] = cls.stored_energy
        return outputJson
    
    @classmethod
    def writeOutputToFile(cls) -> None:
        json_object = json.dumps(cls.prepareJsonOutput())
        filename = OUTPUTDIR + 'standard_boiler.json'
        try:
            with open(filename, 'w') as outputfile:
                outputfile.write(json_object)
        except BaseException as e:
            print('BaseException: ', filename)
            print(e)
        else:
            print('data have been successfully written.')


StandardBoiler.loadOutputData()
StandardBoiler.writeOutputToFile()
# test_obj = StandardBoilerModel()