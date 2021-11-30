# Download EventKG files
wget -O eventkg_output_light.tar.gz https://zenodo.org/record/4720078/files/eventkg_v3_3_output_light.tar.gz?download=1
tar -xf eventkg_output_light.tar.gz

# Extract coordinates
grep '<http://schema.org/l' data/output_light/relations_entity_base.nt > entity_coordinates_raw.nt
grep '<http://schema.org/l' data/output_light/relations_event_base.nt > event_coordinates_raw.nt
cat event_coordinates_raw.nt entity_coordinates_raw.nt > base_coordinates.nt
rm entity_coordinates_raw.nt
rm event_coordinates_raw.nt

grep 'http://semanticweb.cs.vu.nl/2009/11/sem/hasPlace' data/output_light/relations_event_base.nt > event_places.nt


sed -i 's/<http:\/\/eventKG.l3s.uni-hannover.de\/resource\///g ; s/> <http:\/\/schema.org\// /g ; s/> "/ /g ; s/"^^<http:\/\/www.w3.org\/2001\/XMLSchema#double> .//g' base_coordinates.nt
mv base_coordinates.nt base_coordinates.csv

sed -i 's/> <http:\/\/semanticweb.cs.vu.nl\/2009\/11\/sem\/hasPlace> <http:\/\/eventKG.l3s.uni-hannover.de\/resource\// /g ; s/<http:\/\/eventKG.l3s.uni-hannover.de\/resource\///g ; s/> .//g' event_places.nt
mv event_places.nt event_places.csv

grep 'http://www.w3.org/2002/07/owl#sameAs> <http://www.wikidata.org/' data/output_light/events.nt > events_same_as.nt
grep 'http://www.w3.org/2002/07/owl#sameAs> <http://www.wikidata.org/' data/output_light/entities.nt > entities_same_as.nt
cat events_same_as.nt entities_same_as.nt > same_as_wikidata.nt
rm events_same_as.nt
rm entities_same_as.nt

sed -i 's/<http:\/\/eventKG.l3s.uni-hannover.de\/resource\///g ; s/> <http:\/\/www.w3.org\/2002\/07\/owl#sameAs> <http:\/\/www.wikidata.org\/entity\// /g ; s/> .//g' same_as_wikidata.nt
mv same_as_wikidata.nt same_as_wikidata.tsv

grep 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://semanticweb.cs.vu.nl/2009/11/sem/Place' data/output_light/entities.nt > places.nt
sed -i 's/<http:\/\/eventKG.l3s.uni-hannover.de\/resource\///g ; s/> <http:\/\/www.w3.org\/1999\/02\/22-rdf-syntax-ns#type> <http:\/\/semanticweb.cs.vu.nl\/2009\/11\/sem\/Place> .//g' places.nt
mv places.nt places.csv
