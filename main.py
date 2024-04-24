#! /usr/bin/env python3
import subprocess
import os
from requests import Response
from colorama import init, Fore, Back, Style
from tqdm import tqdm
import classes as c

GITHUB_API_TOKEN=os.environ['GITHUB_API_TOKEN']
GITLAB_API_TOKEN=os.environ['GITLAB_API_TOKEN']
ORG_DESTINATION=os.environ['ORG_DESTINATION']

def read_links():
  links = c.Reader('utils/links.yaml')
  return links.read()

def get_gitlab_data(gitlab ,url: str):
  data: Response = gitlab.get(url)
  repos: list = []
  for item in data.json():
      repos.append({'ssh_url_to_repo': item['ssh_url_to_repo'], 'path_with_namespace': item['path_with_namespace'].replace('/', '-')})
  return repos

def get_github_data(github, url: str):
  data: Response = github.get(url)
  repos: list = []
  for item in data.json():
      repos.append({'ssh_url': item['ssh_url'], 'name': item['name']})
  return repos

def create_clone_repos_gitlab(gitlab_repos):
    for repo in tqdm(gitlab_repos, desc="Syncing repositories - Gitlab", unit="repos"):
        repo_path = f'../gitlab/{repo["path_with_namespace"]}'
        if os.path.exists(repo_path):
            subprocess.run(['rm', '-rf', repo_path])
        repository = c.Repository(
            f"https://api.github.com/repos/{ORG_DESTINATION}/{repo['path_with_namespace']}",
            GITHUB_API_TOKEN
        )
        subprocess.run(['git', 'clone', repo['ssh_url_to_repo'], repo_path])
        os.chdir(repo_path)
        try:
            print(Fore.GREEN + f'Updating repo {repo["path_with_namespace"]} at dir {os.getcwd()}' + Style.RESET_ALL)
            subprocess.run(['git fetch --all'], shell=True, check=True)
            subprocess.run(['git pull --all'], shell=True, check=True)
            print(Fore.BLUE + str(repository.exists()) + Style.RESET_ALL)
            if repository.exists() == 1:  # repo exists
                print(Fore.YELLOW + f'Updating repo {repo["path_with_namespace"]}' + Style.RESET_ALL)
                subprocess.run([
                    f'git remote add upstream git@github.com:{ORG_DESTINATION}/{repo["path_with_namespace"]}.git'
                ], shell=True, check=True)
                subprocess.run([
                    f'git push upstream --tags "refs/remotes/origin/*:refs/heads/*"'
                ], shell=True, check=True)
            else:  # repo doesn't exist
                os.chdir(os.path.dirname(os.getcwd()))
                print(Fore.RED + f'Creating repo {repo["path_with_namespace"]}' + Style.RESET_ALL)
                subprocess.run([
                    'gh', 'repo', 'create',
                    f'{ORG_DESTINATION}/{repo["path_with_namespace"]}',
                    '--confirm', '--private',
                    f'--source={repo_path}',
                    '--remote', 'upstream',
                    '--push'
                ], check=True)
                subprocess.run([
                    f'git push upstream --tags "refs/remotes/origin/*:refs/heads/*"'
                ], shell=True, check=True)
        finally:
            os.chdir(os.path.dirname(os.getcwd()))
            subprocess.run(['rm', '-rf', repo_path])

def create_clone_repos_github(github_repos):
   for repo in tqdm(github_repos, desc="Syncing repositories - Github", unit="repos"):
        print('\n' + Fore.GREEN + f'Cloning repo {repo["name"]}\n' + Style.RESET_ALL)
        repo_path = f'../github-src/{repo["name"]}'
        if os.path.exists(repo_path):
            subprocess.run(['rm', '-rf', repo_path])
        repository = c.Repository(
            f"https://api.github.com/repos/{ORG_DESTINATION}/{repo['name']}",
            GITHUB_API_TOKEN
        )
        subprocess.run(['git', 'clone', repo['ssh_url'], repo_path])
        os.chdir(repo_path)
        try:
            print(Fore.GREEN + f'\nUpdating repo {repo["name"]} at dir {os.getcwd()}\n' + Style.RESET_ALL)
            subprocess.run(['git fetch --all'], shell=True, check=True)
            subprocess.run(['git pull --all'], shell=True, check=True)
            print(Fore.BLUE + "Status code: " + str(repository.exists()) + Style.RESET_ALL)
            if repository.exists() == 1:  # repo exists
                print(Fore.YELLOW + f'Updating repo {repo["name"]}' + Style.RESET_ALL)
                subprocess.run([
                    f'git remote add upstream git@github.com:/{ORG_DESTINATION}/{repo["name"]}.git'
                ], shell=True, check=True)
                subprocess.run([
                    f'git push upstream --tags "refs/remotes/origin/*:refs/heads/*"'
                ], shell=True, check=True)
            else:  # repo doesn't exist
                print(Fore.MAGENTA + f'\nCreating repo {repo["name"]}\n' + Style.RESET_ALL)
                subprocess.run([
                    f'git remote add upstream git@github.com:/{ORG_DESTINATION}/{repo["name"]}.git'
                ], shell=True, check=True)

                subprocess.run([
                    'gh', 'repo', 'create',
                    f'{ORG_DESTINATION}/{repo["name"]}',
                    '--confirm', '--private',
                ], check=True)

                subprocess.run([
                    f'git push upstream --tags "refs/remotes/origin/*:refs/heads/*"'
                ], shell=True, check=True)

        except Exception as e:
            print(Fore.RED + f'\nError: {e}\n' + Style.RESET_ALL)
        finally:
            os.chdir(os.path.dirname(os.getcwd()))
            subprocess.run(['rm', '-rf', repo_path])

if __name__ == '__main__':
  writer = c.Writer('utils/data.yaml')
  gitlab_runner = c.Gitlab(GITLAB_API_TOKEN)
  github_digidoc = c.Github(GITHUB_API_TOKEN)

  data_gitlab = read_links()['gitlab_target']['url']
  data_github = read_links()['github_target']['url']

  repos_gitlab = get_gitlab_data(gitlab_runner, data_gitlab)
  repos_github = get_github_data(github_digidoc, data_github)

  writer.write({'gitlab': repos_gitlab, 'github-source': repos_github})

  #create_clone_repos_gitlab(repos_gitlab)
  create_clone_repos_github(repos_github)