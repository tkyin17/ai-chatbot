import re
import MeCab
import alkana
import pandas as pd

alpha_reg = re.compile(r"^[a-zA-Z]+$")


def is_alpha(s) -> bool:
    return alpha_reg.match(s) is not None


def katakana_converter(text: str) -> str:
    wakati = MeCab.Tagger("-Owakati")
    wakati_result = wakati.parse(text)

    data_frame = pd.DataFrame(wakati_result.split(" "), columns=["word"])
    data_frame = data_frame[data_frame["word"].str.isalpha() == True]
    data_frame["english_word"] = data_frame["word"].apply(is_alpha)
    data_frame = data_frame[data_frame["english_word"] == True]
    data_frame["katakana"] = data_frame["word"].apply(alkana.get_kana)

    dict_rep = dict(zip(data_frame["word"], data_frame["katakana"]))

    for word, read in dict_rep.items():
        try:
            text = text.replace(word, read)
        except Exception as error:
            print(f"error converting text to katakana: {error}")

    return text
