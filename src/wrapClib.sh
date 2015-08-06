#!/usr/bin/env bash
java -jar ../lib/jnaerator.jar main/cpp/clib.h -v -noJar -noComp -package main.java  -f -convertBodies -forceNames -runtime BridJ
rm _jnaerator.*