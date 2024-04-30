#!/bin/sh -e

# the search server variable was renamed after the upgrade to elasticsearch 7
export SEARCH_SERVER_ES7="$SEARCH_SERVER"

echo "Waiting for mongodb/elasticsearch..."

DOCKERIZE_COMMAND="dockerize -wait-retry-interval 5s -timeout 600s"

WAIT_MONGODB=""
if [ "${MONGODB_HOST#mongodb+srv://}" != "${MONGODB_HOST}" ]; then
    echo "MongoDB is using SRV records, so we cannot wait for it to be ready"
    export MONGOHQ_URL="${MONGODB_HOST}/${MONGODB_DATABASE}"
else
    export MONGOHQ_URL="mongodb://${MONGODB_AUTH}${MONGODB_HOST}:${MONGODB_PORT}/${MONGODB_DATABASE}"
    WAIT_MONGODB="-wait tcp://${MONGODB_HOST}:${MONGODB_PORT}"
fi

WAIT_SEARCH_SERVER="-wait $SEARCH_SERVER"
if [ -n "${ELASTICSEARCH_CA_PATH}" ]; then
    WAIT_SEARCH_SERVER="${WAIT_SEARCH_SERVER} -cacert ${ELASTICSEARCH_CA_PATH}"
fi

$DOCKERIZE_COMMAND $WAIT_MONGODB
$DOCKERIZE_COMMAND $WAIT_SEARCH_SERVER

exec "$@"
