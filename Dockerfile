# syntax=docker/dockerfile:1
 FROM archlinux:latest

 WORKDIR /hat
 COPY docker docker

 RUN cp docker/mirrorlist /etc/pacman.d/mirrorlist
 RUN pacman -Syu --noconfirm

 COPY requirements.pacman.txt requirements.pacman.txt
 RUN pacman -Sy $(< requirements.pacman.txt) --noconfirm

 COPY requirements.pip.txt requirements.pip.txt
 RUN pip install -r requirements.pip.txt
