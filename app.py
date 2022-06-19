# -*- coding:utf-8 -*-
import mechanics.instruments as instruments
import json
from flask import *
import os

germanet = None
relatedness = None
spacy = None
test = None


app = Flask(__name__)


@app.route('/')
def put():
    """
    the main method that will be called from the app framework
    - load args
    - generate objects
    - start Test values
    """

    """
    secure:
    "sCP4ce&dhTJ4qQ##b#xMTGxwSFqeCa"
    as CTR
    """
    """if request.json['key'] != os.getenv('CTR'):
        return "x", 403"""

    test_id = request.args.get('test_id', default=-1, type=int)
    method = request.args.get("method", default=0, type=int)
    input_data = json.loads(request.args.get("input_data", default=None, type=str))

    global test, germanet, relatedness, spacy
    if g.get("germanet"):
        germanet = g.germanet
        relatedness = g.relatedness
        spacy = g.spacy
        test = g.test

    if not test and instruments.test_exists():
        test = instruments.test_from_str()
    elif not test:
        test = instruments.Test()

    output = test.put(test_id, method, input_data)

    g.germanet = germanet
    g.relatedness = relatedness
    g.spacy = spacy
    g.test = test

    test.save()

    return output, 200


def check():
    put(-1, 0, None)
    x1, x2 = json.loads(put(0, 0, ["Schrank", "Zeit", "Raum", "Religion", "Start", "Schule", "Radio"]))[3]
    x3 = []
    for xx in x1:
        x3.append(xx[0])
    put(0, 1, (x3, x2))
    x3 = put(1, 0, x2)
    x4 = {
        x3[0]: ["Zeit", "Geld", "Uhr", "Auto"],
        x3[1]: ["Maschine", "Verganganeheit", "Versuch"],
        x3[2]: ["Frage", "Wissenschaft", "Lampe"]
    }
    put(1, 1, x4)
    put(2, 0, ["Die Zeit krümmt den Raum im Schrank", {"Zeit": "Religion", "Raum": "Radio", "Schrank": "Zeit"}])
    put(3, 0, ["Ich frage eine andere Person", "Ich übersetze das Wort", "Ich zeige es durch Pantomime"])
    put(3, 1, ["Ich frage eine andere Person", "Ich übersetze das Wort", "Ich zeige es durch Pantomime"])
    put(3, 2, ["Ich frage eine andere Person", "Ich übersetze das Wort", "Ich zeige es durch Pantomime"])
    put(4, 0, [[("Auto", 500), ("Lastwagen", 500), ("Antrieb", 700), ("Maschine", 1000)],
               [("Auto", 500), ("Lastwagen", 500), ("Antrieb", 700), ("Maschine", 1000)],
               [("Auto", 500), ("Lastwagen", 500), ("Antrieb", 700), ("Maschine", 1000)]])
    put(5, 0, "Ich fahre durch Nacht und Wind.\nUnd sehe den Vater mit seinem Kind.")
    put(6, 0, 0)


if __name__ == '__main__':
    app.run(port=24232)
