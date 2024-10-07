# syntax=docker/dockerfile:1
########## Base image
# https://hub.docker.com/_/ruby/tags
FROM docker.io/ruby:3.3.1-slim-bullseye as base

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
  apt upgrade -y && \
  apt install -y wget curl autoconf bison build-essential libffi-dev libgdbm-dev libncurses5-dev libssl-dev libyaml-dev libreadline6-dev zlib1g-dev git

# Create unprivileged "app" user
# From then on, run as unprivileged app user
RUN useradd --home-dir /app --create-home --shell /bin/bash --uid 1000 app
USER app

# Install rake and bundler
ENV PATH=/app/.gem/ruby/3.3.1/bin:$PATH
RUN gem install --user-install bundler --version 2.3.26
RUN gem install --user-install rake --version 13.1.0

########## Clone repo
FROM base AS forum-git
ARG FORUM_REPOSITORY={{ FORUM_REPOSITORY }}
ARG FORUM_REPOSITORY_VERSION={{ FORUM_REPOSITORY_VERSION }}
ADD --keep-git-dir=true $FORUM_REPOSITORY#$FORUM_REPOSITORY_VERSION /app/cs_comments_service

########## Empty layer with just the repo at the root.
# This is useful when overriding the build context with a host repo:
FROM scratch AS forum-src
COPY --from=forum-git /app/cs_comments_service /

########## Production image
FROM base AS production
COPY --link --chown=1000:1000 --from=forum-src / /app/cs_comments_service

# Install ruby requirements
WORKDIR /app/cs_comments_service
RUN bundle config set --local deployment 'true'
RUN bundle install

ENV SINATRA_ENV=staging
ENV NEW_RELIC_ENABLE=false
ENV API_KEY=forumapikey
ENV SEARCH_SERVER_ES7=http://elasticsearch:9200
ENV MONGODB_AUTH=""
ENV MONGODB_HOST=mongodb
ENV MONGODB_PORT=27017
ENV MONGODB_DATABASE=cs_comments_service
# Duplicating the function of dockerize
ENV MONGOID_TIMEOUT=600

EXPOSE 4567
CMD ./bin/unicorn -c config/unicorn_tcp.rb -I '.'
