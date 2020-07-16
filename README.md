# K_project

### Goal of the project

Realization of a realtime instruction system for injured patients to do habilitation tasks.



### Requirements

- QT

- PYQT5

- OpenCV

  

### Installation

If you are using [Anaconda](https://www.anaconda.com/) for installing packages:

1. Download [Anaconda](https://www.anaconda.com/download/)

2. Install following packages (pygame and opencv), since they are not automatically installed by Anaconda:

```shell
$ conda install -c cogsci pygame
$ conda install -c menpo opencv
```

---

If you are using pip for installing packages:

Several dependent packages (not all) are documented in ```req.txt```, so to help you install those packages:

```shell
$ pip install -r req.txt
```

---

The data & video are provided elsewhere


### [Syncing with upstream](https://help.github.com/articles/syncing-a-fork/)

```shell
$ git fetch upstream
$ git merge upstream/master
```

