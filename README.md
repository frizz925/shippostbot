# ShippostBot

[![Travis (.org) branch](https://img.shields.io/travis/Frizz925/shippostbot/master.svg?style=flat-square)](https://travis-ci.org/Frizz925/shippostbot)
[![Codecov branch](https://img.shields.io/codecov/c/gh/Frizz925/shippostbot/master.svg?style=flat-square)](https://codecov.io/gh/Frizz925/shippostbot)
[![GitHub](https://img.shields.io/github/license/Frizz925/shippostbot.svg?style=flat-square)](https://github.com/Frizz925/shippostbot/blob/master/LICENSE)

Your friendly bot for pairing your favorite anime characters, [ShippostBot](https://www.facebook.com/ShippostBot/)

## Usage

### Requirements

Here are the requirements in order to use the bot:

- Python 3.7
  - pip
  - virtualenv
- ImageMagick
- Git

Furthermore, the bot had only been tested to work on Ubuntu 18.04. It may still work on other platforms like macOS and Windows if you have the required tools and software, but they have not been tested yet.

### Setup

The following commands assume that you're using bash or similar shell.

Clone the repository using Git.

```sh
git clone https://github.com/Frizz925/shippostbot.git
cd shippostbot
```

It is recommended to create a *virtualenv* in order to keep the bot in an isolated environment so that it would work normally.

```sh
virtualenv -p $(which python3.7) .venv
source .venv/bin/activate
```

At this point, you should be inside an isolated environment of *virtualenv*. You can then use *pip* to install the required Python packages.

```sh
pip install -r requirements.txt
```

### Testing

Tests are done using [nose](https://nose.readthedocs.io/en/latest/). However, it is likely that different testing framework would be used should new test requirements arise in the future.

```sh
pip install nose
```

You can then run the tests and see if the test cases pass successfully.

```sh
nosetests
```

### Using the bot

An additional Python package is required to run the bot from command line.

```sh
pip install click
```

After that, simply run the bot's package module to start using the bot.

```sh
python -m shippostbot
```

### Command line arguments

TBA

### Environment variables

TBA

## Deployment

TBA

## Issues and Suggestions

Should you find any issues with the bot or if you happen to have any suggestions to further improve the bot, you can head over to the [Issues](https://github.com/Frizz925/shippostbot/issues) page.

## License

GPL-3.0
