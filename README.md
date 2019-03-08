# UNESCO Database Solution

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Give examples
```

### Installing

Run the following lines one by one after loging into your new server.

[Say the server is Ubuntu based distribution with IP - 159.89.124.218]

```
cd ~
mkdir app
cd app
apt install python
sudo apt update
python3 -V
sudo apt install python3-django
sudo apt update
sudo apt install python3-pip
sudo apt install python3-venv
python3.6 -m venv my_env
source my_env/bin/activate
pip install django
pip install -U channels
pip install --upgrade django-crispy-forms
pip install image
sudo apt update
sudo apt install redis-server
//  ps aux | grep redis <<Check running redis servers>>
//  /etc/init.d/redis-server restart
//  /etc/init.d/redis-server stop
//  /etc/init.d/redis-server start
pip install asgi_redis
pip install asgiref==2.2.0
pip install channels_redis
/etc/init.d/redis-server start <<if not started>>
git clone https://github.com/acferreir4/UNESCO-Database-Project.git
cd UNESCO-Database-Project/djangoUnescoProject/
python manage.py runserver 159.89.124.218:8000
```

NOTE: in the settings.py we have to add our droplet hostip, like below
ALLOWED_HOSTS = ['159.89.124.218']

## Optonal Tasks

keep it the site live: Keep the app running after you exit the console by using screen to keep the app running on the background.

```
make new screen session
1. screen
2. python manage.py runserver 159.89.124.218:8000
3. CLT+A then d

<<resume cmd>>  screen -r
		  	        screen -r 22082.pts-0.UNESCO-Project <<to kill specific screen>>
<<kill cmd>>    screen -r 22056.pts-0.UNESCO-Project kill
```
## Keep it synced with github
How To Use Git Hooks To Automate Development and Deployment Tasks: https://www.digitalocean.com/community/tutorials/how-to-use-git-hooks-to-automate-development-and-deployment-tasks


End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

