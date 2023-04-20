import time
import json
import os
import torch
from torch import no_grad, LongTensor
from utils.hparams import HParams
from utils.models import SynthesizerTrn
from utils.text import text_to_sequence

DEVICE = "cpu"
MODEL_PATH = "src/model/G_953000.pth"
CONFIG_PATH = "src/model/config.json"

hps_ms = None
net_g_ms = None


def get_hparams_from_file():
    with open(CONFIG_PATH, "r") as f:
        data = f.read()
    config = json.loads(data)

    hparams = HParams(**config)
    return hparams


def load_checkpoint(checkpoint_path, model, optimizer=None):
    assert os.path.isfile(checkpoint_path)
    checkpoint_dict = torch.load(checkpoint_path, map_location="cpu")
    iteration = checkpoint_dict["iteration"]
    learning_rate = checkpoint_dict["learning_rate"]
    if optimizer is not None:
        optimizer.load_state_dict(checkpoint_dict["optimizer"])
    saved_state_dict = checkpoint_dict["model"]
    if hasattr(model, "module"):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    new_state_dict = {}
    for k, v in state_dict.items():
        try:
            new_state_dict[k] = saved_state_dict[k]
        except:
            print(f"{k} is not in the checkpoint")
            new_state_dict[k] = v
    if hasattr(model, "module"):
        model.module.load_state_dict(new_state_dict)
    else:
        model.load_state_dict(new_state_dict)
    print(f"Loaded checkpoint {checkpoint_path} (iteration {iteration})")
    return model, optimizer, learning_rate, iteration


def intersperse(lst, item):
    result = [item] * (len(lst) * 2 + 1)
    result[1::2] = lst
    return result


def get_text(text, hps):
    text_norm, clean_text = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm, clean_text


def init_vits_model():
    global DEVICE, hps_ms, net_g_ms

    hps_ms = get_hparams_from_file()
    net_g_ms = SynthesizerTrn(
        len(hps_ms.symbols),
        hps_ms.data.filter_length // 2 + 1,
        hps_ms.train.segment_size // hps_ms.data.hop_length,
        n_speakers=hps_ms.data.n_speakers,
        **hps_ms.model,
    ).to(DEVICE)
    _ = net_g_ms.eval()
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
    length_scale=1.1,
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
