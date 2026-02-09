import csv
import datetime

class CSVWriter():
    def __init__(self, filename: str):
        self.filename = filename

    def writeData(self, timestamp: str, response: str, kind: bool, school: str) -> None:
        """ Adds the response to the dataset

        Parameters:
        (str)timestamp: The time that the response was sent to the Google for within 5 seconds of accuracy
        (str)response: The response from the form
        (bool)kind: Determinate if the message was kind or not
        (str)school: The name of the school

        """
        with open(self.filename, "a", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, dialect="excel")
            writer.writerow([timestamp, school, response, int(kind)])
        
    

if __name__ == "__main__":
    CSVWriter("data.csv").writeData("!!!!!", "22😀", True, "TestSchool")