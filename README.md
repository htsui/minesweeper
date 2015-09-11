Minesweeper

* Multiplayer
* Seperate Rooms
* First click will never be bomb

[Video demo (sorry, screen capture didn't capture the cursor)](http://streamable.com/mlsu)

[Live Demo](http://intense-gorge-2755.herokuapp.com)


---
###Setup
```
git clone
pyvenv env
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | env/bin/python
env/bin/easy_install "pyramid==1.6a2"
env/bin/python setup.py develop
env/bin/pserve development.ini
```