from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'gui'

executables = [
    Executable('app.py', base=base, target_name = 'BlitzLog')
]

setup(name='BlitzLog',
      version = '1.0',
      description = 'Helldivers 2 mission logger for people who wanna sweat a casual speedrun competition.',
      options = {'build_exe': build_options},
      executables = executables)
