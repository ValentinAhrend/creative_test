import math

from germanetpy.germanet import Germanet

from word_relatedness.experiment import semantic_distance_with_raster


def germanet_small_experiment(wordA: str, wordB: str):
    distances = []
    sA: list = germanet.get_synsets_by_orthform(wordA)
    sB: list = germanet.get_synsets_by_orthform(wordB)
    for sAA in sA:
        for sBB in sB:
            distances.append(math.sqrt(semantic_distance_with_raster(sAA, sBB)))
    return distances


if __name__ == '__main__':

    germanet_file = str(__file__)[
                    0:str(__file__).rindex("word_relatedness")] + "germanet_data/germanet/GN_V160/GN_V160_XML"
    germanet = Germanet(germanet_file)

    """
    small_germanet experiment

    """

    """
    i(0): selbiges Wort, Ergebnis sollte den maximalen Wert für Zusammenhang in allen Fällen geben
        --> Die Werte sind nicht alle maximal, da es verschiedene Bedeutungen zu 'Katze' gibt, 
        die verschieden interpretiert werden können.
    """
    distances = germanet_small_experiment(wordA="Katze", wordB="Katze")
    # print(distances)

    """
    i(1): wiederholung von i(0), allerdings wird nun auch der Durchschnitt aus allen Distanzen erzeugt.
        --> Der Median liegt bei 0.7755 (ungefähr) und ist damit weit von der Erwartung entfernt. 
    """
    median = sum(distances) / len(distances)
    # print(median)

    """
    Es ist nicht möglich die Erwartungen herzustellen, da man sonst vorallem richitge Antworten 
    also geringe Zusammenhänge stark beeinflusst
    
    i(2): zwei Wörter mit einem großen Zusammenhang [ENGLISH=20/200]
        --> Durchschnitt leigt bei 0.69754, Erwartung: hoher Zusammenhang
    """
    distances = germanet_small_experiment(wordA="Katze", wordB="Hund")
    median = sum(distances) / len(distances)
    # print(distances, median)

    """
    i(3): um die Erwartung zu erfüllen und den richtigen Wert zu erhalten, kann man den Maximal-Wert 
    der Liste als Ausgabe verwenden
    """
    output = max(distances)
    # print(output)

    """
    i(4) gilt dies auch für geringe Zusammenhänge? 
    --> Es kommen hier mittlere Werte heraus.
    """
    distances = germanet_small_experiment(wordA="Katze", wordB="Regenbogen")
    print(max(distances), min(distances))
    distances = germanet_small_experiment(wordA="Katze", wordB="Physik")
    print(max(distances), min(distances))
    distances = germanet_small_experiment(wordA="Katze", wordB="Periodensystem")
    print(max(distances), min(distances))

    """Bei geringen Zusammenhängen sind die geringen Werte und bei hohen Zusammenhängen die hohen Werte besser "
    "geeigent, welche Bedeutung nun benutzt wird, muss für das optimale Ergebnis vom Benutzer bestimmt werden."""

