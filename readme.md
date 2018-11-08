# Zotler

Zotler (ZotFile Butler) searches ZotFile Custom Location of attachment files and
makes a list containing files not linked in Zotero database. The files can be
deleted directly or saved to a file. The file can be edited and used as a template
for subsequent removal of the orphan files.

## Requirements

* Linux
* Python 3.6+
* Zotero with ZotFile addon

## Installation

###Linux

1. Clone Zotler from GitHub

   $ git clone https://github.com/vrbacky/zotler.git

2. Change directory to Zotler

   $ cd zotler

3. Install Zotler
   
   $ python3 setup.py install


## Running Zotler

### Overview

Path to location of the files is parsed from the Custom Location setting in
ZotFile preferences saved in the prefs.js file. Path to the file can be passed
as an option -p or it can be created automatically using default path
`~/.zotero/xxxxxxxx.default/prefs.js` (Linux only). The first dictionary ending with
.default is used.

Path to the Zotero database file zotero.sqlite can be specified using -f option or
-d option. Later option sets path to the Zotero home dictionary containing
zotero.sqlite file. Default path `~/Zotero/zotero.sqlite` (Linux only) is used
if both options are omitted.

### Examples:

Parse path to ZotFile attachments from `~/.zotero/zotero/xxxxxxx.default/pref.js`
file, use default path to Zotero database file (`~/Zotero/zotero.sqlite`), find
orphan files and save paths to the files to `~/orphans.txt` file:

`$ python zotler.py -o ~/orphans.txt`

or

`$ python zotler.py -p ~/.zotero/zotero/xxxxxxx.default/pref.js
-f ~/Zotero/zotero.sqlite -o ~/orphans.txt`

Delete files listed in ~/orphans.txt file:

`python zotler.py -l ~/orphans.txt`

## Author

Filip Vrbacky

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Contact

If you have questions you can email
`Filip Vrbacky <mailto:vrbacky@fnhk.cz>`__.

If you've discovered a bug or have a feature request, you can create an issue
on GitHub using the
`Issue Tracker <https://github.com/vrbacky/zotler/issues>`__.