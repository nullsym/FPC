#!/usr/bin/env python

#################
# Documentation #
#################
# https://kazuar.github.io/scraping-tutorial/
# http://docs.python-requests.org/en/master/
#
# Technologies the website uses
# (1) Dojo Toolkit: DHTML + AJAX functions
# (2) WebSphere Application Server (WAS)

import os, sys
import configparser
import requests
# For YEAR and WEEK
import time

###############
# Global vars #
###############
DIR_NAME = os.path.split(os.path.abspath(sys.argv[0]))[0]
DIR_NAME = DIR_NAME.rpartition("FPC")
DIR_NAME = DIR_NAME[0] + DIR_NAME[1]
YEAR = time.strftime("%Y")
WEEK = time.strftime("%U")


#############
# Functions #
#############
def sanity_check():
    if "FPC" not in DIR_NAME:
        sys.exit("[EROR] The name of this project must be FPC.")

def file_exists(file_name, bool_retrn=False):
    if not os.path.exists(file_name):
        if not bool_retrn:
            sys.exit("[ERROR] The file " + file_name + " does not exist")
        else:
            return False
    return True

def settings(request):
    sanity_check()
    if file_exists(DIR_NAME + '/settings.ini', True):
        config = configparser.ConfigParser()
        config.read(DIR_NAME + '/settings.ini')
        # [Auth]
        if request == "username":
            return config['Auth']['user_name']
        elif request == "password":
            return config['Auth']['password']
        elif request == "account_number":
            return config['Auth']['account_number']
        elif request == "zip":
            return config['Auth']['zip_code']

        # [Pushover]
        elif request == "po_token":
            return config['Pushover']['token']
        elif request == "po_user":
            return config['Pushover']['user']
    else:
        sys.exit("Move {}/txt/settings.ini.skel to {}/settings.ini".format(DIR_NAME, DIR_NAME))


def get_session(option):
    sanity_check()
    session_requests = requests.session() # Session object that will allow us to persist the login session
    # Perform login: Your username and password are sent on a GET request to /api/resources/login
    # as: Authorization: Basic <base64_of_your_username_plus_password>
    login_url =  "https://www.fpl.com/api/resources/login?_="
    result = session_requests.get(login_url, auth=requests.auth.HTTPBasicAuth(settings("username"), settings("password")))

    if option == "yearly":
        url = "https://www.fpl.com/api/resources/account/" + settings("account_number") + "/energyUsage"
        result = session_requests.get(url)
        return result

    elif option == "monthly" or option == "daily":
        url = "https://app.fpl.com/wps/myportal/EsfPortal"
        result = session_requests.get(url)
        url = "https://app.fpl.com/wps/myportal/"
        result = session_requests.get(url)
        return result

    sys.exit("[ERROR] An error ocurred in fpc.get_session")


########
# Main #
########
if __name__ == '__main__':
    sanity_check()
    session_requests = requests.session()
    login_url =  "https://www.fpl.com/api/resources/login?_="
    result = session_requests.get(login_url, auth=requests.auth.HTTPBasicAuth(settings("username"), settings("password")))
    print(result)
    print(result.headers, "\n\n")

    url = "https://www.fpl.com/api/resources/header?_="
    result = session_requests.get(url)
    print(result)
    print(result.headers, "\n\n")

    url = "https://app.fpl.com/wps/myportal/EsfPortal"
    result = session_requests.get(url)
    print(result)
    print(result.headers, "\n\n")

    url = "https://app.fpl.com/wps/myportal/"
    result = session_requests.get(url)
    print(result)
    print(result.headers, "\n\n")
