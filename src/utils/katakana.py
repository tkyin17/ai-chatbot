import re
import sys
import MeCab
import alkana
import pandas as pd

sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf8", buffering=1)

alpha_reg = re.compile(r"^[a-zA-Z]+$")


def is_alpha(s) -> bool:
    return alpha_reg.match(s) is not None


def katakana_converter(text: str) -> str:
    wakati = MeCab.Tagger("-Owakati")
    wakati_result = wakati.parse(text)

    df = pd.DataFrame(wakati_result.split(" "), columns=["word"])
    df = df[df["word"].str.isalpha() == True]
    df["english_word"] = df["word"].apply(is_alpha)
    df = df[df["english_word"] == True]
    df["katakana"] = df["word"].apply(alkana.get_kana)

    dict_rep = dict(zip(df["word"], df["katakana"]))

    for word, read in dict_rep.items():
        try:
            text = text.replace(word, read)
        except:
            pass

    return text
