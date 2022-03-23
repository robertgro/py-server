@echo off
if not exist py-server mkdir py-server
cd py-server
if not exist .git git init
::https://stackoverflow.com/questions/15637507/fatal-origin-does-not-appear-to-be-a-git-repository
git remote add origin https://github.com/robertgro/py-server.git
git pull origin master
::https://stackoverflow.com/questions/35450049/what-does-would-be-overwritten-by-merge-mean
if not exist env python -m venv env
::if not exist img git clone https://github.com/robertgro/py-server.git
::for /r %%i in (py-server\*.*) do move %%i %%~pi..
::for /d %%i in (py-server\*) do move %%i %%~pi..
::rmdir /s /q py-server
::https://stackoverflow.com/questions/4228807/copy-files-without-overwrite
::https://ss64.com/nt/move.html
::https://superuser.com/questions/1115231/batch-move-a-folders-content-up-one-level
pip_install_dep.cmd
::https://stackoverflow.com/questions/2883840/differences-between-git-pull-origin-master-git-pull-origin-master
::https://stackoverflow.com/questions/3620633/what-is-the-difference-between-pull-and-clone-in-git
::https://ss64.com/nt/syntax-empty.html

::https://superuser.com/questions/1115231/batch-move-a-folders-content-up-one-level
::https://stackoverflow.com/questions/10155420/recursive-move-command-on-windows