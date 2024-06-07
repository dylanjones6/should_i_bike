import time
from stravalib.client import Client
# import numpy as np
import re
from pathlib import Path
import pickle
import os

# credit for this section due to
# https://medium.com/analytics-vidhya/
# accessing-user-data-via-the-strava-api-using-stravalib-d5bee7fdde17


def get_code():
    client = Client()
    client_id, client_secret, client_refresh = (
        open("/Users/jonesdr/.stuff/dilly.secret").read().strip().split(","))

    # print(client_id)

    url = client.authorization_url(
            client_id=client_id,
            redirect_uri='http://127.0.0.1:5000/authorization',
            scope=['read_all', 'profile:read_all', 'activity:read_all'])
    print("\n Here's the confirmation url: \n")
    print(url)
    print("\n")
    time.sleep(3)
    access_code = None
    i = 0
    while (access_code is None):
        if (i > 0):
            print("Code not found!\n")
            time.sleep(1)
        elif (i > 5):
            print("Can't find the code, exiting!\n")
            return
        access_code_url = input("Paste the link returned after the "
                                "confirmation question here: ")
        print("\n")
        access_code_re = re.search("(?<=&code=).*?(?=&scope)", access_code_url)
        if (access_code_re is not None):
            access_code = access_code_re.group(0)
        i += 1
    print("Code found!\n")
    print("Code is: " + access_code + "\n")
    time.sleep(3)

    with open(Path("/Users/jonesdr/"
                   ".stuff/strava_client_obj.pkl"), "wb") as file:
        pickle.dump(client, file)
    access_code_path = Path("/Users/jonesdr/.stuff/strava_access_code.pkl")
    with open(access_code_path, "wb") as file:
        pickle.dump(access_code, file)

    return client, access_code

    # client_obj.pkl

    # http://127.0.0.1:5000/authorization?state=&code=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&scope=read,activity:read_all,profile:read_all,read_all
    # write.pkl file with client

    # return client_id, client_secret


def get_token(client_id, client_secret, client_refresh, access_code, client):

    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(
            client_id=client_id, client_secret=client_secret,
            refresh_token=client_refresh
        )
        access_token = refresh_response["access_token"]
        refresh_token = refresh_response["refresh_token"]
        expires_at = refresh_response["expires_at"]

    token_response = client.exchange_code_for_token(
            client_id=client_id,
            client_secret=client_secret,
            code=access_code
            )
    print("got token!\n")
    access_token = token_response["access_token"]
    refresh_token = token_response["refresh_token"]
    expires_at = token_response["expires_at"]

    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at

    strava_token_package = str(access_token) + "," + str(refresh_token) + ","\
        + str(expires_at)

    token_package_path = Path("/Users/jonesdr/.stuff/strava_token_package.pkl")
    # client_final_path = Path("/Users/jonesdr/.stuff/client_final.pkl")

    with open(token_package_path, "wb") as file:
        pickle.dump(strava_token_package, file)
    # with open(client_final_path, "wb") as file:
    #     pickle.dump(client, file)

    return access_token, refresh_token, expires_at, client


def get_token2(client_id, client_secret, client_refresh, access_code, client):

    # if time.time() > client.token_expires_at:
    #     refresh_response = client.refresh_access_token(
    #         client_id=client_id, client_secret=client_secret,
    #         refresh_token=client_refresh
    #     )
    #     access_token = refresh_response["access_token"]
    #     refresh_token = refresh_response["refresh_token"]
    #     expires_at = refresh_response["expires_at"] GOTTA REMEMBER TO CHANGE TO LAST
    this_token_time_path = Path("/Users/jonesdr/"
                                ".stuff/this_token_time.pkl")
    last_token_time_path = Path("/Users/jonesdr/"
                                ".stuff/last_token_time.pkl")
    access_token_package_path = Path("/Users/jonesdr/"
                                     ".stuff/strava_token_package.pkl")
    this_token_time = str(time.time())

    # if (this_token_time_path.exists()):
    #     os.replace(this_token_time_path, this_token_time_path)
    # else:
    #     with open(this_token_time_path, "wb") as file:
    #         pickle.dump(this_token_time, file)

    with open(this_token_time_path, "wb") as file:
        pickle.dump(this_token_time, file)

    if (access_token_package_path.exists()):

        with open(access_token_package_path, "rb") as file:
            access_token_package = pickle.load(file)
        access_token, refresh_token, expires_at = \
            access_token_package.strip().split(",")
        token_response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_at": expires_at,
        }
    else:

        if (last_token_time_path.exists()):
            print("Found previous token request time\n")
            with open(last_token_time_path, "rb") as file:
                last_token_request = pickle.load(file)

            time_gap = (60 * 60) * 4.9
            if ((float(last_token_request) + time_gap) >
                    (float(this_token_time))):

                if (access_token_package_path.exists()):
                    print("Found the access_token_package, let's read it\n")
                    with open(access_token_package_path, "rb") as file:
                        package_raw = pickle.load(file)
                    access_token, refresh_token, expires_at = \
                        package_raw.strip().split(",")
                    token_response = {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "expires_at": expires_at,
                            }
                else:
                    # then exchange code for token
                    print("We can use the access code we "
                          "already got earlier\n")
                    token_response = client.exchange_code_for_token(
                        client_id=client_id,
                        client_secret=client_secret,
                        code=access_code
                    )
            else:
                # refresh access token
                print("The last access code is too old, "
                      "so we'll get a new one\n")
                token_response = client.refresh_access_token(
                    client_id=client_id, client_secret=client_secret,
                    refresh_token=client_refresh
                )
        else:
            print("No previous token made, so we'll make our first one\n")
            print(client_id + ";" + client_secret + ";" + access_code + "\n")
            token_response = client.exchange_code_for_token(
                client_id=client_id,
                client_secret=client_secret,
                code=access_code
            )
    print("Token retrieved\n")

    # if (this_token_time_path.exists()):
    #     os.replace(last_token_time_path, last_token_time_path)
    # else:
    #     with open(last_token_time_path, "wb") as file:
    #         pickle.dump(this_token_time, file)

    with open(last_token_time_path, "wb") as file:
        pickle.dump(this_token_time, file)

    os.remove(this_token_time_path)

    access_token = token_response["access_token"]
    refresh_token = token_response["refresh_token"]
    expires_at = token_response["expires_at"]

    client.access_token = access_token
    client.refresh_token = refresh_token
    client.token_expires_at = expires_at

    strava_token_package = str(access_token) + "," + str(refresh_token) + ","\
        + str(expires_at)

    token_package_path = Path("/Users/jonesdr/.stuff/strava_token_package.pkl")
    # client_final_path = Path("/Users/jonesdr/.stuff/client_final.pkl")

    with open(token_package_path, "wb") as file:
        pickle.dump(strava_token_package, file)

    # with open(client_final_path, "wb") as file:
    #     pickle.dump(client, file)

    return access_token, refresh_token, expires_at, client


"""
def something(client):

    athlete = client.get_athlete()
    print(
        "I now have a access token {token} for id {id}\n".format(
             token=access_token, id=athlete.id
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
"""


def get_secrets():
    strava_secrets_path = Path("/Users/jonesdr/.stuff/dilly.secret")
    with open(strava_secrets_path) as file:
        client_id, client_secret, client_refresh = \
            file.read().strip().split(",")

    return client_id, client_secret, client_refresh


def main():

    client_id, client_secret, client_refresh = get_secrets()

    access_code_path = Path("/Users/jonesdr/.stuff/strava_access_code.pkl")
    client_obj_path = Path("/Users/jonesdr/.stuff/strava_client_obj.pkl")

    if (not access_code_path.exists() or not client_obj_path.exists()):
        print("access_code not found or client_obj not found"
              ", let's get them.\n")
        time.sleep(1)
        client, access_code = get_code()      # client, code = get_code()
    else:
        # read in.pkl objects
        print("access_code found, let's read it and locate a client obj.\n")
        # with open(client_path) as file:
        #     client = pickle.load(file)
        with open(access_code_path, "rb") as file:
            access_code = pickle.load(file)
        with open(client_obj_path, "rb")as file:
            client = pickle.load(file)

    print(client_id)
    print(client_secret)
    print(client_refresh)
    print(access_code)
    print(client)

    access_token, refresh_token, expires_at, client = get_token2(
            client_id, client_secret, client_refresh, access_code, client)
    """
    access_token_package_path = Path("/Users/jonesdr/.stuff/\
                                     strava_token_package.pkl")

    if (not access_token_package_path.exists()):
        print("Couldn't find the access token package, let's make one!\n")
        time.sleep(1)
        access_token, refresh_token, expires_at = get_token2(client_id,
            client_secret, client_refresh, access_code, client)
    else:
        print("Found the access_token_package, let's read it.")
        with open(access_token_package_path) as file:
            package_raw = pickle.load(file)
        access_token, refresh_token, expires_at = \
            package_raw.strip().split(",")
    """
    activities = client.get_activities()

    for activity in activities:
        print(activity)

    return activity









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
