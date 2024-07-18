#!/bin/dash
exec fork dash -c '. ./ircdenv/bin/activate ; exec fork python3 ircd.py --fork'
