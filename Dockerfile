FROM ubuntu:trusty
RUN apt-get update && apt-get install -y build-essential debhelper devscripts equivs git-core curl python-dev python-setuptools python-pip && pip install debfolder

COPY ./ /build/oscarslam/

WORKDIR /build/oscarslam
RUN debfolder --changelog
RUN dpkg-source -b ./
RUN mk-build-deps -i ../*.dsc -r -t "apt-get -y"
RUN dpkg-buildpackage -b
RUN dpkg -i ../*.deb
RUN apt-get install -f
CMD /usr/share/python/oscarslam/bin/oscarslam
