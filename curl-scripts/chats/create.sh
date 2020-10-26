#!/bin/bash

curl "http://localhost:8000/chats/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "chat": {
      "content": "'"${CONTENT}"'",
      "owner": "'"${OWNER}"'"
    }
  }'

echo
