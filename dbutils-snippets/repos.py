from typing import Optional, List
import sys


def add_repos_paths(paths_in_repos: Optional[List[str]]=None):
  """Automatically add Repos to sys.path for use with files in repos. 
  
  :param paths_in_repos: optional list of subdirectories inside the repository (relative paths!)
  """
  np = dbutils.notebook.entry_point.getDbutils().notebook().getContext().extraContext().get("notebook_path")
  if np is None:
      return
  np = np.get()
  splits = np.split('/')
  if splits[1] == 'Repos':
    repo_root = '/Workspace' + '/'.join(splits[:4])
    if repo_root not in sys.path:
      sys.path(repo_root)
      
    if paths_in_repos:
      for p in paths_in_repos:
        tp = repo_root + '/' + p
        if tp not in sys.path:
          sys.path.append(tp)

