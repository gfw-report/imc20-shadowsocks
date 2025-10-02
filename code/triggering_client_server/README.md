# README

This directory includes the source code of the triggering clients and sink/responding servers used in Section 4.1.

## Exp1a: high entropy, sink server

length(bytes): 1 to 1000
entropy: > 7

server: sfo1
client: bj3-new

## Exp1b: high entropy, responding server

length(bytes): 1 to 1000
entropy: > 7

server: sfo1
client: bj3-new

## Exp2: low entropy

length(bytes): 1 to 1000
entropy: < 2

server: sfo2
client: bj4-new

## Exp3: varied length and entropy

length(bytes): 1 to 2000
entropy: [0,8]

server: sfo3
client: bj5-new
