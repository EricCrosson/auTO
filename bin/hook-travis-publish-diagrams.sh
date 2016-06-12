#!/usr/bin/env bash
# Written by Eric Crosson
# 2016-04-26

# Exit under these circumstances -- when we don't care about publishing diagrams
if [[ "$TRAVIS_REPO_SLUG" != "EricCrosson/auTO" || \
            "$TRAVIS_PULL_REQUEST" != "false" || \
            "$TRAVIS_BRANCH" != "master" ]]; then
    echo "Quitting $0"
    echo "TRAVIS_REPO_SLUG is <$TRAVIS_REPO_SLUG>"
    echo "TRAVIS_PULL_REQUEST is <$TRAVIS_PULL_REQUEST>"
    echo "TRAVIS_BRANCH is <$TRAVIS_BRANCH>"
    exit
fi

# Get to the Travis build dir, configure git and clone the repo
cd $HOME
git config --global user.email "travis@travis-ci.org"
git config --global user.name "travis-ci"
git clone --depth 1 --quiet --branch=diagrams https://${GH_TOKEN}@github.com/ericcrosson/auto $HOME/auto

# Commit and push changes
cd $HOME/auto
cp -fv README* $HOME/diagrams
git rm -rf *
cp -Rfv $HOME/diagrams/* ./
git add -f .
git commit -m "Latest diagrams from successful travis build $TRAVIS_BUILD_NUMBER auto-pushed to diagrams"
git push -fq origin diagrams > /dev/null
