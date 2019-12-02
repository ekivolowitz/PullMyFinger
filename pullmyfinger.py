#!/usr/bin/python3

from github import Github
from github.GithubException import UnknownObjectException
import os
import sys
import argparse
import getpass
from pprint import pprint
from consts import pull_my_finger, displaying
parser = argparse.ArgumentParser()

def ls(org, org_name):
    projects = "\n"
    for project in org.get_repos():
        projects += project.name + "\n"
    print(displaying.format(org_name, projects))
 
def clone(org, organization_name, username, password):
    for project in org.get_repos():
        repo = project._rawData['html_url']
        location = organization_name + os.sep + project.name
        domain = repo.split("https://")[1]
        url = "https://{}:{}@{}".format(username, password, domain)
        os.system("git clone {} {}".format(url, location))

if __name__ == "__main__":
    print(pull_my_finger)

    parser.add_argument("organization", help="List the name of an organization that you'd like to pull down.")
    parser.add_argument("-l", "--list", action="store_true", help="List the repositories in the organization.")
    args = parser.parse_args()

    username = input("Username: ").strip()
    password = getpass.getpass("password: ").strip()

    g = Github(username, password)

    try:
        org = g.get_organization(args.organization)
    except UnknownObjectException as e:
        print("Organization: '{}' does not exist. Please enter a valid organization name.".format(args.organization))
        sys.exit(1)

    if args.list:
        ls(org, args.organization)
    else:
        clone(org, args.organization, username, password)
