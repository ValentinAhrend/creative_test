import time

import requests

from mechanics.instruments import Value
import test_f


# from 'v0: /Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/aiTest
def ex000():
    def rhyme_valid(rhyme) -> int:
        """rhyme_group is a dict, {K:V} where K is the rhyme-group as str and V the usage"""
        url = 'https://de.wiktionary.org/wiki/Reim:Deutsch:-' + rhyme
        print(url)
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
        print(count)
        return count

    def count_substring(string, sub_string):
        ans = 0
        for i in range(len(string) - (len(sub_string) - 1)):
            if sub_string == string[i:len(sub_string) + i]:
                ans += 1

        # print(string+"/////"+sub_string)

        return ans

    def load_random_rhymes(word, language):
        # print("get word_ " + word)

        global before

        before = word
        url = "https://de.wiktionary.org/wiki/Spezial:Zuf%C3%A4llige_Seite"

        content = requests.get(url)

        word = content.url[content.url.rindex("wiki/") + len("wiki/"):]
        print(content.url)

        # wikitionary daten laden

        connected = False

        while content.status_code == 404:
            url = 'https://de.wiktionary.org/w/index.php?search=' + word + '&title=Spezial:Suche&go=Seite&ns0=1'
            content = requests.get(url)

            if not content.url.__contains__('index.php?search='):
                return test_f.load_rhymes(content.url[content.url.rfind("/") + 1:], language)

            # url wurde nicht gefunden, suche nach dem Wort wird gestartet

            q0 = "<div class='mw-search-result-heading'><a href=\""

            if not content.text.__contains__(q0):
                connected = True
                # die Suche ist erfolglos, da es keine Ergebnisse gibt
                break

            index0 = content.text.index(q0)
            index1 = content.text.index('" title', index0 + len(q0))

            part = content.text[index0 + len(q0):index1]
            return test_f.load_rhymes(part, language)
            # das ergebniss wird nun erneut gesucht

        q1 = '<dd><a href="/wiki/Hilfe:Reime" title="Hilfe:Reime">Reime:</a> <span class="ipa" style="padding: 0 1px; text-decoration: none;">'
        q2 = 'title="Reim:Deutsch:'
        # print(content.text.__contains__(q1))
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

                        if not test_f.has_vocals(word):
                            '''syllables are not found, now using pyphen'''
                            syllables = test_f.dic.inserted(word)
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
                                if len(we) > 2 and (test_f.d.check(we) or test_f.d.check(we.capitalize())):
                                    wu_.append(we)
                                    we = ""

                            # print(wu_)

                            if len(wu_) > 0 and word.endswith(wu_[-1]):
                                return test_f.load_rhymes(wu_[-1], language)
                            else:
                                return time.time_ns().__str__()

                        if changed:

                            if before.rfind(word) + word.__len__() is not before.__len__():
                                return test_f.load_rhymes(
                                    (word + before[before.rfind(word) + word.__len__()]).capitalize(),
                                    'de')
                            else:
                                return test_f.load_rhymes(word.capitalize(), 'de')
                        else:
                            return time.time_ns().__str__()

                    else:
                        '''syllables are not found, now using pyphen'''
                        syllables = test_f.dic.inserted(word)
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
                            if len(we) > 2 and (test_f.d.check(we) or test_f.d.check(we.capitalize())):
                                # print("dic found " + we)
                                wu_.append(we)
                                we = ""

                        # print(wu_)

                        if wu_ != [] and len(wu_[-1]) > 2 and word.endswith(wu_[-1]):
                            return test_f.load_rhymes(wu_[-1], language)
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

    zz = 0
    for i in range(50):
        rhy = load_random_rhymes("", 'de')
        while rhy is None or rhy.isnumeric():
            rhy = load_random_rhymes("", 'de')
            # print(rhy)
        print(i)
        zz += rhyme_valid(rhy)
    print(zz)

    # 8800 for 50
    # 8800/50 = 176 (average) -> 176 = 0.5


before = "a"

if __name__ == '__main__':
    ex000()
    exit(1)
    '''if True:
        dic = enchant.Dict('de_DE')
        out = dic.check('auu')
        print(out)
        exit(0)'''
    '''if True:
        nrv = NRV()
        nrv.start()
        exit(0)'''

    print("RUNNING TEST F - MAIN.PY - ASP")

    url = 'https://gedichte.ws/zufall'
    # url = 'https://www.gedichte.ws/sonstige/1854'
    content = requests.get(url)
    print(content.url)

    index0 = content.text.index("<p>")
    index1 = content.text.index("</p>", index0)
    piut = content.text[index0 + 3:index1]

    errr = piut.split("<br />")

    e2 = []
    for e in errr:
        if e.__contains__('&quot;'):
            e = e.replace('&quot;', '')
        if e.__contains__("\n"):
            e = e.replace("\r\n", "")
        e2.append(e)

    piut = "".join(e2)

    while piut.endswith(""):
        piut = piut[:-1]

    if piut.__contains__("©"):
        piut = piut[0:piut.index("©")]
    gedicht = piut.strip()
    print(gedicht)
    # gedicht = open("/Users/valentinahrend/OneDrive/! Valentin/Kreativität Quellen/project/application/creativity_test/test_F/assets/text_gedicht","r").read()

    # init von dem Value-Wert des Tests

    value0 = Value('Test-F-Value')

    # Fehlerüberprüfung

    if len(gedicht) == 0 or len(gedicht.split(" ")) <= 2:
        value0.send_exception("Formatexception", "Das Gedicht ist falsch formatiert.")

    # Gedicht in Paragraphen unterteilen
    # Achtung: Der Linebreaker (\n) wird vorher durch ein  ersetzt.

    lines = gedicht.split(sep="")
    paragraphs = [""]
    for line in lines:
        if line != "" and line != "":
            paragraphs[len(paragraphs) - 1] += line + ""
        else:
            paragraphs.append("")

    # wir haben nun das paragraphen array geschaffen

    # Fehlerüberprüfung

    if len(paragraphs) == 0:
        value0.send_exception("Formatexception", "Das Format des Gedichtes ist nicht korrekt. Die Einteilung in "
                                                 "Paragraphen ist fehlgeschlagen.")

    total_r = 0

    # jede Strophe wird analysiert...

    total_schemes = []
    z_length = 0

    for paragraph in paragraphs:

        if paragraph.endswith(""):
            paragraph = paragraph[:-1]

        result = test_f.reimschema_typus(paragraph)
        print(result)

        total_schemes.append(test_f.Scheme(result['schema']))
        z_length += result['z_anzahl']

    f0, f1, f2, f3 = test_f.valid0(schemes=total_schemes, z_len=z_length)
    f4 = test_f.valid1(gedicht)

    mass_f0 = 5.70611  # 5.70611 in 126 tries
    print(f0)
    mass_f1 = 44.9997  # 44.9997 in 126 tries
    print(f1)
    # no mass f2
    mass_f3 = 3.50783  # 3.50783 in 126 tries
    print(f3)  #
    mass_f4 = 10
    print(f4)  # Wort besonderheit

    mesh_f0 = 3  # editable
    mesh_f1 = 5  # editable
    mesh_f2 = 3
    mesh_f3 = 3  # editable
    mesh_f4 = 4

    # f2 is the amount of rhymes in general.

    f_pre_mass_mesh = 1 + mesh_f0 * (f0 / mass_f0) + mesh_f1 * (f1 / mass_f1) + mesh_f2 * (f2 / 100) + mesh_f3 * (
            f3 / mass_f3) + mesh_f4 * (f4 / mass_f4)

    print("->>" + str(f_pre_mass_mesh))
