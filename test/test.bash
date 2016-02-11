#!/bin/bash -exv

set -o pipefail

###TEST1: nodes are running or not###
rosnode list		|
grep '^/buzzer$'
