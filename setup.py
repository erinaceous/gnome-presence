from setuptools import setup


setup(
    name='gnome-presence',
    version='0.1',
    description='Run scripts when your desktop session becomes idle / active',
    author='Owain Jones',
    author_email='contact@odj.me',
    scripts=['gnome-presence'],
    data_files=[('/usr/share/applications/', ['gnome-presence.desktop'])]
)