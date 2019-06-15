try:
    from local.config import currentLocation, projects_dict, defaultProj
except ImportError:
    print("Local config not found. Using default configuration.")
    projects_dict = {
        7: {
            'name': 'bundler',
            'active': True,
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
    }

    defaultProj = 7

    locationsDict = {
        'pc2': {
            'name': 'pc2',
            'bundlesDirs': ['D:/toCopy'],
            'enableMissingFileListGeneration': False,
            'enableMissingFileZipGeneration': True,
            'syncFilesTo': 'pc3',
            'wayOfExecution': 'bash',  # options are: bash, powershell, direct, git-bash
            'OSName': 'windows',  # options are: windows, linux
        },
        'pc3': {
            'name': 'pc3',
            'bundlesDirs': ['/home/usr/toCopy'],
            'enableMissingFileListGeneration': False,
            'enableMissingFileZipGeneration': True,
            'syncFilesTo': 'pc2',
            'wayOfExecution': 'git-bash',
            'OSName': 'linux',
        },
    }

    currentLocation = locationsDict['pc2']
