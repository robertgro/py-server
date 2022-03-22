@echo off
if not exist py-server mkdir py-server
cd py-server
if not exist .git git init
if not exist env python -m venv env
if not exist img git clone https://github.com/robertgro/py-server.git
call pip_install_dep.cmd
::https://stackoverflow.com/questions/2883840/differences-between-git-pull-origin-master-git-pull-origin-master
::https://stackoverflow.com/questions/3620633/what-is-the-difference-between-pull-and-clone-in-git
::https://ss64.com/nt/syntax-empty.html