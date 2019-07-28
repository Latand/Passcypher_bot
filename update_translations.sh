#!/usr/bin/env bash
pybabel extract bot/ -o locales/pcypher.pot
pybabel update -d locales -D pcypher -i locales/pcypher.pot
pybabel compile -d locales -D pcypher