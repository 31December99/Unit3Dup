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
        self.branch_name = "0.x.x"
        self.repo_exist = os.path.exists(self.repo_local_path)

    def process(self) -> bool:
        if not self.repo_exist:
            console.log(
                f"Cloning repository from {self.repo_url} to {self.repo_local_path}",
                style="bold blue",
            )
            self._clone()
            return True
        else:
            self._update()

    def _update(self):
        # Validate git repo
        try:
            repo = git.Repo(self.repo_local_path)
        except git.exc.InvalidGitRepositoryError:
            console.log(
                f"{self.repo_local_path} is not a valid Git repository.",
                style="red bold",
            )
            self._clone()
            return

        # Checkout new branche
        repo.git.checkout(self.branch_name)

        if repo.is_dirty(untracked_files=True):
            repo.git.stash("save", "--include-untracked")

        origin = repo.remotes.origin
        origin.pull(self.branch_name)
        console.log(
            f"Repository updated successfully to branch '{self.branch_name}'",
            style="bold blue",
        )
        console.rule("", style="violet bold")

        # Stash
        if repo.git.stash("list"):
            repo.git.stash("pop")

    def _clone(self):
        current_dir = os.getcwd()
        new_folder_path = os.path.join(current_dir, "Unit3d-up_0.x.x")

        if os.path.exists(new_folder_path):
            console.log(
                f"Folder {new_folder_path} already exists. Please remove it manually and retry",
                style="red bold",
            )
            exit(1)

        repo = git.Repo.clone_from(
            self.repo_url, new_folder_path, branch=self.branch_name
        )
        console.log(
            f"Cloned repository from {self.repo_url} to {new_folder_path} on branch {self.branch_name}",
            style="bold blue",
        )


if __name__ == "__main__":
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

    console.rule("- Autoupdate for Unit3D-up_0.x.x -", style="violet bold")
    my_git = MyGit(repo_local_path=os.getcwd())
    my_git.process()
