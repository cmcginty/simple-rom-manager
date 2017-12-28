# Simple ROM Manager

[![Build Status](https://travis-ci.org/cmcginty/simple-rom-manager.svg?branch=master)](https://travis-ci.org/cmcginty/simple-rom-manager)
[![Status](https://img.shields.io/pypi/status/simple-rom-manager.svg)](https://pypi.python.org/pypi/simple-rom-manager)
[![Version](https://img.shields.io/pypi/v/simple-rom-manager.svg)](https://pypi.python.org/pypi/simple-rom-manager)
[![PyVersion](https://img.shields.io/pypi/pyversions/simple-rom-manager.svg)](https://www.python.org/)
[![License](https://img.shields.io/pypi/l/simple-rom-manager.svg)](https://github.com/cmcginty/simple-rom-manager/blob/master/LICENSE.md)

A command-line tool for verifying console and arcade ROMs against published ROM set DAT files.

For users familiar with ROM management, the goal of this tool is to implement some of the verification and file management features found in [ClrMamePro](https://mamedev.emulab.it/clrmamepro/).

## About

There are a few groups that publish a collection of metadata for ROMs used in legacy gaming systems and arcades. In some cases the data is simply a "best-of" list for defining complete ROM set. For emulators like [MAME](https://github.com/mamedev/mame/releases) ([split](https://github.com/libretro/fbalpha/tree/master/dats)) or [FBA](https://github.com/libretro/fbalpha/tree/master/dats), a ROM may not work correctly when used with older versions of a ROM.

[No-Intro](http://no-intro.org/) is one groups that publish ROM sets for many gaming consoles on their [Dat-O-Matic](http://datomatic.no-intro.org/) site.

Simple ROM Manager (SRM) can be used to quickly manage ROMs into a collection by confirming ROMs that are _good_, _bad_, and _missing_ and by renaming and/or re-packaging the files.

## Features

* `srm init` command to put the current directory under management.

## Usage

Setup a top-level directory all of the ROMs referenced inside of a DAT file.

```
$ cd ~/MyRoms/System
$ srm init
```

## Install

It's unlikely that your OS package manger contains a version of SRM. For now, you can install using PIP:

```bash
$ pip3 install srm
```

## Latest News

This software is pre-release. Please check back later for announcements or read the [design doc](DESIGN.md) for more details on what features are planned.
