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

### previewing the site

This outputs the site to a temporary directory with a live-preview at http://localhost:8000

```sh
pipenv run pelican -s ./pelicanconf.py -lr --relative-urls -o $(mktemp -d)
```

### publishing to GitHub Pages

Build the site to the `output/` directory by running:

```sh
pipenv run pelican -s ./pelicanconf.py
```

After reviewing and committing the changes to the directory, publish it by pushing it to the `gh-pages` subtree:

```sh
git subtree push --prefix output origin gh-pages
```

### docker

Build the site with the desired output and then run:

```sh
docker build -t dafnelately/dont-reinvent-bicycle:latest .
```

You can preview the container at http://localhost:8000 by running:

```sh
docker run --rm -p 8000:80 dafnelately/dont-reinvent-bicycle:latest
```

### pygment

Generating a pygment theme:

```bash
pipenv run pygmentize -S perldoc -f html -a .highlight > theme/static/css/pygment.css
```
