from pythainlp import word_tokenize as tokenize
from pythainlp.util import *
from tqdm.auto import tqdm
tqdm.pandas()

class WB:

    def __init__(self, newmm_filename):
        self.newmm_stopword = self.read_stop_word(newmm_filename)
        self.newmm_WB = []

    def read_stop_word(self, filename):
        text_file = open(f"../assets/Stop_Word_List/{filename}.txt", "r", encoding='utf-8')
        content = text_file.read()
        dict_list = content.split("\n")
        text_file.close()
        return dict_list

    def wb(self, news):
        segment = tokenize(str(news),keep_whitespace=False,engine="newmm")
        return segment

    def word_break(self, df):
        l = len(df)

        list_column = df.columns.values.tolist()
        column_name = list_column[1]

        for i in tqdm(range(l)):
            wb_list = self.wb(df.iloc[i][column_name])
            remove_sw = [word for word in wb_list  if word not in self.newmm_stopword]
            self.newmm_WB.append(remove_sw)