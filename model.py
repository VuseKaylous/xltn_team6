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

import soundfile as sf
import numpy as np
import librosa

class RunModel:
    def __init__(self) -> None:
        # self.model = nemo_asr.models.EncDecCTCModel.load_from_checkpoint("checkpoint.ckpt", map_location='cpu')
        self.model = nemo_asr.models.EncDecCTCModel.restore_from(restore_path="mymodel.nemo", map_location='cpu')

    def get_result(self, path2audio_files) :
        batch_sz = 4
        trans = []
        batch = []
        for i in range(len(path2audio_files)) :
            batch.append(path2audio_files[i])
            if (i % batch_sz == batch_sz - 1) :
                rt = self.model.transcribe(path2audio_files=batch, batch_size=len(batch))
                for _ in rt:
                    trans.append(_)
                batch = []
        rt = self.model.transcribe(path2audio_files=batch, batch_size=len(batch))
        for _ in rt:
            trans.append(_)
        # return model.transcribe(paths2audio_files=path2audio_files, batch_size=len(path2audio_files))
        return trans
    
    def split_wav(self, input_path, output_folder, segment_duration=10):
        y, sr = librosa.load(input_path, sr=None)

        segment_frames = int(segment_duration * sr)
        files = []

        for i in range(0, len(y), segment_frames):
            segment = y[i:i+segment_frames]
            output_file = f"{output_folder}/segment_{i // segment_frames + 1}.wav"
            sf.write(file=output_file, data=segment, samplerate=sr)
            files.append(output_file)
        return files
    
    def solve_a_file(self, input_path):
        split = self.split_wav(input_path, "divided")
        ans = model.get_result(split)
        rt = ""
        for x in ans:
            rt = rt + x + " "
        return (rt, input_path)
    
    def split_many_file(self, input_paths):
        paths = []
        for p in input_paths:
            p.save(p.filename)
            path = self.solve_a_file(p.filename)
            paths.append(path)
        return paths

import sys
import time

if __name__ == '__main__':
    st_time = time.time()

    args = []
    for i in range(1, len(sys.argv)):
        args.append(sys.argv[i])
    
    model = RunModel()
    result = model.split_many_file(args)

    duration = time.time() - st_time
    print("Run time: " + str(duration) + "s\nResult:")
    for (word, fi) in result:
        print("File: " + fi + ", result: " + word)
    print()
    # print(sys.argv[1])