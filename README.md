# iJoRMS

IT Job Résumé Matching System

## Setup

Pre-setup: Make sure `java` is installed on the device.

For Ubuntu:

```
add-apt-repository ppa:webupd8team/java
apt update; apt install oracle-java8-installer
```

1. Clone the project:

```
git clone https://github.com/ManishChandra12/iJoRMS.git
```

2. Install pipenv, if not already installed.
```
pip install pipenv
```

3. Create a virtual environment and install all the dependencies.

```
pipenv install
```

4. Activate the virtual environment.

```
pipenv shell
```

5. Run the application:

```
python manage.py runserver
```

It runs the application on `127.0.0.1:8000`.
