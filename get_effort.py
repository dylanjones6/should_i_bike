import strava_get_activity
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
import pickle

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


def main():

    df = strava_get_activity.main()

    nrows = df.shape[0]
    print(nrows)

    date_today = datetime.datetime("%y%m%d%H%M%S")

    today_perc_exert_path = Path("/Users/jonesdr/"
                                 ".strava/perc_exert_{!S}".format(date_today))
    if (today_perc_exert_path.exists()):
        # MAKE AN IF PATH TO CHECK IF THERE'S ALREADY A FILE TO JUST APPEND TO
        with open(today_perc_exert_path, "rb") as file:
            perc_exert = pickle.load(file)

        past_rows = perc_exert.size
        i = past_rows
        series_getter(df, perc_exert, i)

    else:
        perc_exert = pd.Series()
        series_getter(df, perc_exert, 0)







if __name__ == "__main__":
    main()
