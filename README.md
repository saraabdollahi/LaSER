# LaSER
Here, LaSER takes a query entity and a language as input and recommends a language-specific ranking of events as output using:

To do so, it uses:

* ### Candidate Generation: given a query entity and using an embedding model, it creates a set of candidate events.
* ### Feature Extraction: Here we extract individual and pair features for candidate events.
* ### Ranker: And finally, using the trained LTR model, the candidate events are ranked and top events are suggested.
