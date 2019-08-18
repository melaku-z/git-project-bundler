# Git Project Bundler

This project helps to sync a git project between two or more computers/device not connected to the same network.

## Installation

1. Clone this repo
2. Create "local/config.py" file at the root of the project
3. Create configurations for your git projects as stated in the next section

## Configuration

A python dictionary item named 'config' containing five configuration items can be saved in the "local/config.py" file.

```python
config = {
    'projects_dict': { # A dictionary item containing details of all projects to sync.
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
    },
    'defaultProj': 1 # The default project to sync if no user input is given named
    'currentLocation': { # A dictionary item containing details of the current location/pc/device
        'name': 'pc1',
        'offlineFilesDir': 'a full path' # string, optional path to sync non-git files between devices
        'bundlesDirs': ['a list of full paths'] # string, path to generate git-bundle files to, and pull bundle files from
        'enableMissingFileListGeneration': False,
        'enableMissingFileZipGeneration': False,
        'syncFilesTo': 'pc2',
        'wayOfExecution': 'gitBash',  # Git commands can be executed in 4 ways: direct, bash, powershell, gitBash (for windows)
        'OSName': 'linux',  # linux, windows
    },
    'file_name_descripiton_enabled': False,
    'project_zip_generation_enabled': False,
    'defult_days_of_commits_to_bundle': 4,
}

```

## Usage

Run the python file "__main__.py" or project directory using Python 3
