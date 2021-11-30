# LaSER: Data extraction from EventKG

LaSER requires input data from the [EventKG knowledge graph](https://eventkg.l3s.uni-hannover.de/).
In this 

Specifically, the three following types of information for all entities (including events) are required:
1. Coordinates
2. Happening/Existence times (i.e., start dates and end dates)
3. Link counts

## Instructions

First, run
```sh
sh eventkg_data_download_and_extraction.sh
```
to download, extract and process the original EventKG files. This will require up to 75GB disk space.
This will create a `data` folder in your current directory, as well as the files `places.csv`, `event_places.csv`, `base_coordinates.csv` and `same_as_wikidata.tsv`.

### Coordinates

Then, export a jar file `CoordinatesPerEntityExtractor.jar` from the Java class `de.l3s.cleopatra.laser.coordinates.CoordinatesPerEntityExtractor` and run in the current directory:

```sh
java -jar CoordinatesPerEntityExtractor.jar
```

This will create a file `coordinates_all.csv` and a file `stats.csv`.

### Happening/Existence times

Happening/Existence times that are required to train and run LaSER are contained in the files `data/output_light/relations_entity_base.nq` and `data/output_light/relations_event_base.nq`.

### Link counts
Use the Dumper described of [EventKG](https://github.com/sgottsch/eventkg) in the required languages to extract link counts. 