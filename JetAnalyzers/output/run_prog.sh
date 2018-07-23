#!/bin/bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH_STORED
set -xe
$@
