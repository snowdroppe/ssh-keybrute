# ssh-keybrute
Simple python3 framework to parellelise ssh key bruteforcing

I couldn't find a python3 native script to perform ssh key bruteforcing against legacy targets (such as Debian machines affected by CVE-2008-0166), so I wrote my own. It already has a bunch of algorithm compatibilitiy options included to force modern ssh clients ignore security concerns and connect using legacy methods.

Objectives when writing this tool:
* Native to python3
* Lightweight
  * Only uses bundled modules / system bins
* Customisable
  * Most aspects can be modified including ssh options and error checking to fit your needs
* Simple
  * Code is *kinda* readable and compact
* Parallelisable
  * And mostly threadsafe n_n

## Usage
The script is mostly self documenting. All configuration is done in the `config` dictionary, clearly marked at the top of the script.

Enabling `debug` will print the stderr output of the command which can help troubleshoot if ssh is failing because the key isn't accepted or something unexpected such as lax permissions on the private key file.

## Todo
- [x] Make status message pretty and success / failure blindingly obvious
- [ ] Bug test script fully
- [ ] Finish readme
