# How to contribute

## Issue Submission Guidelines

* Because of the volume of requests, we do not use the issue tracker for support questions. If you are trying to get a particular effect or you have a problem with your code, please ask your question on stackoverflow.com or the [user group](https://groups.google.com/forum/?fromgroups#!forum/dc-js-user-group)
* It will be far, far easier for others to understand your problem or bug if you demonstrate it with a short example on http://jsfiddle.net/ or on http://bl.ocks.org/ (http://blockbuilder.org/ is a great way to edit bl.ocks!). Here are some examples you can fork to get started:
  * [example jsFiddle](http://jsfiddle.net/gordonwoodhull/os27xcg2/) with some data and a chart.
  * [blank jsFiddle](http://jsfiddle.net/gordonwoodhull/u57bfje8/) using the latest dc.js from github.io
  * the same example [as a bl.ock](http://bl.ocks.org/gordonwoodhull/ecce8e32d64c662cffd5); [on blockbuilder.org](http://blockbuilder.org/gordonwoodhull/ecce8e32d64c662cffd5)
  * a blank template bl.ock [on blockbuilder.org](http://blockbuilder.org/gordonwoodhull/9ab997c9a8d7d3380364)
* For bugs and feature requests submit a [github issue](http://github.com/dc-js/dc.js/issues)
  * Please include the version of DC you are using
  * If you can, please try the latest version of DC on the [master](https://raw.github.com/dc-js/dc.js/master/dc.js) branch to see if your issue has already been addressed or is otherwise affected by recent changes.

## Pull Request Guidelines

* Fork the repository.
* As with all pull requests, put your changes in a branch. For contributions that change the dc.js API, create your branch off of `develop`. If your contribution does not change the API, branch off of `master` instead.
* Make changes to the files in `src/` not dc.js
* Add tests to `spec/`. Feel free to create a new file if needed.
* Run `grunt server` and go to http://localhost:8888/spec to develop your tests.
* If your changes might affect transitions, go to the relevant transition tests in http://localhost:8888/web/transitions and watch them by eye to see if they make sense
* Run `grunt lint` to confirm that your code meets the dc.js style guidelines.
* Run `grunt test` to confirm that all tests will pass on phantomjs.
* Commit your changes to `src/*` and `spec/*` but not any build artifacts.  (Build artifacts include `dc.*js*`, `web/docs/*`, `web/js/*`)
* Submit a pull request.
* If you merge `develop` or `master` into your patchset, please rebase against develop. (It's okay to rewrite history for PRs, because these branches are temporary and it's unlikely that anyone is tracking your feature branch.)
* The DC maintainer team will review and build the artifacts when merging.
* If you continue making changes to your fork of `dc.js`, create a separate branch for each pull request and keep the changes separate.

#### Coding Conventions

* Avoid tabs and trailing whitespace
* Please try to follow the existing code formatting
* We use jshint and jscs to verify most of our coding conventions

It helps keep on top of the conventions if you create a git pre-commit hook `.git/hooks/pre-commit`:
```
#!/usr/bin/env sh

grunt jshint
grunt jscs
```

(You also need to make it executable with  `chmod u+x .git/hooks/pre-commit`)

Or you can just run the commands manually before committing.

#### Testing Notes

Running `grunt server` will host the jasmine specs at http://localhost:8888/spec.
Please use `.transitionDuration(0)` for all chart tests.
