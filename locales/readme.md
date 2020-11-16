# Internazionalization support

Internationalization is officially supported thanks to [Babel](http://babel.pocoo.org/en/latest/).

Upon installation of Babel (should be a dev dependency of the project), a script called `pybabel` will be made available for use inside Python's environment.

In order to update the translations for the project, take into account the following steps (all commands must be ran from project's root):

1. Mark all strings that should be translated inside the codebase:
   ```python
       # import the custom wrapper of Python's gettext
       _: Callable[[str], str] = lambda s: I18n().gettext(s)
       
       # wrap the strings you want to make translations available for like this:
       _('this is a string that will later be picked up by gettext scrapper)
   ```
   This will mark the string as scrapable, and will later get translated at runtime.
2. Extract all translation-able strings from project. This will generate a master list that will be used to build each specific locale.
    ```bash
    pybabel extract -o locales/messages.pot .
    ```
3. With all extracted strings (both old and new), we must build the locale-specific lists:
   _NOTE_: this will not delete previous translations; just add the newly added ones.
   ```bash
   pybabel update -i locales/messages.pot -o locales/<LOCALE>/LC_MESSAGES/messages.po -l <LOCALE>
   ```
   In this case, since we have two locales (`en` and `es_ar`), the commands to update are:
   ```bash
   pybabel update -i locales/messages.pot -o locales/en/LC_MESSAGES/messages.po -l en
   pybabel update -i locales/messages.pot -o locales/es_AR/LC_MESSAGES/messages.po -l es_AR
   ```
   1. If we wanted to initialize a locale for the first time, the command would be:
   ```bash
   pybabel init -i locales/messages.pot -d locales/. -l <LOCALE>
   ```
4. In order to compile the translations into usable binaries for GNU's `gettext`, we must run at the end:
    ```bash
    pybabel compile -f -d locales/.
    ```