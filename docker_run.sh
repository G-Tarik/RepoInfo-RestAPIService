#!/usr/bin/bash
docker run -d --rm --name repoinfo-app -p 7001:7000 --network="test-net" --ip 172.31.1.10 repoinfo-app:v1
