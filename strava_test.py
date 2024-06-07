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
    CLIENT_ID, CLIENT_SECRET = (
        open("~/.stuff/dilly.secret").read().strip().split(","))

    # print(CLIENT_ID)

    url = client.authorization_url(
            client_id=CLIENT_ID,
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
        elif (i > 5):
            print("Can't find the code, exiting!")
            return ERROR
        access_code_url = input("Paste the link returned after the \
                        confirmation question here: ")
        print("\n")
        CODE = re.search("(?<=&code=).*?(?=&scope)", access_code_url)
        i += 1
    print("Code found!\n")
    time.sleep(3)

    with open(Path("~/.stuff/strava_client_obj.pickle"), "wb") as file:
        pickle.dump(client, file)

    with open(Path("~/.stuff/strava_access_code.pickle"), "wb") as file:
        pickle.dump(CODE, file)

    return client, CODE

    # client_obj.pickle

    # http://127.0.0.1:5000/authorization?state=&code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&scope=read,activity:read_all,profile:read_all,read_all
    # write pickle file with client

    # return CLIENT_ID, CLIENT_SECRET


def get_token(CLIENT_ID, CLIENT_SECRET, ACCESS_CODE, client):

    # CODE = "57b74ab72cefdbc4cc7c7e7324291cf91ea54cd1"

    token_response = client.exchange_code_for_token(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=CODE
            )
    print("got token!")
    access_token = token_response["access_token"]
    refresh_token = token_response["refresh_token"]
    expires_at = token_response["expires_at"]

    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at

    strava_token_package = str(access_token) + "," + str(refresh_token) + ","\
        + str(expires_at)
    token_package_path = Path("~/.stuff/strava_token_package.pickle")

    with open(token_package_path, "wb") as file:
        pickle.dump(strava_token_package, file)

    return strava_token_package


def something():

    athlete = client.get_athlete()
    print(
        "For {id}, I now have an access token {token}".format(
            id=athlete.id, token=access_token
        )
    )

    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(
            client_id=ID, client_secret=SECRET,
            refresh_token=client.refresh_token
        )
        access_token = refresh_response["access_token"]
        refresh_token = refresh_response["refresh_token"]
        expires_at = refresh_response["expires_at"]

    return athlete, client


def get_secrets():
    strava_secrets_path = Path("~/.stuff/dilly.secret")
    with open(strava_secrets_path) as file:
        CLIENT_ID, CLIENT_SECRET = file.read().strip().split(",")

    return CLIENT_ID, CLIENT_SECRET

# For 118015943, I now have an access token
# d941db4044b70a14e8951ef57523bb44d65fdec7
# is this wrong
# http://127.0.0.1:5000/authorization?state=&code=23d52e19ff9e117cc3a134083cd92a834a1cc104&scope=read,activity:read_all,profile:read_all,read_all


def main():
    # strava_secrets_path = Path("~/.stuff/dilly.secret")
    # with open(strava_secrets_path) as file:
    #     CLIENT_ID, CLIENT_SECRET = file.read().strip().split(",")
    CLIENT_ID, CLIENT_SECRET = get_secrets()

    client_path = Path("~/.stuff/strava_client_obj.pickle")
    access_code_path = Path("~/.stuff/strava_access_code.pickle")

    if (not access_code_path.exists() OR not client_path.exists()):
        print("access_code or client_obj not found, let's generate them.\n")
        time.sleep(1)
        client, code = get_code()      # client, code = get_code()

    # read in pickle objects
    with open(client_path) as file:
        client = pickle.load(file)
    with open(access_code_path) as file:
        ACCESS_CODE = pickle.load(file)

    get_token(CLIENT_ID, CLIENT_SECRET, ACCESS_CODE, client)








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
