import csv
import datetime

class CSVWriter():
    def __init__(self, filename: str):
        self.file = open(filename, "w", newline='')
        self.writer = csv.writer(self.file, dialect="excel")
    
    def __del__(self) -> None:
        self.file.close()

    def writeData(self, timestamp: str, response: str, kind: bool) -> None:
        """ Adds the response to the dataset
        
        Parameters:
        (str)timestamp: The time that the response was sent to the Google for within 5 seconds of accuracy
        (str)response: The response from the form
        (bool)kind: Determinate if the message was kind or not
        
        """
        self.writer.writerow([timestamp, response, int(kind)])
        
    

if __name__ == "__main__":
    CSVWriter("data.csv").writeData(1)