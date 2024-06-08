import get_strava_activity
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
import pickle
import os
import regex as re
import time

# perc_exert stands for perceived exertion


def series_getter(df, perc_exert, i_start):

    perc_exert = perc_exert.to_list()
    nrows = df.shape[0]
    i = i_start

    while (i < nrows):
        num_checked = None

        while (num_checked is None):
            col_name = df.loc[i, "name"]
            num_in = input("What was the effort level from "
                           "0 to 9 for:\n{!s}\n".format(col_name))
            num_in = int(num_in)

            if (num_in in range(-1, 10)):
                print(num_in)
                num_checked = num_in

            if (num_checked == -1):
                num_checked = np.nan

        perc_exert.append(num_checked)
        i += 1

    perc_exert = pd.Series(perc_exert)

    return perc_exert


def get_recent_path():
    strava_path = Path("/Users/jonesdr/.strava/")
    dir_list = os.listdir(strava_path)
    print(dir_list)
    time.sleep(3)
    # match_list = re.findall(r"perc_exert_\d", dir_list)
    match = re.compile(r"perc_exert_\d")
    match_list = list(filter(match.search, dir_list))
    print(match_list)
    time.sleep(3)
    if (match_list == []):
        return None
    if (len(match_list) == 1):
        recent_file_name = match_list[0]
    else:
        # dates = re.findall(r"\d", match_list).group()
        match = re.compile(r"\d{12}")
        dates = list(filter(match.search, match_list))
        print("Dates: ", dates)
        dates = [int(i) for i in dates]
        recent = max(dates)
        print("Recent: ", recent)
        # recent_file_name = re.search(r"perc_exert_" +
        #                              re.escape(recent), dir_list).group()
        match = re.compile(r"perc_exert_" + re.escape(recent))
        recent_file_name = list(filter(match.search, dir_list))
        print("recent_file_name: ", recent_file_name)

    recent_file_path = strava_path + recent_file_name

    return recent_file_path


def main():

    get_recent_path()

    return # for testing!

    df = get_strava_activity.main()

    # nrows = df.shape[0]
    # print(nrows)

    today_date = datetime.datetime("%y%m%d_%H%M%S")
    today_date_str = str(today_date)

    today_perc_exert_path = Path("/Users/jonesdr/.strava"
                                 "/perc_exert_{!S}".format(today_date_str))
    recent_perc_exert_path = get_recent_path()

    if (recent_perc_exert_path is not None):
        # MAKE AN IF PATH TO CHECK IF THERE'S ALREADY A FILE TO JUST APPEND TO
        with open(today_perc_exert_path, "rb") as file:
            perc_exert = pickle.load(file)

        past_rows = perc_exert.size
        i = past_rows
        perc_exert = series_getter(df, perc_exert, i)

    else:
        perc_exert = pd.Series()
        perc_exert = series_getter(df, perc_exert, 0)







if __name__ == "__main__":
    main()
