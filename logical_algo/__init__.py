"""
THE LOGIC AI SCRIPT

--- Author: Valentin Ahrend ---

A contextual logic ai validation

--- SETUP ---

(1) Input: Sentence

(2) Generate a SentenceScheme for the input

(3) Generate LogicPairs for the SentenceScheme

(4) Send LogicPairs into LogicPair Indexer

(6) LogicPair Indexer mix LogicPairs with the ContextScheme

(5) LogicPair Indexer compares the LogicPairs via the LogicComparator

(6) LogicComparator returns the best matching LogicField

(7) LogicField is executed on the main LogicPairs

(8) LogicField returns the LogicState value as a final product

--- AI ---

Is the Logic AI a real Intelligence ?

- Not it isn't, because the Process of validating Logic includes a variety of Algorithms.
  What the Script does, it puts a Logical-Idea generated via an Algorithm over an Input Sentence.
  This Logical-Idea gets compared to many other Logical-Ideas and the abstract forms inside the Logical-Idea gets
  compared too.

- You could call this an AI, because it is able to learn. It is generating new LogicCombinations each time a LogicField
  is returned. So there is a learning aspect inside this machine.

--- Example ---

(1) 'Lisa isst gerne Äpfel'

(2) generating a SentenceScheme via Internet and collected Data:
{
  "S": {
    "data": "Lisa",
    "type": "NA",
    "data_head0": {
      "asz-0": [
        "Frau",
        "Person"
      ],
      "asz-1": [
        "weiblich"
      ],
      "top-0": [
        "Vorname"
      ]
    },
    "id": "HASH_ID"
  },
  "P": {
    "data": "isst",
    "type": "V",
    "data_head0": "essen",
    "data_head1": "current",
    "id": "7294873947239847"
  },
  "ADV-P": {
    "data": "gerne",
    "type": "ADV",
    "data_head0": "positive",
    "data_head1": [
      "0",
      [
        "7294873947239847"
      ]
    ],
    "id": "152345394927643"
  },
  "OBJ-AKK": {
    "data": "Äpfel",
    "type": "N",
    "data_head0": "Apfel",
    "data_head1": {
      "asz-0": [
        "Baum"
      ],
      "asz-1": [
        "rot"
      ],
      "top-0": [
        "Frucht",
        "Essen"
      ]
    }
  }
} lookup ./example.json

For this setup a Platform is needed, for lexical storage and word analysis
...This is the LingualPlatform



"""