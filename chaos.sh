#!/bin/sh

# periodically just delete the db file to cause chaos
while (); do
    random -e
    if [ "$?" == "0" ]; then
        rm -f dbfile
    fi
    sleep 15
done
