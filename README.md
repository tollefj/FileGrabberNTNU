# Downloads assignments from Itslearning (NTNU)
*Requires Chrome to run as a driver with Selenium. Make sure it is installed.*
## Running locally (Python 2.7)
### I cannot guarantee that *only* your submitted files will be downloaded. Some wrongly tagged assignment-related files might be added. Blame the system!
1) Run the following to test for installed packages.
```shell
python setup.py --no-user-cfg install --prefix='/usr/local' --no-compile
```
2) Input your feide user and password in the Tkinter dialog
![](https://raw.githubusercontent.com/ph10m/FileGrabberNTNU/master/images/input.png)
3) Watch your default downloads folder gets clogged up

You might need to install lxml (http parser) on Windows.
```shell
pip install lxml
```
