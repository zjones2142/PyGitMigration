import json
import os
import shutil

"""removes a number of local git repo clones from the machine.
CAUTION: Only run if you are sure you want to delete and remove the repos referenced by the input file.
Note: may not work if the directory of execution does not have correct permissions. Make sure and run with admin"""

def remove_local_clones(json_file, parent_dir):
  """Removes local clones based on data from a JSON file.

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

      for repo in repos:
          repo_name = repo['repoName']
          repo_path = os.path.join(org_dir, repo_name)
          if os.path.isdir(repo_path):
              shutil.rmtree(repo_path)
              print(f"Removed {repo_path}")
          else:
              print(f"Repo '{repo_name}' not found in {org_dir}. Skipping...")

if __name__ == "__main__":
  json_file = 'FILEPATH to repo urls json'
  parent_dir = 'FILEPATH to repo parent directory'
  remove_local_clones(json_file, parent_dir)
