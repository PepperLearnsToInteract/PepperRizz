

class PrintAndSave:
    def __init__(self, filename):
        self.filename = filename
        self.data = list()

    def print(self, *data, end="\n"):
        print(*data, end=end)
        for element in data:
            for line in element.split("\n"):
                if '[0m' in line:
                    line = line.replace('[0m', '')
                if '[92m' in line:
                    line = line.replace('[92m', 'significant!')
                if '[91m' in line:
                    line = line.replace('[91m', 'not significant!')
                if (chr(27) in line):
                    line = line.replace(chr(27), '')
                self.data.append(line)

    def save(self):
        with open(self.filename, "w") as file:
            for data in self.data:
                file.write(data + "\n")
