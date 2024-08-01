import json
import os
import csv
import time
from subprocess import run

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

def import_local_repos(json_file, parent_dir, access_tokens):
  """Imports local clones into target repositories using data from a JSON file.

  Args:
      json_file (str): Path to the JSON file containing organization and repo data.
      parent_dir (str): Path to the parent directory containing organization directories.
  """

  with open(json_file, 'r') as f:
      org_repos = json.load(f)

  for org_name, repos in org_repos.items():
      org_dir = os.path.join(parent_dir, org_name)
      if not os.path.isdir(org_dir):
          print(f"Organization directory '{org_dir}' not found. Skipping...")
          continue
      
      token = access_tokens[org_name]

      for repo in repos:
          repo_name = repo['repoName']
          url = repo['url'].replace("//", f"//{token}@").replace(" ", "") #adding auth headers to url
          repo_path = os.path.join(org_dir, repo_name)

          if os.path.isdir(repo_path) and os.path.exists(os.path.join(repo_path, '.git')):
              print(f"Importing {repo_name} from {org_name} to {url}")

              # Change directory to the repo directory
              os.chdir(repo_path)

              # Push using mirror command
              run(["git", "push", "--mirror", url])

              # Change directory back to the organization directory
              os.chdir(org_dir)

              # Remove the local clone
              #run(["rm", "-rf", repo_name+".git"])

          else:
              print(f"Repo '{repo_name}' not found in {org_dir}. Skipping...")

if __name__ == "__main__":
  json_file = 'FILEPATH to json'
  parent_dir = 'FILEPATH of repo parent directory'
  csv_file = 'FILEPATH to token csv'
  access_tokens = get_access_tokens(csv_file)

  import_local_repos(json_file, parent_dir, access_tokens)
