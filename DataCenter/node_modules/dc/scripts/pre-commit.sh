#!/usr/bin/env bash

# probably a dumb way to detect changed files which are not deleted
scripts/check_merge_conflict.py `comm -12 <(git diff --name-only --cached) <(git ls-files)` && grunt lint
