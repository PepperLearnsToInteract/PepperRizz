import json
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, ttest_ind
from printAndSave import PrintAndSave
from statsmodels.stats.proportion import proportions_ztest
import numpy as np


class analyzer:
    def __init__(self):
        pass

    def load(self, dataFile):
        self.dataFile = dataFile
        with open(dataFile) as file:
            self.data = json.load(file)[0]

    def analyze(self):
        PersonsInteractedGaze = 0
        PersonsInteractedVerbal = 0
        PersonsInteractedGazeVerbal = 0
        PersonsStoppedGaze = 0
        PersonsStoppedVerbal = 0
        PersonsStoppedGazeVerbal = 0

        # Print the data
        for element in self.data['gaze']:  # process the data for gaze

            # check if the current element contains the passerby information, if it does jump to else and extract it
            if "personsPassed" not in element.keys():
                PersonsStoppedGaze += int(element["Aantal personen"])
                if element["Is de persoon naar de robot toe gelopen?"] == True:
                    PersonsInteractedGaze += int(element["Aantal personen"])
            else:
                self.personsPassedGaze = int(element["personsPassed"])

        for element in self.data['verbal']:  # process the data for verbal
            # check if the current element contains the passerby information, if it does jump to else and extract it
            if "personsPassed" not in element.keys():
                PersonsStoppedVerbal += int(element["Aantal personen"])
                if element["Is de persoon naar de robot toe gelopen?"] == True:
                    PersonsInteractedVerbal += int(element["Aantal personen"])
            else:
                self.personsPassedVerbal = int(element["personsPassed"])

        # process the data for gaze-verbal
        for element in self.data['gaze-verbal']:
            # check if the current element contains the passerby information, if it does jump to else and extract it
            if "personsPassed" not in element.keys():
                PersonsStoppedGazeVerbal += int(element["Aantal personen"])
                if element["Is de persoon naar de robot toe gelopen?"] == True:
                    PersonsInteractedGazeVerbal += int(
                        element["Aantal personen"])
            else:
                self.personsPassedGazeVerbal = int(element["personsPassed"])

        self.print_and_save.print("Gaze: " + str(PersonsInteractedGaze) +
                                  " stopped: " + str(PersonsStoppedGaze))
        self.print_and_save.print("Verbal: " + str(PersonsInteractedVerbal) +
                                  " stopped: " + str(PersonsStoppedVerbal))
        self.print_and_save.print("Gaze-Verbal: " + str(PersonsInteractedGazeVerbal) +
                                  " stopped: " + str(PersonsStoppedGazeVerbal))

        # calculate the stop rate for each interaction type
        stopRateGaze = PersonsStoppedGaze/self.personsPassedGaze
        stopRateVerbal = PersonsStoppedVerbal/self.personsPassedVerbal
        stopRateGazeVerbal = PersonsStoppedGazeVerbal/self.personsPassedGazeVerbal

        # calculate the interaction success rate for each interaction type
        interactionSuccesRateGaze = PersonsInteractedGaze/PersonsStoppedGaze
        interactionSuccesRateVerbal = PersonsInteractedVerbal/PersonsStoppedVerbal
        interactionSuccesRateGazeVerbal = PersonsInteractedGazeVerbal/PersonsStoppedGazeVerbal

        # calculate the whole interaction success rate for each interaction type
        wholeInteractionSuccesRateGaze = PersonsInteractedGaze/self.personsPassedGaze
        wholeInteractionSuccesRateVerbal = PersonsInteractedVerbal/self.personsPassedVerbal
        wholeInteractionSuccesRateGazeVerbal = PersonsInteractedGazeVerbal / \
            self.personsPassedGazeVerbal

        self.print_and_save.print("Gaze: " + str(PersonsInteractedGaze) + " stopped: " +
                                  str(PersonsStoppedGaze) + " whole interaction success rate: " +
                                  str(wholeInteractionSuccesRateGaze), " \ninteraction success rate: " +
                                  str(interactionSuccesRateGaze), " stop rate: " + str(stopRateGaze) + "\n\n")
        self.print_and_save.print("Verbal: " + str(PersonsInteractedVerbal) + " stopped: " +
                                  str(PersonsStoppedVerbal) + " whole interaction success rate: " +
                                  str(wholeInteractionSuccesRateVerbal), " \ninteraction success rate: " +
                                  str(interactionSuccesRateVerbal), " stop rate: " + str(stopRateVerbal) + "\n\n")
        self.print_and_save.print("Gaze-Verbal: " + str(PersonsInteractedGazeVerbal) + " stopped: " +
                                  str(PersonsStoppedGazeVerbal) + " whole interaction success rate: " +
                                  str(wholeInteractionSuccesRateGazeVerbal), " \ninteraction success rate: " +
                                  str(interactionSuccesRateGazeVerbal), " stop rate: " + str(stopRateGazeVerbal) + "\n\n")
        ax, fig = plt.subplots(figsize=(12, 8), ncols=3)
        fig[0].set_title('interaction success rate')
        fig[0].set_xlabel('Interaction Type')
        fig[0].set_ylabel('Interaction Success Rate')
        fig[0].bar(['Gaze', 'Verbal', 'Gaze-Verbal'], [interactionSuccesRateGaze,
                                                       interactionSuccesRateVerbal, interactionSuccesRateGazeVerbal])
        fig[1].set_title('stop rate')
        fig[1].set_xlabel('Interaction Type')
        fig[1].set_ylabel('Stop Rate')
        fig[1].bar(['Gaze', 'Verbal', 'Gaze-Verbal'], [stopRateGaze,
                                                       stopRateVerbal, stopRateGazeVerbal])
        fig[2].set_title('whole interaction success rate')
        fig[2].set_xlabel('Interaction Type')
        fig[2].set_ylabel('Whole Interaction Success Rate')
        fig[2].bar(['Gaze', 'Verbal', 'Gaze-Verbal'], [wholeInteractionSuccesRateGaze,
                                                       wholeInteractionSuccesRateVerbal, wholeInteractionSuccesRateGazeVerbal])
        plt.show()

    def calculate_anova(self):

        self. gaze_interacted = []
        self.verbal_interacted = []
        self.gaze_verbal_interacted = []

        with open(self.dataFile, 'r') as file:
            data = json.load(file)
        tests = dict()
        for element in data[0]['gaze']:
            if "personsPassed" not in element.keys():
                self.gaze_interacted.append(
                    element["Is de persoon naar de robot toe gelopen?"])

        for element in data[0]['verbal']:
            if "personsPassed" not in element.keys():
                self.verbal_interacted.append(
                    element["Is de persoon naar de robot toe gelopen?"])

        for element in data[0]['gaze-verbal']:
            if "personsPassed" not in element.keys():
                self.gaze_verbal_interacted.append(
                    element["Is de persoon naar de robot toe gelopen?"])

        tests['interacted'] = f_oneway(
            self.gaze_interacted, self.verbal_interacted, self.gaze_verbal_interacted)

        return tests

    def calculate_ttest(self):

        results = dict()
        ttestResults = dict()
        ttestResults['gaze vs verbal'] = ttest_ind(
            self.gaze_interacted, self.verbal_interacted)
        ttestResults['gaze vs gaze-verbal'] = ttest_ind(
            self.gaze_interacted, self.gaze_verbal_interacted)
        ttestResults['verbal vs gaze-verbal'] = ttest_ind(
            self.verbal_interacted, self.gaze_verbal_interacted)
        results['interacted'] = ttestResults

        return results

    def calculate_ztest(self):

        # Example arrays

        # Perform the z-test for each pair of groups
        stat_gv_g, p_value_gv_g = proportions_ztest([np.sum(self.gaze_verbal_interacted), np.sum(self.gaze_interacted)],
                                                    [len(self.gaze_verbal_interacted), len(self.gaze_interacted)])
        stat_gv_v, p_value_gv_v = proportions_ztest([np.sum(self.gaze_verbal_interacted), np.sum(self.verbal_interacted)],
                                                    [len(self.gaze_verbal_interacted), len(self.verbal_interacted)])
        stat_g_v, p_value_g_v = proportions_ztest([np.sum(self.gaze_interacted), np.sum(self.verbal_interacted)],
                                                  [len(self.gaze_interacted), len(self.verbal_interacted)])

        return {"gaze-verbal vs. gaze": (stat_gv_g, p_value_gv_g), "gaze-verbal vs. verbal": (stat_gv_v, p_value_gv_v), "gaze vs. verbal": (stat_g_v, p_value_g_v)}

    def run(self, input_file, output_file):
        # initialize the print and save class
        self.print_and_save = PrintAndSave(output_file)
        # load the data
        self.load(input_file)
        self.analyze()
        anova_result = self.calculate_anova()

        # print the ANOVA results
        self.print_and_save.print("ANOVA results: \n")
        for key, value in anova_result.items():
            f_value, p_value = value
            p_value = round(p_value, 3)
            if p_value <= 0.05:
                self.print_and_save.print('\033[92m', end="")
            else:
                self.print_and_save.print('\033[91m', end="")
            self.print_and_save.print(
                f"{key}: f-value: {f_value}, p-value: {p_value}\n")
            self.print_and_save.print('\033[0m', end="")
        # print the t-test results
        self.print_and_save.print("\n\nT-test results: \n")
        ttest_results = self.calculate_ttest()
        for key, value in ttest_results.items():
            self.print_and_save.print(f"{key}: \n")
            for key2, value2 in value.items():
                t_value, p_value = value2
                p_value = round(p_value, 3)
                if p_value <= 0.05:
                    self.print_and_save.print('\033[92m', end="")
                else:
                    self.print_and_save.print('\033[91m', end="")
                self.print_and_save.print(
                    f"{key2}: t-value: {t_value}, p-value: {p_value}\n")
                self.print_and_save.print('\033[0m', end="")
        # print the z-test results
        self.print_and_save.print("\n\nZ-test results: \n")
        ztest_results = self.calculate_ztest()
        for key, value in ztest_results.items():
            self.print_and_save.print(f"{key}: \n")
            z_value, p_value = value
            p_value = round(p_value, 3)
            if p_value <= 0.05:
                self.print_and_save.print('\033[92m', end="")
            else:
                self.print_and_save.print('\033[91m', end="")
            self.print_and_save.print(f"Z-score:{z_value} p-value:{p_value}\n")
            self.print_and_save.print('\033[0m', end="")
        # save the results to a file
        self.print_and_save.save()


# only run when this file is being run on its own
if __name__ == "__main__":

    # initialize the analyzer class
    ana = analyzer()
    ana.run("convertedData.json", 'results.txt')
