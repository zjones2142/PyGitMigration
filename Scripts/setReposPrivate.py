import json
import time
import requests
import csv

def get_access_tokens(csv_file):
    """Retrieves access tokens from a CSV file.

    Args:
        csv_file (str): Path to the CSV file containing org names and access tokens.

    Returns:
        A dictionary mapping org names to their corresponding access tokens.
    """

    access_tokens = {}
    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            org_name, token = row
            access_tokens[org_name] = token
    return access_tokens

def set_repos_to_private(json_file, access_tokens):
  """Sets imported repositories to private using the GitHub API.

  Args:
      json_file (str): Path to the JSON file containing organization and repo data.
      access_tokens (dict): A dictionary mapping org names to their access tokens.
  """

  with open(json_file, 'r') as f:
      org_repos = json.load(f)

  for org_name, repos in org_repos.items():
      token = access_tokens[org_name]
      headers = {"Authorization": f"token {token}"}

      for repo in repos:
          repo_name = repo['repoName']
          url = f"https://api.github.com/repos/{org_name}/{repo_name}"
          time.sleep(1)
          response = requests.patch(url, headers=headers, json={"visibility": "private"})
          if response.status_code != 200:
              print(f"Error setting {repo_name} to private: {response.text}")

if __name__ == "__main__":
  json_file = 'FILEPATH to repo urls json'
  csv_file = 'FILEPATH to token csv'

  access_tokens = get_access_tokens(csv_file)  # Function from previous response
  set_repos_to_private(json_file, access_tokens)
