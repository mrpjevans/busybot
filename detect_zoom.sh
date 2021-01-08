#!/bin/sh
lines=`ps ax | grep CptHost | wc -l | xargs`
if [ $lines -gt 1 ]; then
  echo "Running"
else
  echo "Not"
fi