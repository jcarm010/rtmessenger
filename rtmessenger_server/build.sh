#!/bin/bash
rm rtmessenger_server.zip
zip -r rtmessenger_server.zip * .ebextensions/ --exclude=*node_modules/* -x *.zip*