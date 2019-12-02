#!/usr/bin/python3
# Author: Evan Kivolowitz | @ekivolowitz on github
# Date: 12-01-2019
# Description: A tool to help manage a Github Organization
# License: See Github Repository, GNU GPL 3.0
from github import Github
from github.GithubException import UnknownObjectException, BadCredentialsException
import os
import sys
import argparse
import getpass
from pprint import pprint
from consts import pull_my_finger, displaying
parser = argparse.ArgumentParser()

def ls(org):
    '''
    ls - Lists all the repository names in an organization
    params:
        org - Organization - PyGithub object representing the retrieved organization.
    returns:
        list containing strings of the repository names
    '''
    projects = []
    for project in org.get_repos():
        projects.append(project.name)
    return projects 
def clone(org, organization_name, username, password):
    '''
    clone - clones each repository into your $cwd/organization_name/<repository_name>
    params:
        org - Organization - PyGithub object representing the retrieved organization.
        organization_name - str - The name of the organization
        username - str - The entered github username from the user
        password - str - The entered github password from the user
    returns:
        None
    '''
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
            For example, `pullmyfinger -lq organization` would only print the \
            names of the repositories within `organization`.")
    parser.add_argument("-l", "--list", action="store_true", help="List the repositories in the organization.")
    parser.add_argument("-L", action="store_true", help="Display repositories within organization that contain\
            commits that have a HEAD on a different commit.")
    args = parser.parse_args()

    if not args.quiet:
        print(pull_my_finger)

    if args.list and args.L:
        print("ERROR: Cannot use [--list, -l] with -L.")
        sys.exit(102)

    username = input("Username: ").strip()
    password = getpass.getpass("password: ").strip()

    g = Github(username, password)

    try:
        org = g.get_organization(args.organization)
    except BadCredentialsException as e:
        print("ERROR: Please enter valid credentials.")
        sys.exit(100)
    except UnknownObjectException as e:
        print("Organization: '{}' does not exist. Please enter a valid organization name.".format(args.organization))
        sys.exit(101)

    if args.list:
        projects = ls(org)
        formatted_projects = "\n".join(projects)
        if args.quiet:
            print(formatted_projects)
        else:
            print(displaying.format(args.organization, formatted_projects))
    elif args.L:
        print("Coming soon!")
    else:
        clone(org, args.organization, username, password)
