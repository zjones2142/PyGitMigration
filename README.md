General steps for importing repos from gitlab to github:
(replace urls and names like "REPO" appropriately)

Create a new repository on GitHub. You'll import your external Git repository to this new repository.

On the command line, make a "bare" clone of the external repository using the external clone URL. This creates a full copy of the data, but without a working directory for editing files, and ensures a clean, fresh export of all the old data.
$ git clone --bare https://external-host.com/EXTUSER/REPO.git
# Makes a bare clone of the external repository in a local directory

Push the locally cloned repository to GitHub using the "mirror" option, which ensures that all references, such as branches and tags, are copied to the imported repository.
$ cd REPO.git
$ git push --mirror https://github.com/USER/REPO.git
# Pushes the mirror to the new repository on GitHub.com

Remove the temporary local repository.
cd ..
rm -rf REPO.git


Source:
https://help.github.com/articles/importing-a-git-repository-using-the-command-line/