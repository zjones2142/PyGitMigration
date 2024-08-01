# IN PROGRESS
This is a Collection of Python scripts used to gather information from Git APIs (GitLab and GitHub) and then migrate code to GitHub.

##Steps For Execution
1. Replace all placeholders in code with corrected filepaths and filenames
2. Create new organizations under a single user for every group in gitlab, and generate an access key fo
3. Run the information gathering scripts:
   - repoRetrieval.py:
     go through steps to generate a json that stores urls for EVERY repo to be migrated that are stored under top level groups. Make sure access token has admin level perms, and check that url to gitlab is correct.
   - createRepos.py:
     
