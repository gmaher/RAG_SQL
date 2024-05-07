#!/bin/bash

wget http://mlg.ucd.ie/files/datasets/bbc-fulltext.zip

unzip bbc-fulltext.zip

rm bbc-fulltext.zip

mv bbc documents

rm ./documents/README.TXT
