import datetime

import pandas as pd
import tushare as ts
from dateutil import parser


class StaticInfo(object):
    storage_basic_path = "../data_storage/"
    storage_update_date = "../data_storage/date"
    stock_pool = {
        '000002': 11476, '000725': 18320, '600030': 41874, '600036': 17808, '600048': 40049, '600068': 20125,
        '600690': 18380, '601668': 12735, '600728': 32190
    }

    data_type = {
        "industry": storage_basic_path + "industry_data.csv",
        "concept": storage_basic_path + "concept_data.csv",
        "area": storage_basic_path + "area_data.csv",
    }

    @staticmethod
    def get_stock_pool():
        return StaticInfo.stock_pool

    @staticmethod
    def get_stock_hist_data_path(code):
        if len(str(code)) == 6:
            templ = "{0}{1}{2}.csv".format(StaticInfo.storage_basic_path, "stock_hist_data/", str(code))
            return templ
        else:
            print "wrong type of code style"
            return None

    @staticmethod
    def init_stock_pool():

        total_value = 0
        for v in StaticInfo.stock_pool.values():
            total_value += v

        for stock in StaticInfo.stock_pool:
            StaticInfo.stock_pool[stock] = round(float(StaticInfo.stock_pool[stock]) / total_value * 100, 4)

        return StaticInfo.stock_pool


class InitStaticInfo(object):
    @staticmethod
    def _get_stock_hist_data(code_list=list()):
        if code_list:
            for code in code_list:
                hist_path = StaticInfo.get_stock_hist_data_path(code)
                print hist_path
                if hist_path:
                    ts.get_hist_data(code).to_csv(hist_path, index=False)

    @staticmethod
    def update_static_info(force=False):
        now = datetime.datetime.now()
        t = None
        rf = open(StaticInfo.storage_update_date, "r")
        line = rf.read()
        rf.close()
        wf = open(StaticInfo.storage_update_date, "w")
        if line:
            t = parser.parse(line)
        else:
            wf.write(str(now))
        delta_day = (now - t).days
        if delta_day > 0 or force:
            wf.write(str(now))
            print "static info need to update"
            ts.get_industry_classified().to_csv(StaticInfo.data_type["industry"], index=False)
            ts.get_concept_classified().to_csv(StaticInfo.data_type["concept"], index=False)
            ts.get_area_classified().to_csv(StaticInfo.data_type["area"], index=False)
            InitStaticInfo._get_stock_hist_data(StaticInfo.get_stock_pool().keys())

        wf.close()

    @staticmethod
    def get_static_info(info_type=None):
        if info_type and info_type in StaticInfo.data_type:
            df = pd.read_csv(StaticInfo.data_type[info_type], dtype={"code": str})
            return df
        return pd.DataFrame()


class InvestmentModel(object):
    def __init__(self, *args, **kwargs):
        self.code = kwargs.get("code", None)
        self.concept = kwargs.get("concept", None)
        self.area = kwargs.get("area", None)
        self.industry = kwargs.get("industry", None)

    def __str__(self):
        return "-----\ncode: {0}\narea: {1}\nconcept: {2}\nindustry: {3}".format(self.code, self.area,
                                                                                 ";".join(self.concept),
                                                                                 self.industry)


class AnalyseInvestment(object):
    def __init__(self, analyse_dim=list()):
        self.analyse_dim = analyse_dim if analyse_dim else ["industry", "area", "concept"]
        self.stock_pool = StaticInfo.init_stock_pool()
        self.si = InitStaticInfo()
        self.res = list()

    def start_analyse(self):
        for code in self.stock_pool:
            temp_dict = dict(code=code)
            for dim in self.analyse_dim:
                data = InitStaticInfo.get_static_info(info_type=dim)
                if "name" not in temp_dict:
                    temp_dict["name"] = data[data.code == code]["name"].drop_duplicates().values[0]
                if "area" not in temp_dict and dim == "area":
                    temp_dict["area"] = data[data.code == code]["area"].drop_duplicates().values[0]
                if "concept" not in temp_dict and dim == "concept":
                    temp_dict["concept"] = data[data.code == code]["c_name"].drop_duplicates().tolist()
                if "industry" not in temp_dict and dim == "industry":
                    temp_dict["industry"] = data[data.code == code]["c_name"].drop_duplicates().values[0]

            self.res.append(InvestmentModel(**temp_dict))
        return self.res


if __name__ == '__main__':
    InitStaticInfo.update_static_info(force=True)
    ai = AnalyseInvestment()
    for stock in ai.start_analyse():
        print stock
