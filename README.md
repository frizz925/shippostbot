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

Simply run the main script to start using the bot.

```sh
python main.py
```

### Bot functionality levels

The bot has 3 levels of functionality:

1. Creating caption, comment, and combined image
2. Uploading combined image to an [AWS S3](https://aws.amazon.com/s3/) bucket
3. Publishing post and comment to a Facebook page

The available functionality is determined by the *environment variables*.

The first level requires **no environment variables** and it will save the combined image locally along with the caption, comment, and image file url in a JSON format like the following:

```json
{
    "caption": "Character A X Character B",
    "comment": "<comment here>",
    "image_url": "<locally saved image url here>"
}
```

This is useful if you just need the simplest, working functionality of the bot, in which you have your own way of uploading the image and posting them to any places you'd like. This opens up opportunity of the bot being reusable not only as a Facebook bot, but also bot in any other form like Discord and Twitter bots.

(The second and third levels documentation is TBA for the moment)

## Deployment

TBA

## Issues and Suggestions

Should you find any issues with the bot or if you happen to have any suggestions to further improve the bot, you can head over to the [Issues](https://github.com/Frizz925/shippostbot/issues) page.

## License

GPL-3.0
