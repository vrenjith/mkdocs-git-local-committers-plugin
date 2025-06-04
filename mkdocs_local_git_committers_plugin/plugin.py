import os
import sys
import logging
from pprint import pprint
from timeit import default_timer as timer
from datetime import datetime, timedelta

from mkdocs import utils as mkdocs_utils
from mkdocs.config import config_options, Config
from mkdocs.plugins import BasePlugin

from github import Github

LOG = logging.getLogger("mkdocs.plugins." + __name__)

class LocalGitCommittersPlugin(BasePlugin):

    config_scheme = (
        ('github_baseurl', config_options.Type(str, default='')),
        ('branch', config_options.Type(str, default='main')),
        ('docs_path', config_options.Type(str, default='docs/'))
    )

    def __init__(self):
        self.total_time = 0
        self.branch = 'main'

    def on_config(self, config):
        LOG.info("git-committers plugin ENABLED")
        # Set baseurl centrally for use in other methods
        self.baseurl = self.config.get('github_baseurl') or 'github.com'
        return config

    def get_last_commit(self, path):
        """
        Get the last commit details for a file using local git history.
        Returns a dict with commit info or None if not found.
        """
        import subprocess

        git_cmd = [
            "git", "log", "-1", "--format=%an|%ae|%ad|%s", "--date=iso", "--", path
        ]
        try:
            output = subprocess.check_output(git_cmd, universal_newlines=True).strip()
            if not output:
                return None
            name, email, date, message = output.split("|", 3)
            return {
                "name": name,
                "email": email,
                "date": date,
                "message": message
            }
        except Exception as e:
            LOG.warning(f"Could not get last local commit for {path}: {e}")
            return None

    def get_committers(self, path):
        """
        Get unique committers for a file using local git history.
        """
        import subprocess

        LOG.debug(f"Getting committers for path: {path}")
        seen_committers = set()
        unique_committers = []

        # Use git log to get committers for the file
        git_cmd = [
            "git", "log", "--follow", "--format=%an|%ae", "--", path
        ]
        LOG.debug(f"Running git command: {' '.join(git_cmd)}")
        try:
            output = subprocess.check_output(git_cmd, universal_newlines=True)
            LOG.debug(f"Raw git output:\n{output}")
            for line in output.strip().split("\n"):
                if not line:
                    continue
                try:
                    name, email = line.split("|", 1)
                except ValueError as ve:
                    LOG.warning(f"Could not split line '{line}': {ve}")
                    continue
                key = (name, email)
                if key not in seen_committers:
                    seen_committers.add(key)
                    login = name  # Use name as login for local commits
                    committer_info = {
                        "name": name,
                        "login": login,
                        "url": f"https://{self.baseurl}/{login}",
                        "avatar": f"https://{self.baseurl}/{login}.png",
                        "last_commit": "",
                        "repos": f"https://{self.baseurl}/{login}"
                    }
                    LOG.debug(f"Adding committer: {committer_info}")
                    unique_committers.append(committer_info)
        except subprocess.CalledProcessError as e:
            LOG.warning(f"Git command failed for {path}: {e}")
        except Exception as e:
            LOG.warning(f"Could not get local committers for {path}: {e}")

        LOG.debug(f"Total unique committers found: {len(unique_committers)}")
        return unique_committers

    def on_page_context(self, context, page, config, nav):
        context['committers'] = []
        git_path = self.config['docs_path'] + page.file.src_path
        committers = self.get_committers(git_path)
        if 'contributors' in page.meta:
            users = page.meta['contributors'].split(',')
            for u in users:
                seen = False
                for item in committers:
                    if item['login'] == u:
                        seen = True
                if seen:
                    continue
                committers.append( u )
        if committers:
            context['committers'] = committers

        context['last_commit'] = self.get_last_commit(git_path)
        return context

