from setuptools import setup
setup(
    name='FileGrabberNTNU',
    version='0.1',
    setup_requires=['beautifulsoup4','selenium'],
)
from read_courses import main
main()
