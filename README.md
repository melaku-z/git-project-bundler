# Git Project Bundler

This project helps to sync a git project between two or more computers/device not connected to the same network.

## Installation

1. Clone this repo
2. Create "local/config.py" file at the root of the project
3. Create configurations for your git projects as stated in the next section

## Configuration

Three configuration items can be saved in the "local/config.py" file.

1. A dictionary item containing details of all projects to sync.

```python
projects_dict = {
    1: {
        'name': 'name of projet', # string
        'active': False, # whether this project is currently active, boolean
        'locations': { # the project's source root directory at the various locations/pcs/devices
            'pc1': {
                'source': 'a full path' # string
            },
            'pc2': {
                'source': 'a full path' # string
            },
            etc ...
        }
    },
    2: {
        etc ...
    }
}
```

2. The default project to sync if no user input is given named: defaultProj

3. A dictionary item containing details of the current location/pc/device

```python
currentLocation = {
        'name': 'pc1',
        'offlineFilesDir': 'a full path' # string, optional path to sync non-git files between devices
        'bundlesDirs': ['a list of full paths'] # string, path to generate git-bundle files to, and pull bundle files from
        'enableMissingFileListGeneration': False,
        'enableMissingFileZipGeneration': False,
        'syncFilesTo': 'pc2',
        'wayOfExecution': 'git-bash',  # Git commands can be executed in 4 ways: direct, bash, powershell, git-bash (for windows)
        'OSName': 'linux',  # linux, windows
    }
```

## Usage

Run the python file "__main__.py" or project directory using Python 3
