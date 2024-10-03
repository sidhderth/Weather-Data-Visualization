import os
import pandas as pd
import datetime

class fileAverage:
    def __init__(self, path):
        self.path = path
        
    def monthlyAverageMaker(self):
        fileNames = os.listdir(self.path)
        outputFilePath = f"{self.path}\\2024-06-average.csv"

        # Check if the output file exists, and only create it if it doesn't
        if not os.path.exists(outputFilePath):
            with open(outputFilePath, "w+") as outputFile:
                outputFile.write("datetime,solarIrradiance,solarEnergy,uvIndex,cloudCover\n")

            for day in fileNames:
                dataFrame = pd.read_csv(self.path + "\\" + day)
                
                solarIrradianceAverage = sum(dataFrame['solarIrradiance']) / 24
                solarEnergyAverage = sum(dataFrame["solarEnergy"]) / 24
                uvIndexAverage = sum(dataFrame['uvIndex']) / 24
                cloudCoverAverage = sum(dataFrame['cloudCover']) / 24
                
                with open(outputFilePath, "a+") as outputFile:
                    print(str(day)[0:10])
                    outputFile.write(str(day)[0:10] + "," + str(solarIrradianceAverage) + "," + str(solarEnergyAverage) + "," + str(uvIndexAverage) + "," + str(cloudCoverAverage) + "\n")
