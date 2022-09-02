#!/bin/bash

case "$1" in
  total)
    echo `ss -tan | sed '1d' | wc -l`
    ;;
  established)
    echo `ss -tan | sed '1d' | grep -c '^ESTAB'`
    ;;
esac
