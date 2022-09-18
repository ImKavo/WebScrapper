# WebScrapper
This program can parse an HTML-code from real estate site and save it to database

# Technologies:
        - Python
        - MySQL
        - requests, BeautifulSoup4
        - SQLAlchemy

# How it works?
        1. Python connects to site through URL via requests library
        2. BeautifulSoup4 gets connect and parses (scraps) site
        3. Some functions transforms scrapped info to required format
        4. MySQL database saves the results of parsing into table through SQLAlchemy ORM

# HOW TO SET UP
WebScrapper a pretty easy to set up on your device. Just follow the instructions below:

# MYSQL
        1. Install a MySQL Workbench.
        2. Open one MySQL connection
        

# PYTHON
        1. Clone this repository into your device.
        2. Open project terminal and type: python -m pip install -r requirements.txt
        3. Create a db_config.py file in project folder and type some important variables in:
                host = '127.0.0.1' # or another IP if you using host
                user = 'root'
                password = 'password' # you can type any password you want, but you should remember it
                db_name = 'houses_db'

Perfect! Now you can run scrapper.py, wait some time and look out the results in MySQL Workbench
        

        
        
        
