from whisperX import whisperx
import time, argparse
import os
from datetime import datetime

start_time= time.perf_counter()
parser= argparse.ArgumentParser()
parser.add_argument("-f")
parser.add_argument("--filename")
parser.add_argument("--words_list")
parser.add_argument("-p")

# parser.add_argument("--save_path")
args= parser.parse_args()

def seconds_to_srt_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)
    return "{:02}:{:02}:{:02},{:03}".format(
        int(hours), int(minutes), int(seconds), int(milliseconds * 1000)
    )

if args.f or args.filename:

    if args.words_list: 
        _spot = []
        with open(f"{args.words_list}", 'r', encoding='utf-8') as wordsfile:
            _spot = wordsfile.read().splitlines()
            wordsfile.close()

        print(args.filename)
        print(f'To spot: {_spot}')

        device = "cpu"
        if args.p:
            if args.p == "cuda":
                device = "cuda"
            if args.p == "cpu":
                device = "cpu"

        audio_file = (args.f or args.filename)
        model_size = 'medium'
        batch_size = 1 # reduce if low on GPU mem
        compute_type = "int8" # change to "int8" if low on GPU mem (may reduce accuracy)

        print(f'AUDIO_FILE=\'{audio_file}\' PROCESSOR={device} MODEL_SIZE={model_size} BATCH_SIZE={batch_size} COMPUTE_TYPE={compute_type}')

        # 1. Transcribe with original whisper (batched)
        model = whisperx.load_model(model_size, device, compute_type=compute_type, language='es')

        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=batch_size, print_progress=True)
        # print(result["segments"]) # before alignment

        # delete model if low on GPU resources
        # import gc; gc.collect(); torch.cuda.empty_cache(); del model

        # 2. Align whisper output
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False, print_progress=True, spot=_spot)

        # print(result) # after alignment

        if not os.path.exists("/data/results"):
            os.makedirs("/data/results")

        with open(f'/data/results/{os.path.basename(audio_file).split(".")[0]}-{datetime.now()}.txt', 'w', encoding='utf-8') as finalfile:
            for word in result['word_segments']:
                for s in _spot:
                    if s in word['word'].lower():
                        finalfile.write(f'{word["word"]} - {seconds_to_srt_time(word["start"])}\n')

            finalfile.close()

        end_time = time.perf_counter()

        diff = end_time - start_time

        print(f"Elapsed time: {seconds_to_srt_time(diff)}")
    else:
        print("\n>> ERROR: Please, provide a banned words list using --words_list. Eg: python .\\transcript.py -f audio.mp3 --banned_list .banned")

else: 
    print("\n>> ERROR: Please, pass a file name using -f or --filename. Eg: python .\\transcript.py -f audio.mp3")