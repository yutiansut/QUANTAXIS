
import shlex
import subprocess

if __name__ == '__main__':
    shell_cmd = 'python "E:\\quantaxis\\EXAMPLE\\test_backtest\\simplebacktest.py"'
    cmd = shlex.split(shell_cmd)
    p = subprocess.Popen(
        cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while p.poll() is None:
        line = p.stdout.readline()
        line = line.strip()
        if line:
            print('Subprogram output: [{}]'.format(line))
    if p.returncode == 0:
        print('Subprogram success')
    else:
        print('Subprogram failed')
