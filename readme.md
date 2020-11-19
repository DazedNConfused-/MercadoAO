# Mercado AO

[![GitHub license](https://img.shields.io/github/license/DazedNConfused-/MercadoAO?style=flat-square)](https://github.com/DazedNConfused-/MercadoAO/blob/master/LICENSE)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/DazedNConfused-/MercadoAO?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/DazedNConfused-/MercadoAO?style=flat-square)
![LGTM Grade](https://img.shields.io/lgtm/grade/python/github/DazedNConfused-/MercadoAO?style=flat-square)
![Travis (.com)](https://img.shields.io/travis/com/DazedNConfused-/MercadoAO?style=flat-square)

## What is this?

This is a Discord bot that aims to help players of MMORPG [Argentum Online](https://es.wikipedia.org/wiki/Argentum_Online) (_AO_ for short) with the barter of items between each other. 

Users in a server with this bot running can publish items to be sold; list item offerings (either all currently undergoing, or by making a specific search for an item); and/or claim said sales for their own, in which case the bot will DM involved parties so they can meet up and finish the transaction.

## Why is this useful?

If you have ever played vanilla **Argentum** (or its mods for that matter), you most probably have already realized that they are severely lacking in the commerce aspect. With the exception of only the most modified client/server variants, the game doesn't even have an auction system in place. Therefore most "merchants" must publish their sales on the game's forums and hope that potential buyers are keeping an eye on these commerce threads that pop up. With the advent of Discord and the des-use of bulletin boards, this practice is becoming more cumbersome day by day (some currently undergoing **Argentum** projects don't even have a forum anymore!).

## What's to stop players from bartering between each other in the game's Discord server? 

Nothing, but don't you find that a little spam-prone?

Even with a dedicated commerce Discord channel - which is what most **Argentum** servers end up doing to organize things a little - a couple dozen players shouting their offerings in a public chat can hardly be called a "marketplace". The issue is only going to get worse the more people are present, so it pays to have an entity centralizing the offerings while also providing some listing and searching capabilities.

## You have convinced me!

Good! Then go on into [configuring your MercadoAO instance](#configuration). It shouldn't take more than a couple of minutes to have the bot completely set up and administering your game's marketplace!

---

## Configuration

If you have come this far, then you want to set up a MercadoAO instance for your game server. Here is what you have to do:

### Starting Up

You should setup your Discord's token inside `config.ini`. 

Optionally, if you wish for the bot to make automatic sale announcements every time a new item offering is made - which would help keep the economy going and the money flowing :laughing: - then the announcement-channel's ID should also be specified ([see how to get a Discord's channel's ID](https://github.com/Chikachi/DiscordIntegration/wiki/How-to-get-a-token-and-channel-ID-for-Discord)).

### Specifying the Market's Sellable Items

The bot will load and index the complete list of all sellable items on startup. No offerings nor searches can be made on items outside this list.
 
It currently has a base master list coming from [vanilla Argentum Online's .DAT files](https://www.comunidadargentum.com/manual/?seccion=dat_viewer_items); but your game's item list may be different in practice (specially if your game is an **Argentum** mod), and that's why you can customize it to your game's flavor. 

Said item master list lives in `resources/items.json`, and should be an array with the following structure:

```json
{
    "nombre": "Manzana Roja",
    "precio": "2"
}
```

Extra parameters are allowed but ignored. 

The master list will be indexed on MercadoAO's startup. While indexing, each item will be given a unique identifier (UID) based on its name, checking for collisions. If a collision is detected, it is a strong indicator of a duplicate item, which is not allowed and should be sanitized (entry removed or renamed) before starting up the bot again.

Given that the Item's UIDs are hashed constants, they are volatile and can be rebuilt without repercussions as long as the item's names remain the same.

### Allowed Commands

To see a list of all allowed commands, type `$help` in a channel where the bot is in. For more information about a specific command, type `$help <command>`

---

## Developer section

From this point onwards, this information will only be relevant if you want to add features to the bot yourself.

### Initial Setup

In order to start developing features for this bot, you will have to install its dependencies and setup the commit hooks:

```bash
pipenv install
pipenv run pre-commit install -t pre-commit
pipenv run pre-commit install -t pre-push
```