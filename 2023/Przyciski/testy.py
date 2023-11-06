import sys, re, configparser, pathlib, os, subprocess, psutil, time
from colorama import Fore, Back, Style
import glob

def log(message, type = 'log'):
    match type:
        case 'info':
            title = 'Info'
            back = Back.WHITE
            fore = Fore.WHITE
        case 'warn':
            title = 'Warn'
            back = Back.YELLOW
            fore = Fore.YELLOW
        case 'error':
            title = 'Err '
            back = Back.RED
            fore = Fore.RED
        case 'ok':
            title = ' Ok '
            back = Back.GREEN
            fore = Fore.GREEN
        case 'header':
            title = f'        {message}        '
            message = ''
            back = Back.WHITE
            fore = Fore.WHITE
        case 'fail':
            title = 'Fail'
            back = Back.RED + Style.DIM
            fore = Fore.RED + Style.DIM
        case _:
            title = '    '
            back = Back.LIGHTBLACK_EX
            fore = Fore.LIGHTBLACK_EX

    print(f'{back} {title} {Back.RESET}', end='')
    print(Back.RESET + fore + " " + message, end='')
    print(Style.RESET_ALL)

stats = {
    'ok': 0,
    'fail': 0,
    'error': 0
}
def doTest(testname):
    dir = pathlib.Path(__file__).parent.resolve()
    paths = {
        "in": f"{dir}/testy/in/{testname}.in",
        "out": f"{dir}/testy/out/{testname}.out",
    }
    files = {}
    def readTextFile(path):
        with open(path, 'r') as file:
            return file.read()
        
    for type in paths.keys():
        path = paths[type]
        abs = pathlib.Path(path).absolute()
        if(not os.path.exists(abs)):
            print(f"File {path} not found")
            exit(2)
        files[type] = readTextFile(abs)

    # Import solution
    solution = pathlib.Path(f"{dir}/prz.py").absolute()
    if(not os.path.exists(solution)):
        print(f"Solution file {solution} not found")
        exit(2)

    # Create start command
    command = "py [FILE]".replace('[FILE]', f'"{solution}"')

    # Run solution
    startTime = time.time()
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    process.stdin.write(files['in'])


    # Get memory usage
    pid = process.pid
    subprocess_process = psutil.Process(pid)
    memory_used = subprocess_process.memory_info().rss
    process.stdin.close() 
    while(process.poll() is None):
        try:
            memory_used = subprocess_process.memory_info().rss
            time.sleep(0.02)
        except:
            break;
    memory_used = str(round(memory_used / 1024 / 1024)) + "MB"

    # Get output
    stdout, stderr = process.communicate()
    stdout = stdout.rstrip() 
    duration = round(time.time() - startTime, 2)
    duration = str(duration) + "s"
    # Verify output
    report = {}
    memory = Fore.LIGHTBLACK_EX + f"  (Mem: {memory_used}, Time: {duration})" + Fore.RESET
    indent = Back.LIGHTBLACK_EX + " " + Back.RESET + "  "

    if(stderr != ''):
        report['status'] = 'error'
        error = stderr.split('\n')
        for no, line in enumerate(error):
            error[no] = indent + Fore.RED + line
        error.pop()
        error = '\n'.join(error)
        report['message'] = f'Test {testname} errored: {memory}\n' + Fore.RESET + error + "\n"
    elif stdout == files['out'].rstrip():
        report['status'] = 'ok'
        report['message'] = f'Test {testname} passed\n'
    else:
        report['status'] = 'fail'
        received = Fore.WHITE + stdout + Fore.RED
        expected = Fore.WHITE + files["out"] + Fore.RED
        report['message'] = f'Test {testname} failed {memory}{Fore.RED} \n{indent}Received: {received}\n{indent}Expected: {expected}'

    stats[report['status']] += 1
    log(report['message'], report['status'])

log(f"Running tests:\n", 'info')

for i in range(1,1000001):
    doTest("prz%i"%i)

log(f"Tests finished:\n{Fore.GREEN + str(stats['ok'])} passed{Fore.RESET},{Fore.RED} {str(stats['fail'])} failed{Fore.RESET} and {Fore.RED}{stats['error']} errored", 'info')