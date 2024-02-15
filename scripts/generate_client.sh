#!/bin/bash

mkdir -p invariant_client/bindings/
pushd invariant_client/bindings/
poetry run openapi-python-client generate --path ../../schema/openapi.json --meta none
poetry run openapi-python-client generate --path ../../schema/openapi_login.json --meta none
popd
