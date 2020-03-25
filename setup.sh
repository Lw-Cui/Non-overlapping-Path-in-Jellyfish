#!/bin/sh

mkdir pickled_routes
mkdir plots
mkdir results
mkdir transformed_routes
cd ripl && python setup.py install
cd ../
cd riplpox && python setup.py install
cd ../
