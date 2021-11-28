# LaSER
Here, LaSER takes a query entity and a language as input and recommends a language-specific ranking of events as output using:

* #### Candidate Generation
      Given a query entity and using an embedding model, candidate_generation.py creates a set of candidate events.
* #### Feature Extraction
      feature_extraction.py returns individual and pair features for candidate events.
* #### Ranker: 
      Using training dataset, LTR_training.py trains a ranker which would finally be used on extracted features of candidate events to rank candidates.
    
    
## License
Distributed under the MIT License. See LICENSE for more information.


