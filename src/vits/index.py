import time

# import torch_directml
from text import text_to_sequence
from torch import no_grad, LongTensor
from vits.utils import get_hparams_from_file, load_checkpoint
from vits.models import SynthesizerTrn
from vits.commons import intersperse

# DEVICE = torch_directml.device() if torch_directml.is_available() else "cpu"
DEVICE = "cpu"
MODEL_PATH = "src/vits_model/G_953000.pth"
CONFIG_PATH = "src/vits_model/config.json"

hps_ms = None
net_g_ms = None


def get_text(text, hps):
    text_norm, clean_text = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm, clean_text


def init_vits_model():
    global DEVICE, hps_ms, net_g_ms

    hps_ms = get_hparams_from_file(CONFIG_PATH)
    net_g_ms = SynthesizerTrn(
        len(hps_ms.symbols),
        hps_ms.data.filter_length // 2 + 1,
        hps_ms.train.segment_size // hps_ms.data.hop_length,
        n_speakers=hps_ms.data.n_speakers,
        **hps_ms.model,
    )
    _ = net_g_ms.eval().to(DEVICE)
    speakers = hps_ms.speakers
    model, optimizer, learning_rate, epochs = load_checkpoint(
        MODEL_PATH, net_g_ms, None
    )


def vits(
    text,
    language=1,
    speaker_id=324,
    noise_scale=0.6,
    noise_scale_w=0.668,
    length_scale=1.2,
):
    global DEVICE

    start = time.perf_counter()
    if not len(text):
        return "输入文本不能为空！", None, None
    text = text.replace("\n", " ").replace("\r", "").replace(" ", "")
    if len(text) > 200:
        return f"输入文字过长！{len(text)}>100", None, None
    if language == 0:
        text = f"[ZH]{text}[ZH]"
    elif language == 1:
        text = f"[JA]{text}[JA]"
    else:
        text = f"{text}"
    stn_tst, clean_text = get_text(text, hps_ms)
    with no_grad():
        x_tst = stn_tst.unsqueeze(0).to(DEVICE)
        x_tst_lengths = LongTensor([stn_tst.size(0)]).to(DEVICE)
        speaker_id = LongTensor([speaker_id]).to(DEVICE)
        audio = (
            net_g_ms.infer(
                x_tst,
                x_tst_lengths,
                sid=speaker_id,
                noise_scale=noise_scale,
                noise_scale_w=noise_scale_w,
                length_scale=length_scale,
            )[0][0, 0]
            .data.cpu()
            .float()
            .numpy()
        )

    return (
        "generated successfully",
        (22050, audio),
        f"time took: {round(time.perf_counter()-start, 2)} s",
    )
