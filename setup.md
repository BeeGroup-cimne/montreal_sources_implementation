# Install Neo4j

Follow the instruction in the [link](https://neo4j.com/docs/operations-manual/current/installation/linux/debian/#debian-installation)

Add in the `plugins` directory located at `/var/lib/neo4j/plugins`:
 - the neosemantics
 - the spatial
 - the apoc

if you face the error `NoSuchMethodError` with `apoc.convert.fromJsonList`, follow the instruction in the [link](https://github.com/neo4j-contrib/neo4j-apoc-procedures/issues/2861)

# Set up the database (first time)
- login and change the password.
- run in neo4j:
```cypher
CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;
```
# Set up the database (all the time after reset)
- run in neo4j:
```cypher
CALL n10s.graphconfig.init({ keepLangTag: true, handleMultival:"ARRAY", multivalPropList:["http://bigg-project.eu/ontology#kpiType","http://bigg-project.eu/ontology#shortName","http://www.w3.org/2000/01/rdf-schema#label", "http://www.w3.org/2000/01/rdf-schema#comment", "http://www.geonames.org/ontology#officialName"]});
CALL n10s.nsprefixes.add("schema","https://schema.org/");
CALL n10s.nsprefixes.add("qudt", "https://qudt.org/vocab/unit/");
CALL n10s.nsprefixes.add("vaem","http://www.linkedmodel.org/schema/vaem#");
CALL n10s.nsprefixes.add("s4city","https://saref.etsi.org/saref4city/");
CALL n10s.nsprefixes.add("owl","http://www.w3.org/2002/07/owl#");
CALL n10s.nsprefixes.add("s4bldg","https://saref.etsi.org/saref4bldg/");
CALL n10s.nsprefixes.add("gn","https://www.geonames.org/ontology#");
CALL n10s.nsprefixes.add("saref","https://saref.etsi.org/core/");
CALL n10s.nsprefixes.add("skos","http://www.w3.org/2004/02/skos/core#");
CALL n10s.nsprefixes.add("bigg","http://bigg-project.eu/ontology#");
CALL n10s.nsprefixes.add("rdfs","http://www.w3.org/2000/01/rdf-schema#");
CALL n10s.nsprefixes.add("purl","http://purl.org/dc/terms/");
CALL n10s.nsprefixes.add("vcard","http://www.w3.org/2006/vcard/ns#");
CALL n10s.nsprefixes.add("ssn","http://www.w3.org/ns/ssn/");
CALL n10s.nsprefixes.add("geo","http://www.w3.org/2003/01/geo/wgs84_pos#");
CALL n10s.nsprefixes.add("rdf","http://www.w3.org/1999/02/22-rdf-syntax-ns#");
CALL n10s.nsprefixes.add("geosp","http://www.opengis.net/ont/geosparql#");
CALL n10s.nsprefixes.add("s4syst","https://saref.etsi.org/saref4syst/");
CALL n10s.nsprefixes.add("s4agri","https://saref.etsi.org/saref4agri/");
CALL n10s.nsprefixes.add("time","http://www.w3.org/2006/time#");
CALL n10s.nsprefixes.add("foaf","http://xmlns.com/foaf/0.1/");

```
* add other namespaces if required.
