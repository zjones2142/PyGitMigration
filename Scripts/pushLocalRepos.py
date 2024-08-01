import json
import os
import csv
import subprocess

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

def import_local_repos(json_file, parent_dir, access_tokens, log_file='repo_import.log'):
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
            try:
                result = subprocess.run(["git", "push", "--mirror", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                output = result.stdout.decode()
                errors = result.stderr.decode()
            except subprocess.CalledProcessError as e:
                output = ""
                errors = e.stderr.decode()

            # Write captured output and errors to log file
            log_file.write(f"\n** {repo_name} Push Output:**\n{output}\n")
            log_file.write(f"\n** {repo_name} Push Errors:**\n{errors}\n")

            # Change directory back to the organization directory
            os.chdir(org_dir)

        else:
            print(f"Repo '{repo_name}' not found in {org_dir}. Skipping...")

if __name__ == "__main__":
  json_file = 'FILEPATH to json'
  parent_dir = 'FILEPATH of repo parent directory'
  csv_file = 'FILEPATH to token csv'
  access_tokens = get_access_tokens(csv_file)
  log_file = 'repo_import.log'
  import_local_repos(json_file, parent_dir, access_tokens, log_file)
