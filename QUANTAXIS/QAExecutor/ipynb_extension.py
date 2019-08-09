from QUANTAXIS.QAExecutor.QAExecutor import QA_Executor


def load_ipython_extension(ipython):
    # The `ipython` argument is the currently active `InteractiveShell`
    # instance, which can be used in any way. This allows you to register
    # new magics or aliases, for example.
    print('# active quantaxis_autogen')
    ipython.register_magic_function(run_ipython_cell, 'line_cell', 'qarun')
    ipython.register_magic_function(
        run_ipython_cell_test, 'line_cell', 'qatest')
    ipython.register_magic_function(run_pms, 'line_cell', 'qarun')


def run_ipython_cell(line, cell=None):
    args = line.split()
    print(args)
    args.extend(["--source_code", cell if cell is not None else ""])
    try:
        run(args)
    except SystemExit as e:
        pass
