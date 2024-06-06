import time
from stravalib.client import Client
import numpy as np
import re
from pathlib import Path

# credit for this section due to
# https://medium.com/analytics-vidhya/
# accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17


def get_code():
    client = Client()
    DILLY_STRAVA_CLIENT_ID, DILLY_STRAVA_CLIENT_SECRET = (
        open("~/.stuff/dilly.secret").read().strip().split(","))

    # print(DILLY_STRAVA_CLIENT_ID)

    url = client.authorization_url(
            client_id=DILLY_STRAVA_CLIENT_ID,
            redirect_uri='http://127.0.0.1:5000/authorization',
            scope=['read_all', 'profile:read_all', 'activity:read_all'])
    print("\n Here's the confirmation url: \n")
    print(url)
    print("\n")
    time.sleep(3)
    CODE = None
    i = 0
    while (CODE is None):
        if (i > 0):
            print("Code not found!")
            time.sleep(1)

        access_code_url = input("Paste the link returned after the confirmation
                                question here: ")
        print("\n")
        CODE = re.search("(?<=&code=).*?(?=&scope)", access_code_url)
        i += 1
    print("Code found!\n")
    time.sleep(3)
    

    # http://127.0.0.1:5000/authorization?state=&code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&scope=read,activity:read_all,profile:read_all,read_all
    # write pickle file with client

    return DILLY_STRAVA_CLIENT_ID, DILLY_STRAVA_CLIENT_SECRET


def get_token(CODE, ID, SECRET):

    #CODE = "57b74ab72cefdbc4cc7c7e7324291cf91ea54cd1"

    token_response = client.exchange_code_for_token(
            client_id = ID,
            client_secret = SECRET,
            code = CODE
            )
    print("got token!")
    access_token = token_response["access_token"]
    refresh_token = token_response["refresh_token"]
    expires_at = token_response["expires_at"]

    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at

    athlete = client.get_athlete()
    print(
        "For {id}, I now have an access token {token}".format(
            id=athlete.id, token=access_token
        )
    )

    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(
            client_id=ID,
            client_secret=SECRET,
            refresh_token=client.refresh_token
        )
        access_token = refresh_response["access_token"]
        refresh_token = refresh_response["refresh_token"]
        expires_at = refresh_response["expires_at"]

    return athlete, client


# For 118015943, I now have an access token
# d941db4044b70a14e8951ef57523bb44d65fdec7

# http://127.0.0.1:5000/authorization?state=&code=23d52e19ff9e117cc3a134083cd92a834a1cc104&scope=read,activity:read_all,profile:read_all,read_all
def main():
    bin_path = Path("~/.stuff/pickle_file_access_code") # THIS IS GONNA NEED REPLACED
    if (!bin_path.exists())
        print("access_code not found!")
        get_code()

    else
        






    # ID, SECRET = get_code()
    # print(ID + "\n" + SECRET)
    # ID = 128025
    # SECRET = "fe4382cd7bde203c138fd28ea8db3da6a96efa46"
    # code = "23d52e19ff9e117cc3a134083cd92a834a1cc104"
    # athlete, client = get_token(code, ID, SECRET)
    # print(athlete)
    # print(client)
    # activities = client.get_activities()
    # act_arr = np.asarray(activities)
    # np.savetxt("foo.csv", act_arr, delimiter=",")


if __name__ == "__main__":
    main()
