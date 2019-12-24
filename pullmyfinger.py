#!/usr/bin/python3
# Author: Evan Kivolowitz | @ekivolowitz on github
# Date: 12-01-2019
# Description: A tool to help manage a Github Organization
# License: See Github Repository, GNU GPL 3.0
# Last used error code: 104
from github import Github
from github.GithubException import UnknownObjectException, BadCredentialsException
import os
import sys
import argparse
from pprint import pprint
from consts import pull_my_finger, displaying
import json

PAGE_SIZE = 30
parser = argparse.ArgumentParser()

def check_in_history(cursors, sha):
    for commit in cursors:
        if sha == commit.sha:
            return True
    return False

def get_commit_history(repo):
    return repo.get_commits()

def get_repo_head_local(relative_path, repo_name):
    '''
        file containing the head - .git/refs/heads/master
    '''
    path = os.path.expanduser(relative_path + os.sep + repo_name)
    master_path = '.git/refs/heads/master'
    try:
        with open(path + os.sep + master_path, 'r') as f:
            return f.read().strip()
    except:
        print("ERROR: Cannot read master head ref file for {}{}{}".format(relative_path, os.sep, repo_name))
        sys.exit(104)

def diff_ls(org, path):
    print()
    for project in org.get_repos():
        local_head = get_repo_head_local(path, project.name)
        commits = get_commit_history(project)

        last_page = int(commits.totalCount / PAGE_SIZE)
        lp = commits.get_page(0)
        github_most_recent_commit_sha = lp[0]
        if local_head == github_most_recent_commit_sha.sha:
            print("%-30s: remote equal to local." % (org.login + "/" + project.name))
            continue
        elif check_in_history(commits, local_head):
            print("%-30s: remote ahead of local" % (org.login + "/" +  project.name))
        else:
            print("%-30s: local ahead of remote" %(org.login + "/" + project.name))
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
def clone(org, organization_name, username, token):
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
        url = "https://{}:{}@{}".format(username, token, domain)
        os.system("git clone {} {}".format(url, location))

def get_token(path):
    try:
        with open(os.path.expanduser("~/.pullmyfinger.json"), 'r') as f:
            d = json.load(f)
            access_token = d['access_token']
            return access_token
    except:
        print("ERROR: Make sure you have your access token in ~/.pullmyfinger.json in the right format.")
        sys.exit(103)

if __name__ == "__main__":

    parser.add_argument("organization", help="List the name of an organization that you'd like to pull down.")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode only outputs the intended output\
            of the command ignoring all else (the PullMyFinger ASCII art at the top, for instance). \
            For example, `pullmyfinger -lq organization` would only print the \
            names of the repositories within `organization`.")
    parser.add_argument("-l", "--list", action="store_true", help="List the repositories in the organization.")
    parser.add_argument("-L", help="Path to an organization folder locally. Display repositories within organization that contain\
            commits that have a HEAD on a different commit.")
    args = parser.parse_args()

    if not args.quiet:
        print(pull_my_finger)

    if args.list and args.L:
        print("ERROR: Cannot use [--list, -l] with -L.")
        sys.exit(102)

    username = input("Username: ").strip()
    token = get_token("~/.pullmyfinger.json")
    g = Github(token)
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
        diff_ls(org, args.L)
    else:
        clone(org, args.organization, username, token)
