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

def ls(org):
    projects = []
    for project in org.get_repos():
        projects.append(project.name)
    return projects 
def clone(org, organization_name, username, password):
    for project in org.get_repos():
        repo = project._rawData['html_url']
        location = organization_name + os.sep + project.name
        domain = repo.split("https://")[1]
        url = "https://{}:{}@{}".format(username, password, domain)
        os.system("git clone {} {}".format(url, location))

if __name__ == "__main__":
    parser.add_argument("organization", help="List the name of an organization that you'd like to pull down.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode only outputs the intended output\
            of the command ignoring all else (the PullMyFinger ASCII art at the top, for instance). \
            For example, `pullmyfinger -l organization` would only print the \
            names of the repositories within `organization`.")
    parser.add_argument("-l", "--list", action="store_true", help="List the repositories in the organization.")
    args = parser.parse_args()

    if not args.quiet:
        print(pull_my_finger)

    username = input("Username: ").strip()
    password = getpass.getpass("password: ").strip()

    g = Github(username, password)

    try:
        org = g.get_organization(args.organization)
    except UnknownObjectException as e:
        print("Organization: '{}' does not exist. Please enter a valid organization name.".format(args.organization))
        sys.exit(1)

    if args.list:
        projects = ls(org)
        formatted_projects = "\n".join(projects)
        if args.quiet:
            print(formatted_projects)
        else:
            print(displaying.format(args.organization, formatted_projects))
    else:
        clone(org, args.organization, username, password)
