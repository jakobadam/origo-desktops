# https://msdn.microsoft.com/en-us/library/windows/desktop/bb892057(v=vs.85).aspx

def graceperioddays():
    script = open('{}/scripts/graceperioddays.ps1'.format(HERE))
    return run_script(script, host, args=[name], **kwargs)

def licensingtype():
    script = open('{}/scripts/licensingtype.ps1'.format(HERE))
    return run_script(script, host, args=[name], **kwargs)
