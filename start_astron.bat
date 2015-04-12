@echo off
title astrond
echo ===============================
echo Starting Toontown Rewritten Astron Cluster...
echo ===============================
astrond --loglevel info config/dev.yml
pause