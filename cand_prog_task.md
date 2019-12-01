# Programming exercise

## Task

Develop in Python3 a script that takes a configured grouped list of urls to check,
for each url it must be possible to specify regular expressions that are matched
in the content.

The results of the check must be stored somehow for later analysis, at bare minimum
must contain the time of check, response time and possible error if check was not
successful.

The process must be able to run continuously doing the checks periodically. It must
be able to deal with large number of urls without exploding, it must always respond
to user input (ctrl-c for example in case of CLI script) within one second and clean
up any resources gracefully on exit.

If you choose to make a GUI application use GTK or QT (Definitely not Tk)

You must document how to install and use your script and comment your code where you
see it being useful.

Script must work on Linux regardless of what OS was used for development.

Even if we use the word "script" it does not mean that the solution must
be self-contained in one file.

This should be doable in a few hours ("One evening"), no need to get fancy:
"Real developers ship".

All design decisions are yours to make, be prepared to explain why you made
a particular choice.

## Tips

  - [PEP8][pep8] style, indent is 4 spaces, EOL is UNIX newline.
  - Concurrency good
  - Asynchronous IO good
  - Idiomatic code good
  - Git good
  - Unit tests good ([`py.test`][pytest] preferred)
  - Lots of external dependencies bad
  - Documenting design decisions good

[pep8]: https://www.python.org/dev/peps/pep-0008/
[pytest]: https://docs.pytest.org/en/latest/

## Delivery

Deliver the code and documentation to us any way you see best, there is nothing
secret here so publishing on public git hosting is perfectly acceptable.

If you choose to use an "proper database" you must provide a `docker-compose` file that will take care of all the setups.
