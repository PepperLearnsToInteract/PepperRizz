import json


class converter:
    def __init__(self):
        pass
    # Read the file

    def read(self, dataFile, outFile="convertedData.json"):
        with open(dataFile) as file:
            data = json.load(file)

        # Print the data
        converData = {'gaze': list(), 'verbal': list(), 'gaze-verbal': list()}
        for element in data:
            convertedElement = dict()
            for key, element in element.items():
                try:
                    convertedElement[key] = int(element)
                except ValueError:
                    convertedElement[key] = element
            if convertedElement["Is de persoon naar de robot toe gelopen?"].lower() == "ja":
                convertedElement["Is de persoon naar de robot toe gelopen?"] = True
            else:
                convertedElement["Is de persoon naar de robot toe gelopen?"] = False

            # 0 is gaze, 1 is verbal, 2 is gaze-verbal
            usedStrategy = ""
            if convertedElement["Welke strategie gebruik je"].lower() == "gaze":
                convertedElement["Welke strategie gebruik je"] = 0
                usedStrategy = "gaze"
            elif convertedElement["Welke strategie gebruik je"].lower() == "verbal":
                convertedElement["Welke strategie gebruik je"] = 1
                usedStrategy = "verbal"
            elif convertedElement["Welke strategie gebruik je"].lower() == "gaze-verbal":
                convertedElement["Welke strategie gebruik je"] = 2
                usedStrategy = "gaze-verbal"
            if convertedElement["Aantal personen"] == '' or convertedElement["Aantal personen"] == ' ' or convertedElement["Aantal personen"] == '-':
                convertedElement["Aantal personen"] = 1
            converData[usedStrategy].append(
                convertedElement)
        # Add the total amount of people that passed the robot
        converData['gaze'].append({"personsPassed": 1158})
        converData['verbal'].append({"personsPassed": 959})
        converData['gaze-verbal'].append({"personsPassed": 1185})
        json.dump([converData], open(outFile, "w"), indent=4)
        # return the file name of the converted file
        return outFile


# only run when this file is being run on its own
if __name__ == "__main__":
    converter().read("data.json")
