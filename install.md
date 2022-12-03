# Donaldson ASU Twitter Analysis Tool

## Installation Guide

<div style="page-break-after: always"></div>

## Introduction

Donaldson Company makes filters (air, gasoline, chemical, etc). They see the possibility of the market shifting away from fossil fuels, and would like to see if any predictions can be made about the direction companies are headed in using social media information.

They wished for data from major companies to be scraped from Twitter, and analyzed for 'tone of voice' with what we later learned was VADER Sentiment Analysis, and marked if it was relating to one of four alternative power-trains: Hydrogen fuel cells, hydrogen combustion engines, natural gas engines, and electric batteries.

We elected to work with them scraping data from Twitter. This is the tool we developed to perform this task. It integrates Tweepy, MySQL's Python connector, a MySQL database, and vaderSentiment, the VADER analysis tool (by Hutto, C.J. & Gilbert, E.E.) via our own code.

## Installation Preparation

For this installation, you will need:

Python3 installed, which you can install from <https://www.python.org/downloads/>. Make sure when installing, you have Python added to your PATH directory.

A working MySQL server that you have full permissions to operate within. You can find out more information on how to install a local MySQL database from <https://dev.mysql.com/doc/mysql-getting-started/en/>

A Twitter developer account, as well as a Bearer Token for an App, as allocated by them. Currently, you can sign up for an account at <https://developer.twitter.com/en/portal/dashboard>.

__It is recommended that you set up a virtual development environment when installing or using our software.__

(It may be easiest to set up the virtual environment in or near the same directory where you unzip our software. Please read all the instructions before performing the installation.)

For more information on virtual Python environments, please see <https://docs.python.org/3/tutorial/venv.html>

If you would like to set up a Python virtual environment, you can do so by typing `python -m venv env` (`env` will be the name of a directory created in the location you run this command. It stores some information about the virtual environment as well as scripts to activate/deactivate the environment.)

If you would like to be using the Python virtual environment you set up, type `.\env\Scripts\activate`, or the appropriate script of choice for the OS/Terminal you are using. (`activate.ps1` for PowerShell, for example). __Typically, you will know this has succeeded when (env) appears to the left of your command prompt.__

## Installation Instructions

Navigate to:

<https://github.com/agarcia169/4306-Donaldson-Project>

Click the "Code" button, and click "Download ZIP".

Extract this ZIP to the directory you wish the code to be installed at. It should extract as a single directory named `4306-Donaldson-Project-main`. (You can rename this directory to whatever you want.)

Type `python -m pip install -e .\4306-Donaldson-Project-main\` to install our package. This method of installation uses the `-e` flag, which installs the package in editable mode. This mode keeps the package in the directory you unzipped it to, which allows you to edit the code within that directory to control the operation of the software.

This should install our software, and all necessary Python dependencies.

Use the `databaseSetup.sql` file to create all the relevant tables needed within a database of your choosing on the MySQL server you set up.

You will now need to create a config.cfg file in the proper directory. In the same directory you unzipped `4306-Donaldson-Project-main` to, navigate to a sibling directory named `config` and create two files, `api_keys.cfg` and `server.cfg`.

The `api_keys.cfg` should contain the following:

```text
[twitter]
bearer_token=
```

With your Twitter developer Bearer Token pasted to the right of that `=`.

`server.cfg` should contain the following:

```text
[mysql]
username=
password=
host=
database=
port=
```

Include the username and password to your local MySQL database, the host and port address, and the name of the database you created for this software to use.
