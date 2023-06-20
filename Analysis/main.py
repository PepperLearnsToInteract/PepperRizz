from analyzer import analyzer
from converter import converter


### !!!! USAGE !!!! ###
# only run this file, printAndSave.py, analyzer.py and converter.py are imported here, so make sure they are in the same folder
# the results will be in the results.txt file or other file you specified in the call below
# this code only requires data.json

if __name__ == "__main__":
    # Run the analyzer, use the converter to put the data in the expected format
    analyzer().run(converter().read("data.json"), "results.txt")
