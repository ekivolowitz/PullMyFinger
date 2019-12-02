#!/usr/bin/python3
from github import Github
from github.GithubException import UnknownObjectException
import os
import sys
import argparse
import getpass
from pprint import pprint
parser = argparse.ArgumentParser()

if __name__ == "__main__":
    parser.add_argument("organization", help="List the name of an organization that you'd like to pull down.")
    args = parser.parse_args()
    username = input("Username: ")
    password = getpass.getpass("password: ")
    g = Github(username, password)
    try:
        org = g.get_organization(args.organization)
    except UnknownObjectException as e:
        print("Organization: '{}' does not exist. Please enter a valid organization name.".format(args.organization))
        sys.exit(1)
    for project in org.get_repos():
        repo = project._rawData['html_url']
        location = args.organization + os.sep + project.name
        domain = repo.split("https://")[1]
        url = "https://{}:{}@{}".format(username, password, domain)
        os.system("git clone {} {}".format(url, location))
