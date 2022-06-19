import requests
import statistics
import time
import random
import json
import math
import pyphen
import enchant

'''REIMSCHEMA-TYPUS FUNKTIONEN'''

before = ""
dic = pyphen.Pyphen(lang='de_DE')

def has_vocals(word) -> bool:
    for w in word:
        w = str(w).lower()
        if w == 'a' or w == 'e' or w == 'o' or w == 'i' or w == 'u' or w == 'ö' or w == 'ü' or w == 'ä':
            return True
    return False


def load_rhymes(word, language):
    # print("get word_ " + word)

    global before
    if before == word:
        return None
    before = word
    url = "https://de.wiktionary.org/wiki/" + word

    content = requests.get(url)

    # wikitionary daten laden

    connected = False

    while content.status_code == 404:
        url = 'https://de.wiktionary.org/w/index.php?search=' + word + '&title=Spezial:Suche&go=Seite&ns0=1'
        content = requests.get(url)

        if not content.url.__contains__('index.php?search='):
            return load_rhymes(content.url[content.url.rfind("/") + 1:], language)

        # url wurde nicht gefunden, suche nach dem Wort wird gestartet

        q0 = "<div class='mw-search-result-heading'><a href=\""

        if not content.text.__contains__(q0):
            connected = True
            # die Suche ist erfolglos, da es keine Ergebnisse gibt
            break

        index0 = content.text.index(q0)
        index1 = content.text.index('" title', index0 + len(q0))

        part = content.text[index0 + len(q0):index1]
        return load_rhymes(part, language)
        # das ergebniss wird nun erneut gesucht

    q1 = '<dd><a href="/wiki/Hilfe:Reime" title="Hilfe:Reime">Reime:</a> <span class="ipa" style="padding: 0 1px; text-decoration: none;">'
    q2 = 'title="Reim:Deutsch:'

    while not content.text.__contains__(q1) or connected:
        q3 = '<a href="/wiki/Determinativkompositum" title="Determinativkompositum">Determinativkompositum</a>'
        # der Begriff Reim ist nicht in der Html-Datei enthalten

        if not content.text.__contains__(q3):
            q6 = '<p style="margin-bottom:-0.5em; font-weight:bold;" title="Etymologie und Morphologie">Herkunft:</p>'
            # das Wort ist kein Zusammengesetztes Nomen, es erfolgt die Suche in www.dwds.de
            if not content.text.__contains__(q6):

                #     print("es gibt keine Resource. Eine weitere bibliothek wird mit einbezogen")
                url_dwds = 'https://www.dwds.de/?q=' + word
                content = requests.get(url_dwds)
                q9 = '<span class="dwdswb-ft-blocklabel serif italic">Wortzerlegung'

                # die Wortzerlegung wird gesucht, um den letzten Teil des Wortes zu finden

                if content.text.__contains__(q9):
                    index0 = content.text.index(q9) + len(q9)
                    index1 = content.text.index('</a></span>', index0)
                    element_xy = content.text[index0:index1]

                    #   print(element_xy)

                    # print("?---" + word)

                    word = element_xy[element_xy.rfind('">') + 2:]

                    # print("!---" + word)

                    # get last completion
                    changed = False
                    for cc_e in range(len(word) - 1):
                        rf = word[0:len(word) - cc_e]
                        if before.__contains__(rf):
                            word = rf
                            changed = True
                            break
                        elif before.__contains__(rf.lower()):
                            word = rf.lower()
                            changed = True
                            break

                    # print(word + "/" + changed.__str__())

                    if not has_vocals(word):
                        '''syllables are not found, now using pyphen'''
                        syllables = dic.inserted(word)
                        # print(syllables)

                        '''Putting x syllables together, to form a word. The last word that gets detected
                        by wikitionary as a word, will be replaced by "" and then the loop continues as 
                        long as there are any elements over (that form a legal word)'''

                        we = ""
                        wu_ = []

                        for sy in syllables:
                            if sy == '-':
                                continue
                            we += sy
                            if len(we) > 2: # d.check(we) or d.check(we.capitalize()))
                                wu_.append(we)
                                we = ""

                        # print(wu_)

                        if len(wu_) > 0 and word.endswith(wu_[-1]):
                            return load_rhymes(wu_[-1], language)
                        else:
                            return time.time_ns().__str__()

                    if changed:

                        if before.rfind(word) + word.__len__() is not before.__len__():
                            return load_rhymes((word + before[before.rfind(word) + word.__len__()]).capitalize(), 'de')
                        else:
                            return load_rhymes(word.capitalize(), 'de')
                    else:
                        return time.time_ns().__str__()

                else:
                    '''syllables are not found, now using pyphen'''
                    syllables = dic.inserted(word)
                    # print(syllables)

                    '''Putting x syllables together, to form a word. The last word that gets detected
                    by wikitionary as a word, will be replaced by "" and then the loop continues as 
                    long as there are any elements over (that form a legal word)'''

                    we = ""
                    wu_ = []

                    for sy in syllables:
                        if sy == '-':
                            continue
                        we = we + sy
                        # print(we + "?")
                        if len(we) > 2: # d.check(we) or d.check(we.capitalize()))
                            # print("dic found " + we)
                            wu_.append(we)
                            we = ""

                    # print(wu_)

                    if wu_ != [] and len(wu_[-1]) > 2 and word.endswith(wu_[-1]):
                        return load_rhymes(wu_[-1], language)
                    else:
                        return time.time_ns().__str__()
            else:
                index0 = content.text.index(q6)
                q7 = '</a></i></dd></dl>'
                if not content.text.__contains__(q7) or content.text.index(q7) < index0:
                    return time.time_ns().__str__()
                else:
                    #  print(content.text)
                    index1 = content.text.index(q7, index0 + len(q6))
                    pr = content.text[index0 + len(q6):index1]
                    pr = pr[pr.rfind('>') + 1:]
                    if pr.startswith("-"):
                        url = "https://de.wiktionary.org/wiki/" + pr
                        content = requests.get(url)
                        q8 = '<span class="ipa" style="padding: 0 1px; text-decoration: none;">'
                        index0 = content.text.index(q8) + len(q8)
                        index1 = content.text.index('</span>', index0)
                        ipa = content.text[index0:index1]

                        # print("returning correct ipa")

                        return ipa[:-1]
                    else:
                        return time.time_ns().__str__()

        index0 = content.text.index(q3)
        # print(content.url)

        if content.text.__contains__('</dd></dl>') and content.text.rfind('</dd></dl>') >= index0 + len(q3):
            index1 = content.text.index('</dd></dl>', index0 + len(q3))
            part = content.text[index0 + len(q3):index1]
            q5 = '</a></i>'
            print(part)
            index0 = part.index(q5)
            index1 = 0
            if not part[index0 + len(q5):].__contains__(q5):
                index1 = part.index("</i></dd>", index0 + len(q5))
                index1 = part[index0:index1].rfind("</a>")
            else:
                index1 = part.index(q5, index0 + len(q5))
            part = part[index0:index1]
            part = part[part.index('">') + 2:len(part)]
            url = "https://" + language + ".wiktionary.org/wiki/" + part
            content = requests.get(url)

            # print(url + "!!")
        else:
            return time.time_ns().__str__()
    index0 = content.text.index(q1)
    index1 = content.text.index("</span></dd>", index0 + len(q1))
    ry = content.text[index0 + len(q1):index1]
    ry = ry[ry.rfind("-") + 1: ry.rfind("</a>")]

    return ry


def nummer_string(num) -> str:
    ral = num
    num = str(num)[::-1]
    count = 0
    while num[0] == "0":
        num = num[1:]
        count += 1
    if count == 0:
        # example: 17 -> 71
        # count = 0
        # match = "1"
        # return 7 + zehn

        # example: 1 -> 1
        # count = 0
        # return eins

        if len(num) > 1:
            match = num[1]
            if match == "1":
                return ns_match(num[0], False, True)
            else:
                return ns_match(match, False, False)
        else:
            return ns_match(num[0], True, False)
    elif count == 1:
        return ns_match(num[0], False, False)
    elif count >= 2:
        return nr_match(count, num[0] == "1" and (len(ral) - 1) % 3 == 0)


def ns_match(match, basic, basic_):
    if basic:
        if match == "0":
            return "null"
        elif match == "1":
            return "eins"
        elif match == "2":
            return "zwei"
        elif match == "3":
            return "drei"
        elif match == "4":
            return "vier"
        elif match == "5":
            return "fünf"
        elif match == "6":
            return "sechs"
        elif match == "7":
            return "sieben"
        elif match == "8":
            return "acht"
        elif match == "9":
            return "neun"
    else:
        if basic_:
            if match == "0":
                return "zehn"
            elif match == "1":
                return "elf"
            elif match == "2":
                return "zwölf"
            else:
                return match + "zehn"
        else:
            if match == "2":
                return "zwanzig"
            else:
                return ns_match(match, True, False) + "zig"


def nr_match(null_count, first):
    if null_count == 2:
        return "hundert"
    elif int(null_count / 3) == 1:
        return "tausend"
    elif int(null_count / 3) % 2 == 0:
        if first:
            return "million"
        else:
            return "millionen"
    else:
        if first:
            return "milliarde"
        else:
            return "milliarden"


ry_sub = []
one_note = []
used_word = []
rz = []
ending_super = []


def reimschema_typus(text):
    global ry_sub
    global one_note
    global used_word
    global rz
    global ending_super

    ry_sub = []
    one_note = []
    rz = []
    used_word = []
    ending_super = []
    lines = str(text).split("\n")
    endings = []
    words = []
    lengths = []
    for lx in lines:
        if lx is not None:
            exl = str(lx).split(" ")
            srr = exl[-1]
            lengths.append(len(exl))
            count_a = 1
            while not (srr[-1:].upper() != srr[-1:].lower() or srr[-1:] == "ß" or srr[-1:].isnumeric()):
                srr = srr[:-1]
                if len(srr) == 0:
                    break

            while not (srr[-1:].upper() != srr[-1:].lower() or srr[-1:] == "ß" or srr[-1:].isnumeric()):
                print("loop" + str(srr))
                if srr is None or len(srr) == 0:
                    break
                srr = exl[-1 - count_a]
                while not (
                        srr[-1:].upper() != srr[-1:].lower() or srr[-1:] == "ß" or srr[-1:].isnumeric() or srr == ""):
                    print(srr)
                    print("??")
                    srr = srr[:-1]
                count_a += 1
            if srr is None or len(srr) == 0:
                print("continue")
                continue
            if str(srr).isnumeric():
                srr = nummer_string(srr)

            while not (srr[-1:].upper() != srr[-1:].lower() or srr[-1:] == "ß" or srr[-1:].isnumeric()):
                srr = srr[:-1]

            loaded = load_rhymes(srr, 'de')
            # print("->" + loaded + " / " + srr)
            if loaded is None or str(loaded).isnumeric():
                loaded = random.random().__str__()
            words.append(srr)
            endings.append(loaded)

    l_oo = statistics.mean(lengths).__round__(3)
    ry = []
    count = 0
    ending_super = endings

    print("endings: " + str(endings))

    for end in endings:
        if end is None:
            count += 1
            continue
        count0 = 0
        for end_ in endings:
            if end_ is None:
                count0 += 1
                continue
            # if one_note.__contains__(count0):
            #    count0 += 1
            #    continue
            if count != count0 and end == end_ and not ry.__contains__((count0, count)):
                ry.append((count, count0))
                if count0 - count == 1:
                    rz_0 = (end, end_)
                    rz_1 = (count, count0)
                    rz_2 = (words[count], words[count0])
                    # check if pair is extended
                    cr = 1
                    while True:
                        if count0 + cr < len(endings) and endings[count0 + cr] == end_:
                            rz_0 = rz_0 + (endings[count0 + cr],)
                            rz_1 = rz_1 + (count0 + cr,)
                            rz_2 = rz_2 + (words[count0 + cr],)
                        else:
                            if count0 + cr >= len(endings):
                                break
                        cr += 1

                    pair_l = 1
                    cc_0 = 0
                    for rz_1_ in rz_1:
                        if cc_0 != 0:
                            pair_l += rz_1_ - rz_1[cc_0 - 1]
                        cc_0 += 1

                    rz_ = ['PAIR' + str(cc_0), rz_0, rz_1, rz_2]
                    contain = False
                    for rr in rz:
                        if list_ends_with(list(rr[2]), list(rz_[2])):
                            contain = True
                            break
                    if not contain:
                        for rr in ry_sub:
                            if list_ends_with(list(rr[2]), list(rz_[2])):
                                contain = True
                                break
                    used_word_0 = used_word.copy()
                    if not contain:
                        count2_ = 0
                        for rz_2_ in rz_2:
                            if used_word_0.__contains__(rz_2_):
                                if count2_ > 1:
                                    rz_0 = rz_0[0:count2_]
                                    rz_1 = rz_1[0:count2_]
                                    rz_2 = rz_2[0:count2_]
                                    rz_ = ['PAIR', rz_0, rz_1, rz_2]
                                    break
                                contain = True
                                break
                            else:
                                used_word_0.append(rz_2_)
                            count2_ += 1
                    if not contain:
                        used_word = used_word_0.copy()
                        rz.append(rz_)
                        for fz in rz_1:
                            one_note.append(fz)
                        ry_sub.append(rz_)
                elif count0 - count == 2:
                    between = max([count, count0]) - 1
                    if between + 2 < len(endings) and endings[between] == endings[between + 2]:
                        cc = 1
                        re = [(end, end_), (endings[between], endings[between + 2])]
                        rx = [(count, count0), (between, between + 2)]
                        rf = [(words[count], words[count0]), (words[between], words[between + 2])]
                        while True:
                            n0 = between + 2 + cc
                            if (n0 < len(endings) and endings[n0] == endings[n0 - 2]) and \
                                    endings[n0] != endings[n0 - 1]:
                                re.append((endings[n0 - 2], endings[n0]))
                                rx.append((n0 - 2, n0))
                                rf.append((words[n0 - 2], words[n0]))
                            else:
                                break
                            cc += 1
                        if cc >= 1:

                            end_a = re[-1][1]
                            end_b = re[-1][0]

                            rz_ = ["CROSS", re, rx, rf]
                            contain = False
                            for rr in rz:
                                if rr[2] == rz_[2]:
                                    contain = True
                                    break
                            if not contain:
                                for rr in ry_sub:
                                    if rr[2] == rz_[2]:
                                        contain = True
                                        break
                            e_contain = False
                            e = []
                            used_word_ = used_word.copy()
                            if not contain:
                                c_count = 0
                                for rf_ in rf:
                                    c_count1 = 0
                                    for rf__ in rf_:
                                        if used_word_.__contains__(rf__):
                                            e_contain = True
                                            e.append(c_count + c_count1 * 2)
                                            break
                                        else:
                                            used_word_.append(rf__)
                                        c_count1 += 1
                                    c_count += 1
                            if e_contain:
                                xx = load_tz_inner(endings[count:count + 4 + (cc - 1) * 2], count, words, e, False,
                                                   used_word.copy(),
                                                   [])
                                ry = xx[0]
                                used_word = xx[1]
                                rz.extend(ry)
                            elif not contain:
                                used_word = used_word_.copy()
                                for fz in rx:
                                    one_note.append(fz[0])
                                    one_note.append(fz[1])
                                rz.append(rz_)
                                ry_sub.append(rz_)
                    else:
                        rz_0 = (end, end_)
                        rz_1 = (count, count0)
                        rz_2 = (words[count], words[count0])
                        # check if pair is extended
                        cr = 1
                        while True:
                            if count0 + cr < len(endings) and endings[count0 + cr] == end_:
                                rz_0 = rz_0 + (endings[count0 + cr],)
                                rz_1 = rz_1 + (count0 + cr,)
                                rz_2 = rz_2 + (words[count0 + cr],)
                            else:
                                if count0 + cr >= len(endings):
                                    break
                            cr += 1
                        pair_l = 1
                        cc_0 = 0
                        for rz_1_ in rz_1:
                            if cc_0 != 0:
                                pair_l += rz_1_ - rz_1[cc_0 - 1]
                            cc_0 += 1

                        rz_ = ['PAIR' + str(cc_0), rz_0, rz_1, rz_2]
                        contain = False
                        for rr in rz:
                            if list_ends_with(list(rr[2]), list(rz_[2])):
                                contain = True
                                break
                        if not contain:
                            for rr in ry_sub:
                                if list_ends_with(list(rr[2]), list(rz_[2])):
                                    contain = True
                                    break
                        used_word_0 = used_word.copy()
                        if not contain:
                            count2_ = 0
                            for rz_2_ in rz_2:
                                if used_word_0.__contains__(rz_2_):
                                    if count2_ > 1:
                                        rz_0 = rz_0[0:count2_]
                                        rz_1 = rz_1[0:count2_]
                                        rz_2 = rz_2[0:count2_]
                                        pair_l = 1
                                        cc_0 = 0
                                        for rz_1_ in rz_1:
                                            if cc_0 != 0:
                                                pair_l += rz_1_ - rz_1[cc_0 - 1]
                                            cc_0 += 1

                                        rz_ = ['PAIR' + str(cc_0), rz_0, rz_1, rz_2]
                                        break
                                    contain = True
                                    break
                                else:
                                    used_word_0.append(rz_2_)
                                count2_ += 1
                        if not contain:
                            used_word = used_word_0.copy()
                            rz.append(rz_)
                            for fz in rz_1:
                                one_note.append(fz)
                            ry_sub.append(rz_)
                elif count0 - count >= 3:

                    if endings[count] != endings[count + 1]:
                        confirm = 0
                        if not used_word.__contains__(words[count]):
                            used_word.append(words[count])
                            confirm += 1
                        if not used_word.__contains__(words[count0]):
                            used_word.append(words[count0])
                            confirm += 1

                        if confirm == 2:
                            uw = used_word.copy()
                            on = one_note.copy()

                            xx = load_tz_inner(endings[count + 1:count0], count + 1, words, [], False, used_word.copy(),
                                               [])
                            ry_ = xx[0]
                            used_word = xx[1]
                            # PAIR CONNECTION

                            rz_0 = (end, end_)
                            rz_1 = (count, count0)
                            rz_2 = (words[count], words[count0])
                            # check if pair is extended
                            cr = 1
                            while True:
                                if count0 + cr < len(endings) and endings[count0 + cr] == end_:
                                    rz_0 = rz_0 + (endings[count0 + cr],)
                                    rz_1 = rz_1 + (count0 + cr,)
                                    rz_2 = rz_2 + (words[count0 + cr],)
                                else:
                                    if count0 + cr >= len(endings):
                                        break
                                cr += 1
                            pair_l = 1
                            cc_0 = 0
                            for rz_1_ in rz_1:
                                if cc_0 != 0:
                                    pair_l += rz_1_ - rz_1[cc_0 - 1]
                                cc_0 += 1

                            rz_ = ['BOUND' + str(cc_0), rz_0, rz_1, rz_2, ry_]
                            contain = False
                            for rr in rz:
                                if list_ends_with(list(rr[2]), list(rz_[2])):
                                    contain = True
                                    break
                            if not contain:
                                for rr in ry_sub:
                                    if list_ends_with(list(rr[2]), list(rz_[2])):
                                        contain = True
                                        break
                            used_word_0 = used_word.copy()
                            if not contain:
                                count2_ = 0
                                for rz_2_ in rz_2:
                                    if used_word_0.__contains__(rz_2_):
                                        if count2_ > 1:
                                            rz_0 = rz_0[0:count2_]
                                            rz_1 = rz_1[0:count2_]
                                            rz_2 = rz_2[0:count2_]
                                            rz_ = ['BOUND', rz_0, rz_1, rz_2, ry_]
                                            break
                                        contain = True
                                        break
                                    else:
                                        used_word_0.append(rz_2_)
                                    count2_ += 1

                            if not contain:
                                used_word = used_word_0.copy()

                            xx = load_tz_inner(endings[count + 1:], count + 1, words, [], True, uw, on)
                            ry_continued = xx[0]
                            uw = xx[1]
                            is_filled = False
                            fill_elements = []
                            for ry_element in ry_continued:
                                if not ry_.__contains__(ry_element):
                                    if ry_element[0].startswith('CROSS'):
                                        for tup in ry_element[2]:
                                            if not (tuple(tup)[0] > count0 and tuple(tup)[1] > count0):
                                                is_filled = True
                                                fill_elements.append(ry_element)
                                    elif ry_element[0].startswith("PAIR"):
                                        is_filled = ry_element[2][len(ry_element[2]) - 1] > count0
                                        if is_filled:
                                            fill_elements.append(ry_element)
                                    elif ry_element[0].startswith('BOUND'):
                                        is_filled = ry_element[2][1] > count0
                                        if is_filled:
                                            fill_elements.append(ry_element)
                            if is_filled:
                                rz_ = ["BOUND", (end, end_), (count, count0), (words[count], words[count0]), []]
                                if not ry_sub.__contains__(rz_):
                                    for fz in rz_1:
                                        one_note.append(fz)

                                    rz.append(rz_)

                                for fe in fill_elements:
                                    if fe[0] == 'CROSS':
                                        for fe_0 in fe[2]:
                                            one_note.append(fe_0[0])
                                            one_note.append(fe_0[1])
                                        contain = False
                                        if not contain:
                                            for rr in ry_sub:
                                                if rr[2] == fe[2]:
                                                    contain = True
                                                    break
                                        e_contain = False
                                        e = []
                                        used_word_ = uw.copy()
                                        if not contain:
                                            c_count = 0
                                            for rf_ in fe[2]:
                                                c_count1 = 0
                                                for rf__ in rf_:
                                                    if used_word_.__contains__(rf__):
                                                        e_contain = True
                                                        e.append(c_count + c_count1 * 2)
                                                        break
                                                    else:
                                                        used_word_.append(rf__)
                                                    c_count1 += 1
                                                c_count += 1
                                        if e_contain:
                                            xx = load_tz_inner(endings[fe[2][0][0]:int(fe[2][0][0]) + len(fe[2]) * 2],
                                                               fe[2][0][0], words, e,
                                                               False, used_word, [])
                                            ry = xx[0]
                                            used_word = xx[1]
                                            rz.extend(ry)
                                        elif not contain:
                                            used_word = used_word_.copy()
                                            for fz in fe[2]:
                                                one_note.append(fz[0])
                                                one_note.append(fz[1])
                                            rz.append(rz_)
                                            ry_sub.append(rz_)
                                    if fe[0].startswith('PAIR'):
                                        uw = re_check(uw)
                                        ee = pair_valid(fe, uw)
                                        if ee[0] is not None and ee[1] is not None:
                                            uw = ee[0]
                                            rz.append(ee[1])
                                    if fe[0].startswith('BOUND'):
                                        uw = re_check(uw)
                                        ee = bound_valid(fe, endings, words, uw)
                                        if ee[0] is not None and ee[1] is not None:
                                            uw = ee[0]
                                            rz.append(ee[1])

                            elif not ry_sub.__contains__(rz_):
                                ry_sub.extend(ry_)
                                one_note.append(count)
                                one_note.append(count0)
                                rz.append(rz_)
            count0 += 1
        count += 1

    return {
        'schema': rz,
        'z_anzahl': len(endings),
        'w_pro_z': l_oo
    }


def re_check(uw):
    if not uw:
        uw = used_word
    delete = []
    for uww in uw:
        contain = False
        for rr in Scheme(rz).single:
            for ww in rr.words:
                if ww == uww:
                    contain = True
        if not contain:
            delete.append(uww)
    for d in delete:
        uw.remove(d)
    return uw


def load_tz_inner(endings, ce, words, banned, serious, u, on):
    global used_word
    global one_note
    # ex = random.randint(0, 1000).__str__()
    '''
        if serious:
        used_word1 = u.copy()
        one_note1 = on.copy()
    else:
        used_word1 = used_word.copy()
        one_note1 = one_note.copy()
    '''

    used_word1 = u.copy()
    one_note1 = on.copy()

    rz1 = []
    ry_sub2 = []
    count = 0
    for end in endings:
        if end is None:
            count += 1
            continue
        if one_note1.__contains__(count + ce) or banned.__contains__(count + ce):
            continue
        count0 = 0
        for end_ in endings:
            if end_ is None:
                count0 += 1
                continue
            '''if banned.__contains__(count0 + ce):
                continue'''
            if count != count0 and end == end_:
                if count0 - count == 1:
                    rz_0 = (end, end_)
                    rz_1 = (count + ce, count0 + ce)
                    rz_2 = (words[count + ce], words[count0 + ce])
                    # check if pair is extended
                    cr = 1
                    while True:
                        if count0 + cr < len(endings) and endings[count0 + cr] == end_:
                            rz_0 = rz_0 + (endings[count0 + cr],)
                            rz_1 = rz_1 + (count0 + cr + ce,)
                            rz_2 = rz_2 + (words[count0 + cr + ce],)
                        else:
                            if count0 + cr >= len(endings):
                                break
                        cr += 1
                    pair_l = 1
                    cc_0 = 0
                    for rz_1_ in rz_1:
                        if cc_0 != 0:
                            pair_l += rz_1_ - rz_1[cc_0 - 1]
                        cc_0 += 1
                    rz_ = ['PAIR' + str(cc_0), rz_0, rz_1, rz_2]

                    contain = False
                    for rr in rz1:
                        if list_ends_with(list(rr[2]), list(rz_[2])):
                            contain = True
                            break
                    if not contain:
                        for rr in ry_sub2:
                            if list_ends_with(list(rr[2]), list(rz_[2])):
                                contain = True
                                break
                    used_word_0 = used_word1.copy()
                    if not contain:
                        count2_ = 0
                        for rz_2_ in rz_2:
                            if used_word_0.__contains__(rz_2_):
                                if count2_ > 1:
                                    rz_0 = rz_0[0:count2_]
                                    rz_1 = rz_1[0:count2_]
                                    rz_2 = rz_2[0:count2_]
                                    pair_l = 1
                                    cc_0 = 0
                                    for rz_1_ in rz_1:
                                        if cc_0 != 0:
                                            pair_l += rz_1_ - rz_1[cc_0 - 1]
                                        cc_0 += 1

                                    rz_ = ['PAIR' + str(cc_0), rz_0, rz_1, rz_2]
                                    break
                                contain = True
                                break
                            else:
                                used_word_0.append(rz_2_)
                            count2_ += 1
                    if not contain:
                        used_word1 = used_word_0.copy()
                        if not serious:
                            for fz in rz_1:
                                one_note1.append(fz)
                        ry_sub2.append(rz_)
                        rz1.append(rz_)
                elif count0 - count == 2:

                    between = max([count, count0]) - 1
                    if between + 2 < len(endings) and endings[between] == endings[between + 2] \
                            and not banned.__contains__(between + ce) and not banned.__contains__(between + 2 + ce):
                        cc = 1
                        re = [(end, end_), (endings[between], endings[between + 2])]
                        rx = [(ce + count, ce + count0), (ce + between, ce + between + 2)]
                        rf = [(words[count + ce], words[count0 + ce]), (words[between + ce], words[between + 2 + ce])]
                        while True:
                            n0 = between + 2 + cc
                            if (n0 < len(endings) and endings[n0] == endings[n0 - 2]) and \
                                    endings[n0] != endings[n0 - 1] and not banned.__contains__(n0):
                                re.append((endings[n0 - 2], endings[n0]))
                                rx.append((n0 - 2 + ce, n0 + ce))
                                rf.append((words[n0 - 2 + ce], words[n0 + ce]))
                            else:
                                break
                            cc += 1
                        if cc >= 1:
                            contain = False
                            rz_ = ["CROSS", re, rx, rf]
                            for rr in rz:
                                if rr[2] == rz_[2]:
                                    contain = True
                                    break
                            if not contain:
                                for rr in ry_sub2:
                                    if rr[2] == rz_[2]:
                                        contain = True
                                        break
                            e_contain = False
                            e = []
                            used_word_ = used_word1.copy()
                            added = []
                            added0 = []

                            if not contain:
                                c_count = 0
                                for rf_ in rf:
                                    c_count1 = 0
                                    for rf__ in rf_:

                                        if used_word_.__contains__(rf__) and not (
                                                added.__contains__(rf__) and added0[added.index(rf__)] == rx[c_count][
                                            c_count1]):
                                            e_contain = True
                                            e.append(rx[c_count][c_count1])
                                        else:
                                            used_word_.append(rf__)
                                            added.append(rf__)
                                            added0.append(rx[c_count][c_count1])
                                        c_count1 += 1
                                    c_count += 1
                            if e_contain:
                                # print("loop" + fz)
                                xx = load_tz_inner(endings[count:count + 4 + (cc - 1) * 2], count, words, e, False,
                                                   used_word1.copy(),
                                                   [])
                                ry = xx[0]
                                used_word = xx[1]
                                rz1.extend(ry)
                            elif not contain:
                                if not serious:
                                    for fz in rx:
                                        one_note1.append(fz[0])
                                        one_note1.append(fz[1])
                                rz1.append(rz_)
                                ry_sub2.append(rz_)
                                used_word1 = used_word_.copy()
                    else:
                        rz_0 = (end, end_)
                        rz_1 = (count + ce, count0 + ce)
                        rz_2 = (words[count + ce], words[count0 + ce])
                        # check if pair is extended
                        cr = 1

                        while True:

                            if count0 + cr < len(endings) and endings[count0 + cr] == end_:
                                rz_0 = rz_0 + (endings[count0 + cr],)
                                rz_1 = rz_1 + (count0 + cr + ce,)
                                rz_2 = rz_2 + (words[count0 + cr + ce],)
                            else:
                                if count0 + cr >= len(endings):
                                    break
                            cr += 1
                        pair_l = 1
                        cc_0 = 0
                        for rz_1_ in rz_1:
                            if cc_0 != 0:
                                pair_l += rz_1_ - rz_1[cc_0 - 1]
                            cc_0 += 1

                        rz_ = ['PAIR' + str(cc_0), rz_0, rz_1, rz_2]
                        contain = False
                        for rr in rz1:
                            if list_ends_with(list(rr[2]), list(rz_[2])):
                                contain = True
                                break
                        if not contain:
                            for rr in ry_sub:
                                if list_ends_with(list(rr[2]), list(rz_[2])):
                                    contain = True
                                    break
                        used_word_0 = used_word1.copy()
                        if not contain:
                            count2_ = 0
                            for rz_2_ in rz_2:
                                if used_word_0.__contains__(rz_2_):
                                    if count2_ > 1:
                                        rz_0 = rz_0[0:count2_]
                                        rz_1 = rz_1[0:count2_]
                                        rz_2 = rz_2[0:count2_]
                                        pair_l = 1
                                        cc_0 = 0
                                        for rz_1_ in rz_1:
                                            if cc_0 != 0:
                                                pair_l += rz_1_ - rz_1[cc_0 - 1]
                                            cc_0 += 1

                                        rz_ = ['PAIR' + str(cc_0), rz_0, rz_1, rz_2]
                                        break
                                    contain = True
                                    break
                                else:
                                    used_word_0.append(rz_2_)
                                count2_ += 1
                        if not contain:
                            used_word1 = used_word_0.copy()
                            rz1.append(rz_)
                            if not serious:
                                for fz in rz_1:
                                    one_note1.append(fz)
                            ry_sub2.append(rz_)
                elif count0 - count >= 3:
                    if endings[count] != endings[count + 1]:
                        confirm = 0
                        if not used_word1.__contains__(words[count + ce]):
                            used_word1.append(words[count + ce])
                            confirm += 1
                        if not used_word1.__contains__(words[count0 + ce]):
                            used_word1.append(words[count0 + ce])
                            confirm += 1

                        if confirm == 2:
                            uw = used_word1.copy()
                            used_word = uw.copy()
                            on = one_note1.copy()
                            one_note = on.copy()
                            xx = load_tz_inner(endings[count + 1:count0 + ce], count + ce + 1, words, [], False,
                                               used_word.copy(),
                                               [])
                            used_word = xx[1]
                            ry_ = xx[0]
                            rz_0 = (end, end_)
                            rz_1 = (count + ce, count0 + ce)
                            rz_2 = (words[count + ce], words[count0 + ce])
                            # check if pair is extended
                            cr = 1
                            while True:
                                if count0 + cr < len(endings) and endings[count0 + cr] == end_:
                                    rz_0 = rz_0 + (endings[count0 + cr],)
                                    rz_1 = rz_1 + (count0 + cr + ce,)
                                    rz_2 = rz_2 + (words[count0 + cr + ce],)
                                else:
                                    if count0 + cr >= len(endings):
                                        break
                                cr += 1

                            pair_l = 1
                            cc_0 = 0
                            for rz_1_ in rz_1:
                                if cc_0 != 0:
                                    pair_l += rz_1_ - rz_1[cc_0 - 1]
                                cc_0 += 1

                            rz_ = ['BOUND' + str(cc_0), rz_0, rz_1, rz_2, ry_]

                            contain = False
                            for rr in rz1:
                                if list_ends_with(list(rr[2]), list(rz_[2])):
                                    contain = True
                                    break
                            if not contain:
                                for rr in ry_sub:
                                    if list_ends_with(list(rr[2]), list(rz_[2])):
                                        contain = True
                                        break
                            used_word_0 = used_word.copy()
                            if not contain:
                                count2_ = 0
                                for rz_2_ in rz_2:
                                    if used_word_0.__contains__(rz_2_):
                                        if count2_ > 1:
                                            rz_0 = rz_0[0:count2_]
                                            rz_1 = rz_1[0:count2_]
                                            rz_2 = rz_2[0:count2_]
                                            rz_ = ['BOUND', rz_0, rz_1, rz_2, ry_]
                                            break
                                        contain = True
                                        break
                                    else:
                                        used_word_0.append(rz_2_)
                                    count2_ += 1
                            if not contain:
                                used_word = used_word_0.copy()
                                used_word1 = used_word.copy()
                            global ending_super
                            ry_continued = load_tz_inner(ending_super[count + 1 + ce:], count + 1 + ce, words, [], True,
                                                         uw, on)[0]

                            is_filled = False
                            fill_elements = []

                            for ry_element in ry_continued:
                                if not ry_.__contains__(ry_element):
                                    if ry_element[0].startswith('CROSS'):
                                        for tup in ry_element[2]:
                                            if not (tuple(tup)[0] > count0 and tuple(tup)[1] > count0):
                                                is_filled = True
                                                fill_elements.append(ry_element)
                                    elif ry_element[0].startswith("PAIR"):
                                        is_filled = ry_element[2][len(ry_element[2]) - 1] > count0 + ce
                                        if is_filled:
                                            fill_elements.append(ry_element)
                                    elif ry_element[0].startswith('BOUND'):
                                        is_filled = ry_element[2][1] > count0 + ce
                                        if is_filled:
                                            fill_elements.append(ry_element)

                            if is_filled:
                                rz_ = ["BOUND", rz_0, rz_1, rz_2, []]
                                if not ry_sub.__contains__(rz_):
                                    one_note1.append(count)
                                    one_note1.append(count0)
                                    rz1.append(rz_)
                                for fe in fill_elements:
                                    if fe[0] == 'CROSS':
                                        for fe_0 in fe[2]:
                                            one_note1.append(fe_0[0])
                                            one_note1.append(fe_0[1])
                                        contain = False
                                        if not contain:
                                            for rr in ry_sub:
                                                if rr[2] == fe[2]:
                                                    contain = True
                                                    break
                                        e_contain = False
                                        e = []
                                        used_word_ = uw.copy()
                                        if not contain:
                                            c_count = 0
                                            for rf_ in fe[2]:
                                                c_count1 = 0
                                                for rf__ in rf_:
                                                    if used_word_.__contains__(rf__):
                                                        e_contain = True
                                                        e.append(c_count + c_count1 * 2)
                                                        break
                                                    else:
                                                        used_word_.append(rf__)
                                                    c_count1 += 1
                                                c_count += 1
                                        if e_contain:
                                            xx = load_tz_inner(endings[fe[2][0][0]:int(fe[2][0][0]) + len(fe[2]) * 2],
                                                               fe[2][0][0], words, e,
                                                               False, uw.copy(), [])
                                            ry = xx[0]
                                            uw = xx[1]
                                            rz1.extend(ry)
                                        elif not contain:
                                            used_word1 = used_word_.copy()
                                            for fz in fe[2]:
                                                one_note1.append(fz[0])
                                                one_note1.append(fz[1])
                                            rz1.append(rz_)
                                            ry_sub2.append(rz_)
                                    if fe[0].startswith('PAIR'):
                                        uw = re_check(uw)
                                        e = pair_valid(fe, uw)
                                        if e[1]:
                                            used_word1 = e[0]
                                            rz1.append(e[1])
                                    if fe[0].startswith('BOUND'):
                                        uw = re_check(uw)
                                        e = bound_valid(fe, endings, words, uw)
                                        if e[1]:
                                            used_word1 = e[0]
                                            rz1.append(e[1])
                            elif not ry_sub.__contains__(rz_):
                                ry_sub2.extend(ry_)
                                one_note1.append(count)
                                one_note1.append(count0)
                                rz1.append(rz_)
            count0 += 1
        count += 1

    '''
        if not serious:
        one_note = one_note1.copy()
        used_word = used_word1.copy()
    '''

    return [rz1, used_word1]


def pair_valid(fe, us):
    global rz
    rz_ = fe
    contain = False
    used_word_0 = us.copy()
    if not contain:
        count2_ = 0
        for rz_2_ in rz_[3]:
            if used_word_0.__contains__(rz_2_):
                if count2_ > 1:
                    rz_0 = rz_[1][0:count2_]
                    rz_1 = rz_[2][0:count2_]
                    rz_2 = rz_[3][0:count2_]
                    rz_ = ['PAIR', rz_0, rz_1, rz_2]
                    break
                contain = True
                break
            else:
                used_word_0.append(rz_2_)
            count2_ += 1

    if not contain:
        used_word__x = used_word_0.copy()
        for fz in fe[2]:
            one_note.append(fz)
        ry_sub.append(rz_)
        return [used_word__x, rz_]

    return [None, None]


def bound_valid(fe, endings, words, uw):
    on = one_note.copy()
    global ending_super
    ry_continued = load_tz_inner(ending_super[fe[2][0] + 1:], fe[2][0] + 1, words, [], True, uw, on)[0]

    is_filled = False
    fill_elements = []

    used_word__x = []

    for ry_element in ry_continued:
        if not fe[4].__contains__(ry_element):
            if ry_element[0].startswith('CROSS'):
                for tup in ry_element[2]:
                    if not (tuple(tup)[0] > fe[2][1] and tuple(tup)[1] > fe[2][1]):
                        is_filled = True
                        fill_elements.append(ry_element)
            elif ry_element[0].startswith("PAIR"):
                is_filled = ry_element[2][len(ry_element[2]) - 1] > fe[2][1]
                if is_filled:
                    fill_elements.append(ry_element)
            elif ry_element[0].startswith('BOUND'):
                is_filled = ry_element[2][1] > fe[2][1]
                if is_filled:
                    fill_elements.append(ry_element)
    if is_filled:
        rz_ = ["BOUND", (fe[1][0], fe[1][0]), (fe[2][0], fe[2][1]), (words[fe[2][0]], words[fe[2][1]]), []]
        if not ry_sub.__contains__(rz_):
            one_note.append(fe[2][0])
            one_note.append(fe[2][1])
            rz.append(rz_)
        for fe in fill_elements:
            if fe[0] == 'CROSS':
                for fe_0 in fe[2]:
                    one_note.append(fe_0[0])
                    one_note.append(fe_0[1])
                contain = False
                if not contain:
                    for rr in ry_sub:
                        if rr[2] == fe[2]:
                            contain = True
                            break
                e_contain = False
                e = []
                used_word_ = uw.copy()
                if not contain:
                    c_count = 0
                    for rf_ in fe[2]:
                        c_count1 = 0
                        for rf__ in rf_:
                            if used_word_.__contains__(rf__):
                                e_contain = True
                                e.append(c_count + c_count1 * 2)
                                break
                            else:
                                used_word_.append(rf__)
                            c_count1 += 1
                        c_count += 1
                if e_contain:
                    xx = load_tz_inner(endings[fe[2][0][0]:int(fe[2][0][0]) + len(fe[2]) * 2], fe[2][0][0],
                                       words, e,
                                       False, uw, [])
                    ry = xx[0]
                    uw = xx[1]
                    rz.extend(ry)
                elif not contain:
                    used_word__x = used_word_.copy()
                    for fz in fe[2]:
                        one_note.append(fz[0])
                        one_note.append(fz[1])
                    rz.append(rz_)
                    ry_sub.append(rz_)
            if fe[0].startswith('PAIR'):
                uw = re_check(uw)
                e = pair_valid(fe, uw)
                if e[1]:
                    used_word__x = e[0]
                    rz.append(e[1])
            if fe[0].startswith('BOUND'):
                uw = re_check(uw)
                e = bound_valid(fe, endings, words, uw)
                if e[1]:
                    used_word__x = e[0]
                    rz.append(e[1])
    elif not ry_sub.__contains__(fe):
        ry_sub.extend(fe[4])
        one_note.append(fe[2][0])
        one_note.append(fe[2][1])
        return [used_word__x, fe]

    return [None, None]


def list_ends_with(list_1, list_2):
    return str(list_1)[1:-1].endswith(str(list_2)[1:-1])


def __reimschema_typus_validation_sub1(s_element) -> int:
    ry_count = 0
    s3 = s_element[2]
    if s_element[0].startswith('CROSS'):
        ry_count += len(list(s3)) * 2
    elif s_element[0].startswith('BOUND'):
        ry_count += len(tuple(s3))
        for ss_element in s_element[4]:
            ry_count += __reimschema_typus_validation_sub1(ss_element)
    else:
        ry_count += len(tuple(s3))

    return ry_count


class Scheme:
    def __init__(self, scheme_0):
        self.scheme = scheme_0
        self.single = self.__generate_r_single()
        self.words = self.__generate_pure_words()
        self.classes = self.__generate_rhyme_classes()

    def __generate_r_single(self) -> list:
        rhymes = []
        for r in self.scheme:
            def __looping_add(rr):
                ry = Rhyme(rr)
                if ry.has_inner_elements():
                    for inner in ry.inner_elements:
                        __looping_add(inner)
                rhymes.append(ry)

            __looping_add(r)
        return rhymes

    def __generate_pure_words(self) -> list:
        words = []
        for s_single in self.single:
            words.extend(s_single.words)
        return words

    def __generate_rhyme_classes(self) -> list:
        classes = []
        for s_single in self.single:
            if not classes.__contains__(s_single.rhyme_group):
                classes.append(s_single.rhyme_group)
        return classes

    def __str__(self):
        return str(self.scheme)

    def to_json(self):
        cl0 = []
        for cl in self.single:
            cl0.append(str(cl))

        return json.dumps([cl0, self.words, self.classes])


class Rhyme:

    def __init__(self, r0):
        self.type = r0[0]
        '''if not str(self.type[-1]).isnumeric():
            self.type = self.type + "2"'''

        if self.type.startswith('CROSS'):
            self.element_count = 0
            self.rhyme_group = {}
            for t in r0[1]:
                self.element_count += len(t)
                if not self.rhyme_group.keys().__contains__(t[0]):
                    self.rhyme_group.update({t[0]: 2})
                else:
                    self.rhyme_group[t[0]] += 2
            self.words = []
            for w in r0[2]:
                for ww in w:
                    self.words.append(ww)
            self.rhyme_group = {}
        else:
            self.element_count = len(r0[1])
            self.rhyme_group = r0[1][0]
            """Problem with rhyme group:
            In a CROSS Rhyme, there are multiple rhyme-groups. This means rhyme_group
            be a list. This also has to indicate how many words build the group in the cross rhyme.
            To do this, we need a dict instead of a string, where K is the group and V the usage.
            For a simple PAIR (0,1) (iːsn):
                self.rhyme_group = {'iːsn': 2}
            For a CROSS ((0,2),(1,3)) (iːsn, ɔʁt):
                self.rhyme_group = {'iːsn': 2, 'ɔʁt': 2}
            """
            self.positions = r0[2]
            self.words = r0[3]
            """Problem: words is used to define the rhyme length.
            For a CROSS rhyme (above) the lenght would be 2.
            """
            if self.type.startswith('BOUND'):
                self.inner_elements = r0[4]

    def has_inner_elements(self) -> bool:
        return self.type.startswith('BOUND') and len(self.inner_elements) > 0

    def __str__(self):
        return str(self.words)

    def __json__(self):
        return [self.words]


def r0_validation(schemes_total):
    words_used_in_rhymes = []
    rhyme_groups = dict({})
    rhyme_types = {}
    for schema in schemes_total:
        for rhyme in schema.single:

            def __check_in_loop(rhyme_g, v, rhyme_groups) -> dict:
                if not rhyme_groups.keys().__contains__(rhyme_g):
                    rhyme_groups.update({rhyme_g: v})
                else:
                    rhyme_groups[rhyme_g] += v

                return rhyme_groups

            if isinstance(rhyme.rhyme_group, dict):
                for rhyme_groupA, usage in rhyme.rhyme_group:
                    rhyme_groups = __check_in_loop(rhyme_groupA, usage, rhyme_groups)
            else:
                rhyme_groups = __check_in_loop(rhyme.rhyme_group, 2, rhyme_groups)

            if not rhyme_types.__contains__(rhyme.type):
                rhyme_types[rhyme.type] = 1
            else:
                rhyme_types[rhyme.type] = rhyme_types[rhyme.type] + 1

            _finished = 0
            for word in rhyme.words:
                def __r_w_(word0) -> int:
                    if not words_used_in_rhymes.__contains__(word0):
                        words_used_in_rhymes.append(word0)
                        return 1
                    return 0

                _finished += __r_w_(word)
            if rhyme.element_count - _finished > 1:
                words_used_in_rhymes = words_used_in_rhymes[0:len(words_used_in_rhymes) - _finished]
                # rhyme_groups.update({rhyme.rhyme_group: (rhyme_groups[rhyme.rhyme_group] - 1)})
                if isinstance(rhyme.rhyme_group, dict):
                    for f, r in rhyme.rhyme_group:
                        rhyme_groups.update({f: (rhyme_groups[f] - r)})
                else:
                    rhyme_groups.update({rhyme.rhyme_group: (rhyme_groups[rhyme.rhyme_group] - 1)})
                rhyme_types[rhyme.type] = rhyme_types[rhyme.type] - 1

    # load percentages from rhyme.frequency.json

    f_frequency = assets("rhyme_frequency.json", "r")

    frequency = json.loads(f_frequency.read())
    a1 = frequency['PAIR']
    a2 = frequency['CROSS']
    a3 = frequency['BOUND']

    w1 = 0
    w2 = 0
    w3 = 0

    print(rhyme_types)

    for key in rhyme_types.keys():
        if str(key).startswith("PAIR"):
            if not str(key).endswith("2") and not str(key)[-1] == "R":
                if int(str(key)[-1]) % 2 == 0:
                    w1 += int(str(key)[-1]) / 2 * rhyme_types[key]
                else:
                    w1 += rhyme_types[key]
            else:
                w1 += rhyme_types[key]
        if str(key).startswith("CROSS"):
            w2 += rhyme_types[key]
        if str(key).startswith("BOUND"):
            w3 += rhyme_types[key]

    w0 = w1 + w2 + w3
    if w1 > 0:
        w1 = w0 / w1
    if w2 > 0:
        w2 = w0 / w2
    if w3 > 0:
        w3 = w0 / w3
    print(((w1 / a1 + w2 / a2 + w3 / a3) / 3 - 1))
    f = (w1 / a1 + w2 / a2 + w3 / a3) / 3

    # value f: Generalflexibilität

    return rhyme_types, rhyme_groups, f, w0


def valid0(schemes, z_len):
    """VALID0 is a method for rhyme complexity and usage validation (and handling)."""

    rhyme_types, rhyme_groups, f0_value, w0 = r0_validation(schemes_total=schemes)
    if z_len != 0:
        f1_value = w0 * 2 / z_len
    else:
        f1_value = 0
    print("Reimverteilung: " + str(f0_value))
    print("Reimhäufigkeit im Gedicht: " + str(f1_value))

    rg2 = rhyme_group_valid(rhyme_groups)
    print("Reimhäufigkeit pro Reim:  " + str(rg2))
    f3_value = 0
    if len(rg2) != 0:
        for key in rg2:
            f3_value += rg2[key][1]
        f3_value /= len(rg2)
    print("Reimhäufigkeit durchschnitt: " + str(f3_value))

    return f0_value, f1_value, w0 * 2, f3_value


def rhyme_group_valid(rhyme_group) -> dict:
    """rhyme_group is a dict, {K:V} where K is the rhyme-group as str and V the usage"""
    for group, usage in rhyme_group.items():
        """locate the group in wikitionary"""
        url = 'https://de.wiktionary.org/wiki/Reim:Deutsch:-' + group
        content = requests.get(url)

        count = 0
        text = content.text

        del content

        while True:
            if len(text) < 8:
                break
            if not text.__contains__('<ul><li>'):
                break
            index0 = text.index('<ul><li>')
            if not text.__contains__('</ul>'):
                break
            index1 = text.index('</ul>', index0)
            crop = text[index0 + len('<ul><li>'):index1]
            count += count_substring(crop, '<a h')
            del crop
            text = text[index1 + len('<ul><li>'):]
            if text.startswith('<!-- '):
                break
        del text

        """Return total and usage / total"""

        rhyme_group[group] = (count, 1 - count / 176 * 0.5) # 176 / count because if count is higher our score should be lower

    return rhyme_group


def count_substring(string, sub_string):
    ans = 0
    for i in range(len(string) - (len(sub_string) - 1)):
        if sub_string == string[i:len(sub_string) + i]:
            ans += 1

    # print(string+"/////"+sub_string)

    return ans


def assets(name, mode):
    top = __file__
    top = top[0:top.rfind("/")]
    return open(top + "/assets/" + name, mode)


def direct_word_analysis(gedicht):
    # gedicht = gedicht.split()
    words = gedicht.split()
    print(words)
    words_ = []
    for word in words:
        word_ = ""
        if word.__contains__('\uf8ff'):
            inc = word.index('\uf8ff')
            w_sep = word[0:inc]
            w_sep_ = ""

            for c in w_sep:
                if c.isalpha() and not c.isnumeric():
                    w_sep_ += c
            # print("-"+word)
            word = word[inc:]
            word = word.replace('\uf8ff', '', -1)
            # print("="+word)
            if len(w_sep_) > 0:
                words_.append(w_sep_)

        for c in word:
            if c.isalpha() and not c.isnumeric():
                word_ += c
        if len(word_) > 0:
            words_.append(word_)

    lt = list(json.loads(assets('trash_word.json', 'r').read()))

    def_word = {}

    # already_def_word = []

    def __check_type(type) -> bool:
        type = str(type)
        # print("check type ... "+type)
        return type.startswith(
            'Substantiv') or type == 'Verb' or type == 'Adjektiv' or type == 'Konjugierte Form' or type == 'Deklinierte Form'

    def __word_type_wiktionary(w) -> str:
        url = 'https://de.wiktionary.org/wiki/' + w
        # print(url)
        content = requests.get(url)

        if content.status_code == 404:
            return ""

        """<a href="/wiki/Hilfe:Wortart#Konjugierte_Form" title="Hilfe:Wortart">Konjugierte Form</a>"""
        if not content.text.__contains__('title="Hilfe:Wortart">'):
            print("PROBLEM WITH: " + w)
            """<i><b><a href="/wiki/rauer#rauer_(Deutsch)" title="rauer">rauer</a></b></i>"""
            sb0 = '<i><b><a href="/wiki/'
            sb1 = 'title="'

            dcx = content.text[content.text.index(sb0) + len(sb0): content.text.index('</a></b></i>')]
            new_element = dcx[dcx.index(sb1) + len(sb1): dcx.index('">')]

            print("new element - " + new_element)

            return __word_type_wiktionary(new_element)

        ic0 = content.text.index('title="Hilfe:Wortart">') + len('title="Hilfe:Wortart">')
        ic1 = content.text.index('</a>', ic0)
        p = content.text[ic0:ic1]
        return p

    def __load_usage_dwds(w) -> int:

        url = 'https://www.dwds.de/?q=' + w
        content = requests.get(url)

        if content.status_code == 404:
            return -1

        s2 = '<table class="serif italic word-frequency">'
        if not content.text.__contains__(s2):
            return -1
        idc = content.text.index(s2) + len(s2)
        data = content.text[idc:content.text.index('</table>', idc)]

        score = 7 - count_substring(data, '<div class="word-frequency-active"></div>')

        # already_def_word[w]: (p, score)
        return score

    def load_word(w) -> tuple:

        if def_word.keys().__contains__(w):
            # print("already there")
            return (w, 1)

        """send request to dwds"""
        # url = 'https://de.wiktionary.org/wiki/' + w
        url = 'https://www.dwds.de/?q=' + w
        content = requests.get(url)

        if lt.__contains__(w):
            return None

        # print(content.status_code)
        # print(content.url)

        if content.status_code == 404:

            # print("dwds request was denied")

            if w[0].isupper():
                return load_word(w.lower())

            w = w.capitalize()

            url = 'https://de.wiktionary.org/wiki/' + w
            content = requests.get(url)
            """<a href="/wiki/Hilfe:Wortart#Konjugierte_Form" title="Hilfe:Wortart">Konjugierte Form</a>"""
            if not content.text.__contains__('title="Hilfe:Wortart">'):
                # print("PROBLEM WITH: " + w)
                """<i><b><a href="/wiki/rauer#rauer_(Deutsch)" title="rauer">rauer</a></b></i>"""
                sb0 = '<i><b><a href="/wiki/'
                sb1 = 'title="'

                dcx = content.text[content.text.index(sb0) + len(sb0): content.text.index('</a></b></i>')]
                new_element = dcx[dcx.index(sb1) + len(sb1): dcx.index('">')]

                # print("new element - " + new_element)

                load_word(new_element)

            ic0 = content.text.index('title="Hilfe:Wortart">') + len('title="Hilfe:Wortart">')
            ic1 = content.text.index('</a>', ic0)
            p = content.text[ic0:ic1]

            # print(p + "-" + w)

            score = __load_usage_dwds(w)

            if score != -1 and __check_type(p):
                return (w, p, score, 1)

        else:
            s0 = '</span><span class="dwdswb-ft-blocktext"><span>'

            # print(content.text)

            """<span class="dwdswb-ft-blocklabel serif italic">Grammatik&nbsp;</span>"""

            if content.text.__contains__(s0):

                # print("grammer found")

                # print(content.text[content.text.index(s0):])
                x = content.text[content.text.index(s0) + len(s0):]
                # print(x)
                if not x.__contains__("</span>"):
                    # print("--d")
                    """search for word type at wiktionary"""
                    """irrelevant word"""
                    # print("err 0 for " + w)
                    return (w,)

                p = x[0:x.index("</span>")]

                # print(p + "-" + w)

                s2 = '<table class="serif italic word-frequency">'
                if not content.text.__contains__(s2):
                    # print("--e")
                    return (w,)
                idc = content.text.index(s2) + len(s2)
                data = content.text[idc:content.text.index('</table>', idc)]

                score = 7 - count_substring(data, '<div class="word-frequency-active"></div>')

                # already_def_word[w]: (p, score)
                if __check_type(p):

                    # print("c--")
                    return (w, p, score, 1)
                else:
                    pn = __word_type_wiktionary(w)
                    if __check_type(pn):
                        return (w, pn, score, 1)
            else:

                # print("no grammar found at dwds...")

                url = 'https://www.dwds.de/?q=' + w.lower()
                content = requests.get(url)
                s0 = '</span><span class="dwdswb-ft-blocktext"><span>'
                if content.text.__contains__(s0):

                    # print("grammer found at dwds... success")

                    x = content.text[content.text.index(s0) + len(s0):]
                    # print(x)
                    p = x[0:x.index("</span>")]
                    # print(p + "-" + w)
                    s2 = '<table class="serif italic word-frequency">'
                    if not content.text.__contains__(s2):
                        # print("--w")
                        return (w,)
                    idc = content.text.index(s2) + len(s2)
                    data = content.text[idc:content.text.index('</table>', idc)]

                    score = 7 - count_substring(data, '<div class="word-frequency-active"></div>')

                    # already_def_word[w]: (p, score)
                    if __check_type(p):
                        return (w, p, score, 1)
                    else:
                        pn = __word_type_wiktionary(w)
                        if __check_type(pn):
                            return (w, pn, score, 1)
                else:

                    """the usage will be calculated using the duden API"""
                    # print("usage problematic")
                    return (w,)
        return (w,)

    median = 0
    median_n = 0
    median_add = 0.0001

    for word in words_:
        d = load_word(word)
        print(d)
        if d:
            if len(d) > 2:
                def_word[d[0]] = d
                median += pow(math.e, d[2])
                median_n += d[2]
                median_add += 1
            elif len(d) == 2:
                """adding count to tuple"""
                tu = list(def_word[d[0]])
                tu[3] += 1
                def_word[d[0]] = tuple(tu)
                median += pow(math.e, def_word[d[0]][2])
                median_n += def_word[d[0]][2]
                median_add += 1
    if median_n == 0:
        return def_word, 0
    print(median)
    # 6 / 6 = 1
    # 6 / 1 = 6
    # 1/6 * 6 / 6 = 1/6
    # 1/6 * 6 = 1.0
    return def_word, 1 - 1 / (median / median_add)


def valid1(gedicht):
    """VALID1 is a method for word complexity, types and originality validation"""
    words_defintions, result0 = direct_word_analysis(gedicht)
    print("Durschnittlicher Seltenheitswert liegt bei: " + str(result0))
    print("gemessen in 0: häufig und 6: selten")
    return result0


def run_test_f(input_poetry: str):
    """
    running the last test
    :param input_poetry: a poetry
    :return: the scores for this poetry based on rhymes and schemes
    """
    lines = input_poetry.split("\n")
    paragraph = []
    for line in lines:
        if not line.__len__() == 0 and not line.startswith("\n"):
            if len(paragraph) > 0:
                paragraph[-1] += str(line + "\n")
            else:
                paragraph.append(line + "\n")
        else:
            paragraph.append("")
    total_r = 0

    # jede Strophe wird analysiert...

    total_schemes = []
    z_length = 0
    print(paragraph)
    if len(paragraph) == 0:
        return 0
    for p in paragraph:

        if p.endswith("\n"):
            p = p[:-1]
        result = reimschema_typus(p)
        print(result)

        total_schemes.append(Scheme(result['schema']))
        z_length += result['z_anzahl']

    f0, f1, f2, f3 = valid0(schemes=total_schemes, z_len=z_length)
    f4 = valid1(input_poetry)

    mass_f0 = 5.70611  # 5.70611 in 126 tries
    mass_f1 = 0.449997  # 0.449997 in 126 tries
    # no mass f2
    mass_f3 = 3.50783  # 3.50783 in 126 tries
    mass_f4 = 3 # durschnitt

    mesh_f0 = 3  # editable
    mesh_f1 = 5  # editable
    mesh_f2 = 3
    mesh_f3 = 3  # editable
    mesh_f4 = 4


    """
     print("Reimverteilung: " + str(f0_value))
    print("Reimhäufigkeit im Gedicht: " + str(f1_value))

    rg2 = rhyme_group_valid(rhyme_groups)
    print("Reimhäufigkeit pro Reim:  " + str(rg2))
    f3_value = 0
    if len(rg2) != 0:
        for key in rg2:
            f3_value += rg2[key][1]
        f3_value /= len(rg2)
    print("Reimhäufigkeit durchschnitt: " + str(f3_value))
    
    
    f0: Reimverteilung
    f1: Reimhäufigkeit
    f2: Anzahl Reimwörter
    f3: Reimhäufigkeit bezogen auf die Besonderheit des Reimes
    f4: Besonderheit der Wörter
    """

    # f2 is the amount of rhymes in general.

    """f_pre_mass_mesh = 1 + mesh_f0 * (f0 / mass_f0) + mesh_f1 * (f1 / mass_f1) + mesh_f2 * (f2 / 10) + mesh_f3 * (
            f3 / mass_f3) + mesh_f4 * (f4 / mass_f4)"""
    print(f2 * f3 / 20)
    print((f1 - mass_f1) / 100)

    f_alternative = math.log10(f2) * (f0 + f1 + f3 + f4) / 4
    print("alt:"+str(f_alternative))

    """f_post_mass_mesh = 1 + (((f0 - mass_f0)/10 + f2 * f3 / ((f1  - mass_f1) / 100) / 100 + (f4 - mass_f4) / 10))

    print(f_post_mass_mesh)
    if f_post_mass_mesh < 0:
        f_post_mass_mesh = 0"""

    return f_alternative, [f0, f1, f2, f3, f4], total_schemes[0].to_json()


if __name__ == '__main__':
    # gedicht = "Das ist das Gedicht.\nIch schreibe über Liebe,\n, die mich so erpicht.\nWarum ist es so Einsamkeit?\nWarum bin ich befreit?\nIch schreibe über Diebe. Ich mag das Haus\nIch mag die Maus\nIch muss raus.\nIch will nicht mehr\nIch mag es sehr."
    gedicht = "Der Reim\nist klein.\naber fein.\nund mein\nund dein"
    # gedicht = "Hier reimt\nsich nichts"
    gedicht = open("assets/erlönig.txt", "r").read()
    print(run_test_f(gedicht))
