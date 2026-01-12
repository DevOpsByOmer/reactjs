#!/bin/sh

echo "Generating runtime env.js file..."
envsubst < /usr/share/nginx/html/env.js.template > /usr/share/nginx/html/env.js

echo "Starting NGINX..."
nginx -g 'daemon off;'
