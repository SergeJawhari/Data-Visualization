import pandas as pd


class PreprocessData:
    def __init__(self, filepath, graph_or_tree):
        pd.set_option('display.max_columns', 10)
        self.filepath = filepath
        self.graph_or_tree = graph_or_tree.lower()
        self.evd_data = None
        self.fxd_data = None
        self.gzd_data = None
        self.kbd_data = None

    def event_data(self):
        if self.evd_data is None:
            eventFile = self.filepath + "p1." + self.graph_or_tree + "EVD.txt"
            eventColNames = ["time", "event", "event key", "data1", "data2", "description"]
            eventData = pd.read_csv(eventFile, delimiter="\t", names=eventColNames, header=None)
            self.evd_data = eventData

        return self.evd_data

    def fixation_data(self):
        if self.fxd_data is None:
            fixationFile = self.filepath + "p1." + self.graph_or_tree + "FXD.txt"
            fixColNames = ["number", "time", "duration", "x", "y"]
            fixData = pd.read_csv(fixationFile, delimiter="\t", names=fixColNames, header=None)
            self.fxd_data = fixData

        return self.fxd_data

    def gaze_data(self):
        if self.gzd_data is None:
            gazeFile = self.filepath + "p1." + self.graph_or_tree + "GZD.txt"
            gazeColNames = ["time", "number",
                            "screenXR", "screenYR", "camXR", "camYR", "distanceR", "pupilR", "validityR",
                            "screenXL", "screenYL", "camXL", "camYL", "distanceL", "pupilL", "validityL"
                            ]
            gazeData = pd.read_csv(gazeFile, delimiter="\t", names=gazeColNames, header=None)
            self.gzd_data = gazeData

        return self.gzd_data
        #remove validity codes 2 or higher (as recommended in manual)
        #validData = gazeData.query('validityR <= 2 and validityL <= 2')
        #return validData

    def keyboard_data(self):
        if self.kbd_data is None:
            df = self.event_data()
            #df = self.event_data(graph_or_tree)
            labels = (df.event != df.event.shift()).cumsum()
            
            df['wordGroup']= labels
            print(df['wordGroup'])
            def concatInput(series):
                mask = (series.str.len()==1)
                return series.loc[mask].str.cat()
            groups = df[df.event=='Keyboard']\
                .groupby(['wordGroup'])\
                .agg({'time': ['min', 'max'], 'description': concatInput})
            groups.columns = groups.columns.get_level_values(1)
            groups.filter(items=['min', 'max', 'concatInput'])
            groups.columns = ['startTime', 'endTime', 'typedString']
            #print(groups)
            self.kbd_data = groups

        #print(groups)
        return self.kbd_data

if __name__ == '__main__':
    test = 0