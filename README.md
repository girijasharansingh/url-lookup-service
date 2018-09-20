# url-lookup-service

Problem Statement:

We have an HTTP proxy that is scanning traffic looking for malware URL's. Before allowing HTTP connections to be made, this proxy asks a service that maintains several databases of malware URL's, if the resource being requested is known to contain malware.

We have to create a small web service, that responds to GET requests, where the caller passes in a URL and the service responds with some information about that URL.
The GET requests would look like this:

`GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}`

Solution Implemented:

Pre-requisites:

- This service is intended to run `Ubuntu 18.04`

- Install Python : `sudo apt install python3`

- Install pip : `sudo apt install python3-pip`

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

References:
```markdown
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04
https://askubuntu.com/questions/1029177/error-1698-28000-access-denied-for-user-rootlocalhost-at-ubuntu-18-04
```
