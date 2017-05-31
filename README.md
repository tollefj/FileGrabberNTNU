# Download data from Itslearning (NTNU)
*Requires Chrome.*
## Running locally (Python 2.7)
[Download python here](https://www.python.org/downloads/release/python-2713/) if missing.

TLDR: download & extract > python gui.py > select an empty folder > load courses > download
1) Download the project
2) Install packages
```shell
pip install -r requirements.txt
```
3) Run the program
```shell
python gui.py
```
4) Enter Feide login information
![Login screen](http://i.imgur.com/qV2Xtwt.png)

5) Select a directory to store your files
## Select an empty folder, or this will mess up already saved files in the directory.
![Directory](http://i.imgur.com/sNRov6E.png)

## WARNING: Selecting Lecture notes will download a tremendous amount of files, although it has been strictly limited to folders with certain keywords. This may cause broken files.
6) Select courses to ignore (i.e not download files for)
![Courses](http://i.imgur.com/7pFR7ar.png)

7) Download  
The final outcome will look something like this.
![Final](http://i.imgur.com/qVvTOMA.png)

Note:
You might need to install lxml (http parser) on Windows.
```shell
python -m pip install lxml
```
