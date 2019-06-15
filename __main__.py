import datetime
import os
import shutil
import glob
from config import currentLocation, projects_dict, defaultProj
from commandRunners import runPSCmd, runBashCmd, runCmd, runGitBashCmd, win_to_linux_path, correctWinPath
from syncFolders import saveFileList, ZipFileList, getMissingFileList


class project:
    def __init__(self, project_dict: dict):
        self.name = project_dict['name']
        self.source = project_dict['locations'][currentLocation['name']]['source']
        self.bundleInDirs = currentLocation['bundlesDirs']
        self.bundleOutDir = currentLocation['bundlesDirs'][0] + '/bundlesOut/'
        self.comment = ''
        self.bundleFileNamePrefix = project_dict['name'][:3].lower()
        self.bundleFileFullPath = ''

        for aDir in [self.source, self.bundleInDirs[0], self.bundleOutDir]:
            if not os.path.exists(aDir):
                print('Project: {0}, path {1} not found.'.format(
                    self.name, aDir))

    def createZipOrBundle(self):
        self.comment = input('Enter zip description: ')
        isOnlyGitBundle = (
            input('Run only git Bundle, No full project zip? (n/y): ') != 'n')
        nowDatetimeText = datetime.datetime.now().strftime("%B %d, %Y %H-%M-%S ")
        self.bundleFileFullPath = self.bundleOutDir + '/' + \
            self.bundleFileNamePrefix + ' ' + nowDatetimeText + ' ' + self.comment
        try:
            if isOnlyGitBundle:
                self.gitBundleCreate()
            else:
                print('Making archive. Please Wait . . .')
                shutil.make_archive(
                    self.bundleFileFullPath, 'zip', self.source)
            print('successfuly created bundle/zip.')
            if 'startFileAfterBundleCreation' in currentLocation:
                os.startfile(currentLocation['startFileAfterBundleCreation'])
        except BaseException as anError:
            print('errors: ' + str(anError))

    def gitBundleCreate(self):
        defultDaysToBundle = 4
        daysToBundle = input(
            'Number of Days of Commits to Bundle (defaults to {0}): '.format(defultDaysToBundle))
        if daysToBundle == '':
            daysToBundle = 1
        daysToBundle = max([defultDaysToBundle, int(daysToBundle)])
        gitBundleCmd = [
            'cd "' + self.source + '"',
            'git status branch',
            'git bundle create "' + self.bundleFileFullPath +
            '.bundle" --since=' + str(daysToBundle) + '.days --all'
        ]
        print('Creating git bundle. Please Wait . . .')
        runCmd(
            gitBundleCmd, wayOfExecution=currentLocation['wayOfExecution'], OSName=currentLocation['OSName'])

    def archiveBundle(self, fileNameBundle):
        for destFolder in self.bundleInDirs:
            if destFolder in fileNameBundle:
                fileNameBundleArchived = fileNameBundle.replace(
                    destFolder, self.bundleInDirs[0] + '/old')
                shutil.move(fileNameBundle, fileNameBundleArchived)
                break

    def getGitBundleCmd(self, fileNameBundle):
        thisProjectDir = os.path.dirname(os.path.abspath(__file__))

        commands = {
            'addOriginBundle': [
                'cd "{0}"'.format(self.source),
                '{1} git remote set-url originBundle "{0}" || git remote add originBundle "{0}"'.format(
                    correctWinPath(fileNameBundle), currentLocation['wayOfExecution']),
            ],
            'pullAll': [
                'git pull originBundle',
            ],
            'gitPullAllBranchesCmd': {
                'powershell': [r"powershell for /F %remote in ('git branch -r') do ( git branch --set-upstream-to %remote)"],
                'bash': ['{0} "{1}/gitPullAllBranchesFromOriginBundle.bash"'.format(currentLocation['wayOfExecution'], win_to_linux_path(thisProjectDir, currentLocation['wayOfExecution']))],
            },
        }

        commands['gitPullAllBranchesCmd']['gitBash'] = commands['gitPullAllBranchesCmd']['bash']

        gitBundleCmd = commands['addOriginBundle'] + \
            commands['gitPullAllBranchesCmd'][currentLocation['wayOfExecution']
                                              ] + commands['pullAll']
        return gitBundleCmd

    def gitBundlePull(self):
        fileNamesBundle = []
        for destFolder in self.bundleInDirs:
            fileNamesBundle += glob.glob('{0}/{1}*.bundle'.format(destFolder, self.bundleFileNamePrefix))

        for fileNameBundle in fileNamesBundle:
            runCmd(
                self.getGitBundleCmd(fileNameBundle), wayOfExecution=currentLocation['wayOfExecution'], OSName=currentLocation['OSName'])

            self.archiveBundle(fileNameBundle)


def ZipOrBundleProjectFromUser(activeProjects: dict):

    projectQueryStr = 'Enter '
    for index in activeProjects.keys():
        projectQueryStr += '{0} for {1}, '.format(str(index), projects_dict[index]['name'])
    projectQueryStr += '(defaults to {0}): '.format(defaultProj)

    projectType = input(projectQueryStr)
    try:
        projectType = int(projectType)
        if projectType not in projects_dict:
            projectType = defaultProj
    except (TypeError, ValueError):
        projectType = defaultProj

    aProject = project(projects_dict[projectType])
    aProject.createZipOrBundle()


def pullAllProjectBundles(activeProjects: dict):
    print("bundle pull started")
    for aProjectItem in activeProjects.values():
        aProject = project(aProjectItem)
        aProject.gitBundlePull()
    print("bundle pull ended")


def syncFilesInFolder():
    if (currentLocation['enableMissingFileZipGeneration'] or currentLocation['enableMissingFileListGeneration']):
        if input('Start File Sync?(y/n)') == 'y':
            if currentLocation['enableMissingFileZipGeneration']:
                ZipFileList(getMissingFileList()['FilesMissingInList'])
            if currentLocation['enableMissingFileListGeneration']:
                saveFileList()


def filterActiveProjects():
    activeProjects = {}
    for aProjectItemKey, aProjectItemValue in projects_dict.items():
        if aProjectItemValue['active'] and currentLocation['name'] in aProjectItemValue['locations'].keys():
            activeProjects[aProjectItemKey] = aProjectItemValue
    return activeProjects


if __name__ == "__main__":

    activeProjects = filterActiveProjects()
    pullAllProjectBundles(activeProjects)
    syncFilesInFolder()

    while (input('Do you want to continue with the operation? (n/y)') != 'n'):
        try:
            ZipOrBundleProjectFromUser(activeProjects)
        except Exception as ex:
            print(ex)
            input("press enter to continue.")
        try:
            if currentLocation['OSName'] == 'windows':
                os.startfile(currentLocation['bundlesDirs'][0] + '/bundlesOut/')
        except Exception as err:
            print('coudn\'t display bundlesDir folder: ' + str(err))