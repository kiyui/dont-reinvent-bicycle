# dont-reinvent-велосипед

## setup

Make sure you have `python` and `pip` 3 installed on your host OS. Start by installing `pipenv`:

```sh
pip3 install --user pipenv
```

Clone the repository:

```sh
git clone --recurse-submodules git@github.com:kiyui/dont-reinvent-bicycle.git dont-reinvent-велосипед
```

Install the dependencies:

```sh
pipenv install
```

## building

### output

Publishing the site:

```sh
pipenv run pelican -s ./publishconf.py
```

Testing the site:

```sh
pipenv run pelican -s ./pelicanconf.py
```

### docker

Build the site with the desired output and then run:

```sh
docker build -t dafnelately/dont-reinvent-bicycle:latest .
```

### pygment

Generating a pygment theme:

```bash
pipenv run pygmentize -S perldoc -f html -a .highlight > theme/static/css/pygment.css
```
