import requests
import pandas as pd
import os
import datetime
from calendar import monthrange

class WeatherDataFetcher:
    def __init__(self, startDate, endDate):
        self.token = "R52RPE7UPW7CUWQFQ5NLKDBH6"
        self.location = "Arlington,TX"
        self.startDate = startDate
        self.endDate = endDate
        self.data = None
    
    def getWeatherDataDaily(self):
        endpoints = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{self.location}/{self.startDate}/{self.endDate}?key={self.token}"
        
        try:
            response = requests.get(endpoints)
            
            if response.status_code == 200:
                self.data = response.json()
                return self.data  # Return the data for use in another class
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                print("Response content:", response.text)
                return None
                
        except requests.RequestException as error:
            print(f"The following error has occurred: {error}")
            return None
    
class cleanData:
    def __init__(self, data):
        self.data = data
        self.cleanedData = None
    
    def cleanData(self):
        if self.data is None:
            print("No data to clean.")
            return None
        
        # Extract hour data from the JSON structure
        hourData = self.data['days'][0]['hours']
        
        solarIrradiance = []
        solarEnergy = []
        uvIndex = []
        cloudCover = []
        dateTime = []
        
        for hour in hourData:
            # Extracting the relevant values
            solarIrradiance.append(float(hour['solarradiation']))
            solarEnergy.append(float(hour['solarenergy']))
            uvIndex.append(float(hour['uvindex']))
            cloudCover.append(float(hour['cloudcover']))
            dateTime.append(hour['datetime'])
        
        # Create a DataFrame for the cleaned data
        self.cleanedData = pd.DataFrame({
            'datetime': dateTime,
            'solarIrradiance': solarIrradiance,
            'solarEnergy': solarEnergy,
            'uvIndex': uvIndex,
            'cloudCover': cloudCover
        })
        
        return self.cleanedData  # Return cleaned data

class fileHandle:
    def __init__(self, subFolderName):
        self.mainFolderName = "Weather\Daily"
        self.subFolderName = subFolderName  # Example subfolder name, change as needed
    
    def makeFolder(self):
        os.makedirs(os.path.join(self.mainFolderName, self.subFolderName), exist_ok=True)
    
    def saveDataToCSV(self, data, fileName):
        filePath = os.path.join(self.mainFolderName, self.subFolderName, fileName)
        data.to_csv(filePath, index=False)  # Save the DataFrame to a CSV file
        print(f"Data saved to {filePath}")

def main():
    month = input("Enter Month: ").zfill(2)
    formatedMonth = month
    currentYear = "2024"
        
    print(currentYear)
    
    for day in [f"{day:02}" for day in range(1, monthrange(int(currentYear), int(month))[1] + 1)]:
        fileName = f"{currentYear}-{formatedMonth}-{day}"

        weatherFetcher = WeatherDataFetcher(fileName, fileName)
        weatherData = weatherFetcher.getWeatherDataDaily()

        if weatherData:
            cleanedData = cleanData(weatherData).cleanData()
            fileHandler = fileHandle(f"{formatedMonth}-{currentYear}")
            fileHandler.makeFolder()
            fileHandler.saveDataToCSV(cleanedData, f"{fileName}.csv")
    
if __name__ == "__main__":
    main()
