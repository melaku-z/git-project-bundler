try:
    from local.config import config
except ImportError:
    print("Warning: Local config not found. Using default configuration.")
    config = {}

default_config = {
    'projects_dict': {
        7: {
            'name': 'bundler',
            'active': False,  # True if project is currently active
            'locations': {
                'pc1': {
                    'source': 'C:/Users/user1/projectBundler',
                },
                'pc2': {
                    'source': 'C:/Users/user/projectBundler',
                },
                'pc3': {
                    'source': '/home/usr/projectBundler',
                },
            }
        },
    },
    'defaultProj': 7,
    'currentLocation': {
        'name': 'pc2',
        'bundlesDirs': ['D:/toCopy'],
        'enableMissingFileListGeneration': False,
        'enableMissingFileZipGeneration': False,
        'syncFilesTo': '',  # a location/computer-name
        'wayOfExecution': 'bash',  # options are: bash, powershell, direct, gitBash
        'OSName': 'windows',  # options are: windows, linux
    },
    'file_name_descripiton_enabled': False,
    'project_zip_generation_enabled': False,
    'defult_days_of_commits_to_bundle': 4,
}

default_config.update(config)
config = default_config
