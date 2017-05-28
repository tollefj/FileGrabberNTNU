# Downloads assignments from Itslearning (NTNU)
*Requires Chrome to run as a driver with Selenium. Make sure it is installed.*
## Running locally (Python 2.7)
### I cannot guarantee that *only* your submitted files will be downloaded. Some wrongly tagged assignment-related files might be added. Blame the system!
1) Download required modules, too lazy to write a few lines to bundle it.
```shell
pip install BeautifulSoup4
pip install Selenium
```
2) That should be it. Run the program.
```shell
python read_courses.py
```
3) Watch your default downloads folder get clogged up.

You might need to install lxml (http parser) on Windows.
```shell
pip install lxml
```
