#!/bin/sh -e

# the search server variable was renamed after the upgrade to elasticsearch 7
export SEARCH_SERVER_ES7="$SEARCH_SERVER"

echo "Waiting for mongodb/elasticsearch..."

WAIT_MONGODB=""
if [ "${MONGODB_HOST#mongodb+srv://}" != "${MONGODB_HOST}" ]; then
    echo "MongoDB is using SRV records, so we cannot wait for it to be ready"
    export MONGOHQ_URL="$MONGODB_HOST/$MONGODB_DATABASE"
else
    export MONGOHQ_URL="mongodb://$MONGODB_AUTH$MONGODB_HOST:$MONGODB_PORT/$MONGODB_DATABASE"
    WAIT_MONGODB="-wait tcp://$MONGODB_HOST:$MONGODB_PORT"
fi

dockerize $WAIT_MONGODB -wait $SEARCH_SERVER -wait-retry-interval 5s -timeout 600s

exec "$@"
