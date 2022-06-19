import time

from germanetpy.germanet import Germanet
from germanetpy.synset import Synset, WordClass, WordCategory

from word_relatedness.word_relation import WordRelation


def ex1():
    """

        Experiment: Graph for root length to count in germanet

        The number of elements that have a specific amount of words to the root compared to those of all other

        """

    germanet_file = str(__file__)[
                    0:str(__file__).rindex("word_relatedness")] + "germanet_data/germanet/GN_V160/GN_V160_XML"
    germanet = Germanet(germanet_file)
    gnroot: Synset = germanet.root
    print(gnroot.lexunits)

    save: dict = {}
    last: dict = {}

    def ix(ss: Synset, val):
        if len(ss.direct_hyponyms) == 0:
            if last.keys().__contains__(val):
                last[val] += 1
            else:
                last[val] = 1
        lsd = ss.direct_hyponyms
        if save.keys().__contains__(val):
            save[val] += len(lsd)
        else:
            save[val] = len(lsd)
        for hy in lsd:
            hy: Synset = hy
            if hy.word_category == WordCategory.nomen:
                ix(hy, val + 1)

    ix(gnroot, 0)
    """ print(save)
   
   for 5
   
    test5 = 0
    for key, value in save.items():
        if key >= 5:
            test5 += value

    print(test5)"""



    """
    the method above is iterating over the complete germanet spec of nouns
    it will send each new layer's length to the save dict

    """

    print(save)
    total = 0
    for k, v in save.items():
        total += v
    print(total)
    dx = {}
    for k, v in save.items():
        dx[k] = v / total
    print(dx)

    for way in range(39):
        start_x = way - 19
        if start_x < 0:
            start_x = 0
        if start_x <= 19 and way - start_x <= 19:
            lx = [start_x]
            ly = [way - start_x]
            while lx[-1] < way and lx[-1] < 19:
                lx.append(lx[-1] + 1)
                ly.append(way - lx[-1])
            total5 = 0
            """
            ex3:
            take only last half
            """
            print(lx)
            for g in lx:
                for key, value in save.items():
                    if key >= g and key == way:
                        total5 += value
                    elif key >= g:
                        total5 += value * dx[key]
            print(way)
            print(str(total5).replace(".", ","))

        else:
            print(0)

    """print(last)
    save2 = {}
    for i in last.keys().__iter__():
        save2[i] = save[i] - last[i]
    print(save2)"""


if __name__ == '__main__':

    germanet_file = str(__file__)[
                    0:str(__file__).rindex("word_relatedness")] + "germanet_data/germanet/GN_V160/GN_V160_XML"
    germanet = Germanet(germanet_file)
    gnroot: Synset = germanet.root

    # rel = WordRelation("Sand", "Teppich", germanet.get_synsets_by_orthform("Sand")[0], germanet.get_synsets_by_orthform("Teppich")[0], None)
    # print(rel.calculate_relation())


    # exit(1)
    """
    x + y = way
    38>= way >= 0
    
    19>=x>=0
    19>=y>=0 
    
    calculate number of possibilities of x and y that equal (after addition) way
    """

    ex1()
    exit(1)

    x = 0
    y = 0

    for way in range(39):
        start_x = way - 19
        if start_x < 0:
            start_x = 0
        if start_x <= 19 and way - start_x <= 19:
            lx = [start_x]
            ly = [way - start_x]
            while lx[-1] < way and lx[-1] < 19:
                lx.append(lx[-1] + 1)
                ly.append(way - lx[-1])
            print(lx)
            print(ly)
            print(len(lx))
        else:
            print(0)
    """
    + 
    """


## old !
def semantic_distance_with_raster(s0: Synset, s1: Synset):
    path_len = s0.shortest_path_distance(s1)
    raster: list = [
        1.0,
        0.987708,
        0.974733,
        0.954862,
        0.925482,
        0.882317,
        0.824512,
        0.755922,
        0.680006,
        0.602665,
        0.531854,
        0.470320,
        0.414220,
        0.365897,
        0.324850,
        0.286456,
        0.249496,
        0.213358,
        0.177132,
        0.141854,
        0.110697,
        0.083603,
        0.060573,
        0.041605,
        0.026676,
        0.015687,
        0.008311,
        0.003894,
        0.001606,
        0.000596,
        0.000194,
        0.000049,
        0.000011,
        0.000003,
        0.000001,
        0.000000,
        0.000000,
        0.000000,
        0.000000
    ]
    return raster[path_len]
