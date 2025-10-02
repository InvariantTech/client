#!/bin/bash

mkdir -p invariant_client/bindings/
pushd invariant_client/bindings/
poetry run openapi-python-client generate --path ../../schema/openapi.json --overwrite --output-path invariant_instance_client --meta=none
poetry run openapi-python-client generate --path ../../schema/openapi_login.json --overwrite --output-path invariant_login_client --meta=none
popd
