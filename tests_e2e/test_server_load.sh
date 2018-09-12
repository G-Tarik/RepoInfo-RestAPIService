#!/usr/bin/bash

siege -c 20 -r 1 -b http://localhost:7000/github/repositories/octocat/Hello-World
