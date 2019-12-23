# GithubRepoPull
## Before Running
```
pip install PyGithub
```
You must create a file in your home directory called `.pullmyfinger.json`.
To get a [Personal Access Token, visit this page.](https://github.com/settings/tokens)
You must give the token the `repo` scope to allow `pullmyfinger` to work.
```json
# ~/.pullmyfinger.json
{
	"access_token" : "<your access token here>"
}
```

## Usage
```
usage: pullmyfinger.py [-h] [-q] [-l] [-L] organization

positional arguments:
  organization  List the name of an organization that you'd like to inspect / clone locally.

optional arguments:
  -h, --help    show this help message and exit
  -q, --quiet   Quiet mode only outputs the intended output of the command
                ignoring all else (the PullMyFinger ASCII art at the top, for
                instance). For example, `pullmyfinger -lq organization` would
                only print the names of the repositories within
                `organization`.
  -l, --list    List the repositories in the organization.
  -L            Display repositories within organization that contain commits
                that have a HEAD on a different commit from your local version.
```
