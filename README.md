# thingernet-graph
Python script to generate neo4j Cypher representation of a collection of IoT devices for visualisation and query.

The script reads a directory of JSON files describing 'things' and creates the
relevant neo4j cypher text for import to neo4j in order to produce a graph 
database representation of the 'thingernet' - a directed graph with node and edge
properties that allow us to reason about, and appraise the security of thingernets.

An accompanying NCC Group whitepaper describes the rationale and use of thingernet-graph.
