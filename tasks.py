from invoke import task

@task
def build(c):
    """
    Use pyinstaller to build the exe (outputs to 'dist')
    """
    c.run('pyinstaller --clean BlitzLog.spec')

@task
def run(c):
    """
    Run the application as a script on host
    """
    c.run('python -m app.app')

@task
def restore(c):
    """
    Use pip to ensure dependencies are installed
    """
    c.run('pip install -r requirements.txt')

@task
def test(c):
    """
    Run all tests in project
    """
    c.run('pytest')