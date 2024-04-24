# Migration gitlab\github to github

this is a migration script written in python, it basically clones the links provided in the `utils/links.yaml` those links should be the ones that you want the request to hit with get so you should changed in order of what you need the script to do. (for more explanation go to the documentation of both api rest gitlab\github, there you will find a lot of information about endpoints)

The script clones those links using the access token provided in the env as a Bearer auth for the get petition. Then, the script will create a `data.yaml` in which you will find the names that the script will use to name those in the destination org repo. For gitlab it uses the full path with namespace included and for github only the name of the repo.

Finally it uses the GH cli to create the repos in the final destination that you should provide via .env variables

## Requirements

* Python 3.12
  * Installing requirements.txt
* GH tool
* Git
  * with corresponding ssh key access to clone repos
* Configure .env with:
  * `GITHUB_API_TOKEN`
  * `GITLAB_API_TOKEN`
  * `REPO_DESTINATION`