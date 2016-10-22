##################################################
#
#                    ##        .
#              ## ## ##       ==
#           ## ## ## ##      ===
#       /""""""""""""""""\___/ ===
#  ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
#       \______ o          __/
#         \    \        __/
#          \____\______/
#
# Hack-MIT
##################################################

FROM python:2.7
MAINTAINER Kevin McDonough <kmacdough@gmail.com>

COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN rm /requirements.txt

# Use for creating a fully contained image
#ADD /src /app

# Use this for live-editing the code instead of ADD /src /apps
RUN mkdir /app
VOLUME /app

#RUN mkdir /logs

# Set the default directory where CMD will execute
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["runserver.py"]
