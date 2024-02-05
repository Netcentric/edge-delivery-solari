#!/usr/bin/env bash
set -x
set -e

ROOT_DIR="$(pwd)"

OUTPUT_DIR="$(pwd)/dist"

LAYER_DIR=$OUTPUT_DIR/layers/lambda

mkdir -p $LAYER_DIR

cp -LR node_modules $LAYER_DIR

cd LAYER_DIR/..

zip -r layers.zip lambda