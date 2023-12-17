import os
try:
    from ruamel.yaml import YAML
except ModuleNotFoundError:
    from ruamel_yaml import YAML

# NeMo's "core" package
import nemo
# NeMo's ASR collection - this collections contains complete ASR models and
# building blocks (modules) for ASR
import nemo.collections.asr as nemo_asr
from omegaconf import DictConfig
import copy
import pytorch_lightning as pl
import torch

model = nemo_asr.models.EncDecCTCModel.load_from_checkpoint("checkpoint.ckpt", map_location='cpu')

def get_result(path2audio_files) :
    batch_sz = 4
    trans = []
    batch = []
    for i in range(len(path2audio_files)) :
        batch.append(path2audio_files[i])
        if (i % batch_sz == batch_sz - 1) :
            rt = model.transcribe(path2audio_files=batch, batch_size=len(batch))
            for _ in rt:
                trans.append(_)
            batch = []
    rt = model.transcribe(path2audio_files=batch, batch_size=len(batch))
    for _ in rt:
        trans.append(_)
    # return model.transcribe(paths2audio_files=path2audio_files, batch_size=len(path2audio_files))
    return trans

import sys
import time

if __name__ == '__main__':
    st_time = time.time()

    args = []
    for i in range(1, sys.argv):
        args.append(sys.argv[i])

    print(get_result(args))
    # print(sys.argv[1])