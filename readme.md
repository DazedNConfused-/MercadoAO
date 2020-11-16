# Mercado AO

[![GitHub license](https://img.shields.io/github/license/DazedNConfused-/MercadoAO?style=flat-square)](https://github.com/DazedNConfused-/MercadoAO/blob/master/LICENSE)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/DazedNConfused-/MercadoAO?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/DazedNConfused-/MercadoAO?style=flat-square)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/DazedNConfused-/MercadoAO?style=flat-square)
![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/DazedNConfused-/MercadoAO?style=flat-square)
![Travis (.com)](https://img.shields.io/travis/com/DazedNConfused-/MercadoAO?style=flat-square)

## Initial Setup

In order to start developing features for this bot, you will have to install its dependencies and setup the commit hooks:

```bash
pipenv install
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```

## Starting up

You should setup your Discord's token inside `config.ini`. 

Optionally, if you wish for the bot to make automatic sale announcements, then the announcement-channel's ID should also be specified ([see how](https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord)).

## Specifying the Market's Sellable Items

The bot will load and index the complete list of all sellable items on startup. Said list lives in `resources/items.json`, and should be an array with the following structure:

```json
{
    "nombre": "Manzana Roja",
    "precio": "2"
}
```

Extra parameters are allowed but ignored. 

While indexing, each item will be given a unique identifier (UID) based on its name, checking for collisions. If a collision is detected, it is a strong indicator of a duplicate item, which is not allowed and should be removed or renamed before starting up the bot again.

Given that the Item's UIDs are hashed constants, they are volatile and can be rebuilt without repercussions as long as the item's names remain the same.

## Allowed Commands

To see a list of all allowed commands, type `$help` in a channel where the bot is in. For more information about a specific command, type `$help <command>`