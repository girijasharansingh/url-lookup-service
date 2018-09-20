# url-lookup-service

Problem Statement:

We have an HTTP proxy that is scanning traffic looking for malware URL's. Before allowing HTTP connections to be made, this proxy asks a service that maintains several databases of malware URL's, if the resource being requested is known to contain malware.

We have to create a small web service, that responds to GET requests, where the caller passes in a URL and the service responds with some information about that URL.
The GET requests would look like this:

`GET http://<IP>:<port>/api/v1/check/url?url=<original_url_to_lookup_for>`

`Ex: http://127.0.0.1:5000/api/v1/check/url?url=dummy.com`

Solution Implemented:
```markdown
The following API server has been implemented in Python 3.6.5 using Flask library.
For backend storage, MySQL database has been used.
Once the API server started, its create connection to the MySQL database and for subsequent GET requests, it uses this same connection.
```
Pre-requisites:

- This service is intended to run `Ubuntu 18.04`

- Install Python : `sudo apt install python3`

- Install pip : `sudo apt install python3-pip`

- Install flask module : `pip3 install flask`

- Install mysql-connector-python module : `pip3 install mysql-connector-python`

- Install and configure MySQL database :
```markdown
sudo apt install mysql-server
sudo mysql_secure_installation
sudo mysql -u root
mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root123';
mysql> SELECT User, Host, HEX(authentication_string) FROM mysql.user;
```

- Create database and populate initial entries :
```markdown
mysql> create database malware_urls;
mysql> use malware_urls;
mysql> create table malwares (id INT NOT NULL AUTO_INCREMENT, url VARCHAR(2000) NOT NULL, PRIMARY KEY (id));
mysql> insert into `malwares` (`id`, `url`) values ('1', 'dummy.com');
mysql> insert into `malwares` (`id`, `url`) values ('2', 'tmp.com');
```

Procedure to use it:

- Clone this repository.
- `cd url-lookup-service/`
- Update `config.ini` according to your environment.
- Run API server using : `python3 url_lookup_server.py`
- Go to the Browser and pass URL : `http://127.0.0.1:5000/`
- Your server is up and running.
- To stop the server press `Ctrl+C` on the same terminal.

References:
```markdown
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04
https://askubuntu.com/questions/1029177/error-1698-28000-access-denied-for-user-rootlocalhost-at-ubuntu-18-04
```
