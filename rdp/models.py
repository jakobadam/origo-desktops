import winexe

class Package(object):

    @staticmethod
    def deploy(filename):

        cmd = '"//ubuntu/share/%s" -ms' % filename

        return winexe.cmd(
            user='vagrant',
            password='vagrant',
            host='192.168.123.191',
            cmd=cmd)
