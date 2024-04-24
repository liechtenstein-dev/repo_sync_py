import yaml
import requests

class Repository:
  def __init__(self, url:str, token:str):
    self.url = url
    self.token = token

  def exists(self):
    headers = {
      'Authorization': f'Bearer {self.token}',
      'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(self.url, headers=headers)
    if response.status_code == 200:
      returncode = 1
    else:
      returncode = 0
    return returncode

class Github:
  def __init__(self, token: str):
    self.token = token

  def get(self, url: str):
    headers = {
      'Authorization': f'Bearer {self.token}'
    }
    response = requests.get(url, headers=headers)
    return response

class Reader:
  def __init__(self, path: str):
    self.path = path

  def read(self):
    with open(self.path, 'r') as file:
      return yaml.load(file, Loader=yaml.FullLoader)

class Writer:
  # example of path: 'data.yaml'
  def __init__(self, path: str):
    self.path = path

  # Write data to file
  # example of data: {'key': 'value'}
  def write(self, data: dict):
    with open(self.path, 'w') as file:
      yaml.dump(data, file)

class Gitlab:
  def __init__(self, token: str):
    self.token = token

  def get(self, url: str):
    headers = {
      'Authorization': f'Bearer {self.token}'
    }
    response = requests.get(url, headers=headers)
    return response

