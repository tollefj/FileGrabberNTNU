# Downloads assignments from Itslearning (NTNU)
*Requires Chrome to run as a driver with Selenium. Make sure it is installed.*
## Running locally (Python 2.7)
### I cannot guarantee that *only* your submitted files will be downloaded. Some wrongly tagged assignment-related files might be added. Blame the system!
1) Download the project
2) Install packages
```shell
pip install --user selenium
pip install --user BeautifulSoup4
```
3) Run the program
```shell
python grabber.py
```
4) Watch as your downloads folder gets clogged up

Note:
You might need to install lxml (http parser) on Windows.
```shell
python -m pip install lxml
```
