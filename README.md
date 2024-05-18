# REQUIREMENTS

OS: Linux<br>
Memory: >= 4GB RAM<br>
Hard disk free space: >= 1 MB<br>
Python version: >= 3.10


# OVERVIEW OF INSTALLATION PACKAGE

This package contains directory *src* with python files, which implement application logic; *requirements.txt*, which contains information about third-party python packages, which are used by this application, *install.py* for importing those modules; *library.py* for running the application.


# INSTALLATION

If you have git installed: run in your terminal:
```cmd
git clone https://github.com/fff2dot0/library.git
cd library
python3 install.py
```

If not, download zip file from [repository](https://github.com/fff2dot0/library.git), unzip it and in that directory, run:
```cmd
cd library-main
python3 install.py
```

*Note: the author recommends creating a virtual environment, and installing it there. For details, see [documentation](https://docs.python.org/3/library/venv.html).*


# USAGE

*Note: before using this app, you have to have an account. You can get it from an administrator of the library. After that, put your login and password into the file ".env" in the directory "src". Now, you are ready to start.*

To start an application run this command in the application's directory:
```cmd
python3 library.py
```
