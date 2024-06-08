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
    i = len(perc_exert)
    # i = i_start

    while (i < nrows):
        num_checked = None

        while (num_checked is None):
            col_name = df.loc[i, "name"]
            print("Press \"q\" if you want to quit, \"b\" to go back")
            num_in = input("What was the effort level from "
                           "0 to 9 (-1 if you didn't measure) "
                           "for:\n{!s}\n".format(col_name))
            if (num_in == "b" and i != 0):
                i -= 1
                perc_exert.pop()
                continue
            elif (num_in == "b" and i == 0):
                return pd.Series()
            if (num_in == "q"):
                perc_exert = pd.Series(perc_exert)
                return perc_exert
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
    elif (len(match_list) == 1):
        recent_file_name = match_list[0]
    else:
        # dates = re.findall(r"\d", match_list).group()
        # match = re.compile(r"\d{6}_\d{6}")
        # dates = list(filter(match.search, match_list))
        dates = []
        for i in match_list:
            match = re.search(r"\d{6}_\d{6}$", i)
            if (match is not None):
                dates.append(match.group())
        print("Dates: ", dates)
        # dates = [int(i) for i in dates]
        recent = max(dates)
        print("Recent: ", recent)
        # recent_file_name = re.search(r"perc_exert_" +
        #                              re.escape(recent), dir_list).group()
        match = re.compile(r"perc_exert_" + re.escape(recent))
        recent_file_name = list(filter(match.search, dir_list))[0]
        # recent_file_name = re.search(r"perc_exert_" +
        #                             re.escape(recent), dir_list).group()
        print("recent_file_name: ", recent_file_name)

    recent_file_path = str(strava_path) + "/" + recent_file_name
    # print(recent_file_path)
    return recent_file_path


def main():

    recent_perc_exert_path = get_recent_path()

    # df = get_strava_activity.main()
    df_path = Path("/Users/jonesdr/.strava/strava_df")
    # add a way to make this most recent as well
    with open(df_path, "rb") as file:
        df = pickle.load(file)

    nrows = df.shape[0]
    # print(nrows)

    today_date = datetime.datetime.today().strftime("%y%m%d")
    today_time = datetime.datetime.today().strftime("%H%M%S")
    today = today_date + "_" + today_time
    today_date_str = str(today)

    today_perc_exert_path = Path("/Users/jonesdr/.strava"
                                 "/perc_exert_" + today_date_str)
    print(today_perc_exert_path)
    recent_perc_exert_path = get_recent_path()

    if (recent_perc_exert_path is not None):
        # MAKE AN IF PATH TO CHECK IF THERE'S ALREADY A FILE TO JUST APPEND TO
        with open(recent_perc_exert_path, "rb") as file:
            perc_exert = pickle.load(file)
        past_nrows = perc_exert.size
        if (nrows == past_nrows):
            # use_recent = False
            # while (use_recent) ...
            while (True):
                use_recent = input("Past file found with all perceived "
                                   "exertion ratings, want to use it? [y]/n\n")
                use_recent = use_recent.lower()
                if (use_recent == "y" or use_recent == "yes"
                        or use_recent == ""):
                    return 0  # exit code for no written file just using most
                              # recent files
                elif (use_recent == "n" or use_recent == "no"):
                    while (True):
                        response = input("Would you like to start a new file, "
                                         "select a different file, start at a "
                                         "certain point in this file, or go "
                                         "back? n/s/c/b\n")
                        response = response.lower()
                        # if (response == "n"):
                            # perc_exert = series_getter(df, pd.Dataseries(), 0)
                            # break
                            # refactor code for this, can't get out of nested
                            # loops
                        if (response == "b"):
                            break
                            
        else:
            i = past_nrows
            perc_exert = series_getter(df, perc_exert, i)

    else:
        perc_exert = pd.Series()
        perc_exert = series_getter(df, perc_exert, 0)
    
    print(perc_exert)

    # add check to remove extra perc_exert files based on contents

    with open(today_perc_exert_path, "wb") as file:
        pickle.dump(perc_exert, file)

    return 1





if __name__ == "__main__":
    main()
