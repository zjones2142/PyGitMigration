import json
import git

#this file uses the git-python module to clone repositories from a list of urls stored in JSON format

access_token = ""  # Replace with your personal access token
username = "zach"

def clone_repos(orgName):
    """Clones a list of repositories from a JSON file using HTTP Basic Auth.

    Args:
        repos_file (str): Path to the JSON file containing repository information.
        access_token (str): Personal access token for authentication.

    Raises:
        FileNotFoundError: If the JSON file is not found.
        JSONDecodeError: If the JSON file is invalid.
        requests.exceptions.RequestException: If an HTTP request error occurs.
        subprocess.CalledProcessError: If a git clone command fails.
    """
    repos_file = "FILEPATH of repos json"+f"{orgName}-projects.json"
    try:
        with open(repos_file, 'r', encoding='utf-8') as f:
            repos_data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: JSON file '{repos_file}' not found.")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error: Invalid JSON format in '{repos_file}': {e}")

    for repo in repos_data:
        repoURLFix = repo['url'].replace("http://", "@") #adding auth headers to url
        url = f"http://{username}:{access_token}{repoURLFix}"

        try:
            # Use the GitPython library for cloning
            git.Repo.clone_from(url, f"FILEPATH to repo parent folder\\{orgName}\\{repo['name']}")
            print(f"Cloned repository: {repo['name']}")
        except git.GitCommandError as e:
            print(f"Error cloning {repo['name']}: {e}")

if __name__ == "__main__":
    orgNames = '' #seperate with commas
    orgList = orgNames.split(',')
    for org in orgList:
        clone_repos(org)