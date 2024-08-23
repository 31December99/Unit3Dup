# -*- coding: utf-8 -*-
import subprocess
import os
import sys


def install_git(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


class MyGit:
    """
    Install gitPython and update the repository
    """

    def __init__(self, repo_local_path: str):
        self.repo_local_path = repo_local_path
        self.repo_url = "https://github.com/31December99/Unit3Dup.git"
        self.repo_exist = os.path.exists(self.repo_local_path)

    def process(self) -> bool:
        if not self.repo_exist:
            console.log(
                f"Cloning repository from {self.repo_url} to {self.repo_local_path}",
                style="bold blue",
            )
            git.Repo.clone_from(self.repo_url, self.repo_local_path)
            return True
        else:
            self._update()

    def _update(self):
        # Check if the path is a valid Git repository
        try:
            repo = git.Repo(self.repo_local_path)
        except git.exc.InvalidGitRepositoryError:
            console.log(
                f"{self.repo_local_path} is not a valid Git repository.",
                style="red bold",
            )
            # this folder has no git metadata, so we are going to clone into a new folder
            self._clone()
            return

        if repo.is_dirty(untracked_files=True):
            repo.git.stash("save", "--include-untracked")

        # Update the repository
        origin = repo.remotes.origin
        origin.pull()
        console.log(
            f"Repository updated successfully to '{repo.tags[-1]}'", style="bold blue"
        )
        console.rule("", style="violet bold")

        # Reapply stashed local changes, if any
        if repo.git.stash("list"):
            repo.git.stash("pop")

    def _clone(self):
        # Define a new position
        current_dir = os.getcwd()
        new_folder_path = os.path.join(current_dir, "Unit3d-up")

        # Verify the folder
        if os.path.exists(new_folder_path):
            console.log(
                f"Folder {new_folder_path} already exists. Please remove it manually and retry",
                style="red bold",
            )
            exit(1)

        # Cloning..
        git.Repo.clone_from(self.repo_url, new_folder_path)
        console.log(
            f"Cloned repository from {self.repo_url} to {new_folder_path}",
            style="bold blue",
        )


if __name__ == "__main__":
    # Test Imports
    try:
        import git
        import rich
    except ImportError:
        print("Installation in progress...")
        install_git("gitpython")
        install_git("rich")

    import git
    from rich.console import Console

    console = Console(log_path=False)

    console.rule("- Autoupdate for Unit3D-up -", style="violet bold")
    my_git = MyGit(repo_local_path=os.getcwd())
    my_git.process()
