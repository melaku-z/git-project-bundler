from time import sleep
from subprocess import Popen, call


def runBashCmd(Bash_Cmd_List: list, cwdDir=None):
    Bash_Cmd = ''
    for aCMD in Bash_Cmd_List:
        Bash_Cmd += aCMD + '|| '

    openedProcess = Popen(
        ['bash', '--login', Bash_Cmd], cwd=cwdDir)
    pollRunningProcess(openedProcess)


def runGitBashCmd(Bash_Cmd_List: list, cwdDir=None):
    Bash_Cmd = ''
    for aCMD in Bash_Cmd_List:
        Bash_Cmd += aCMD + '|| '

    openedProcess = Popen(
        ['bash', '--login', '-i', '-c', Bash_Cmd], cwd=cwdDir)
    pollRunningProcess(openedProcess)


def runPSCmd(PS_Cmd_List: list):
    PS_Cmd = ''
    for aCMD in PS_Cmd_List:
        PS_Cmd += aCMD + '; '

    openedProcess = Popen(
        ['powershell', '-ExecutionPolicy', 'Unrestricted', PS_Cmd], shell=True)
    pollRunningProcess(openedProcess)


def runCmd(PS_Cmd_List: list, cwdDir=None, wayOfExecution='bash', OSName='linux'):
    for aCMD in PS_Cmd_List:
        if aCMD[:3] == 'cd ':
            cwdDir = aCMD[4:-1]
        else:
            if aCMD[:11] == 'powershell ':
                aCMD = ['powershell', '-ExecutionPolicy',
                        'Unrestricted', aCMD[11:]]
            elif aCMD[:6] == 'shell ':
                aCMD = ['sh', '--login', aCMD[6:]]
            elif aCMD[:5] == 'bash ':
                if OSName == 'windows':
                    aCMD = ['bash', '--login', '-i', '-c', aCMD[5:]]
                else:
                    aCMD = ['bash', '--login', aCMD[5:]]
            elif aCMD[:8] == 'gitBash ':
                aCMD = ['bash', '--login', '-i', '-c', 'cd "' +
                        format_path_for_shell(cwdDir, wayOfExecution) + '" && ' + aCMD[8:]]
            openedProcess = Popen(aCMD, shell=True, cwd=cwdDir)
            pollRunningProcess(openedProcess)


def pollRunningProcess(openedProcess):
    for _ in list(range(365)):
        sleep(1)
        output = openedProcess.poll()
        if output is not None:
            openedProcess.kill()
            break
    else:
        openedProcess.kill()
        print('process killed at 65 seconds')


def correctWinPath(win_path: str):
    if win_path[1] == ':':
        win_path = win_path.replace('/', '\\')
    return win_path


def format_path_for_shell(win_path: str, wayOfExecution='bash'):
    if wayOfExecution not in ['bash', 'gitBash']:
        return correctWinPath(win_path)
    
    mountPrefix = {
        'bash': '/mnt',
        'gitBash': '',
    }
    linux_path = win_path.replace('\\', '/').\
        replace('C:', mountPrefix[wayOfExecution] + '/c').\
        replace('c:', mountPrefix[wayOfExecution] + '/c').\
        replace('G:', mountPrefix[wayOfExecution] + '/g').\
        replace('g:', mountPrefix[wayOfExecution] + '/g').\
        replace('D:', mountPrefix[wayOfExecution] + '/d').\
        replace('d:', mountPrefix[wayOfExecution] + '/d')
    return linux_path
