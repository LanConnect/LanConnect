from fabric.api import *



def deploy():
    test()
    package()
    upload()

@run_once
def clean():
    local("find . -iname '*.pyc' -delete")
    local("find . -iname '*.pyo' -delete")
    #This is to help out our disabled friends, like roy
    local("find . -iname '*.html' -exec dos2unix -o {}")
    local("find . -iname '*.py' -exec dos2unix -o {}")

@run_once
def test():
    #UPDATE THIS TO USE NOSE-PROGRESSIVE
    with cd('TestLan'), prefix('source bin/activate' if platform.system!='Windows' else 'Scripts\\activate.bat'):
        local('python manage.py test')

@run_once
def package():
    pass

def upload():
    pass