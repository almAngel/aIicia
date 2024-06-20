<img src="icon.png" alt="drawing" width="200"/>

# AIicia

## What is AIicia?

AIicia is an open source tool for content creators to spot certain words inside audio files or videos. This makes possible to check for certain words that you want to censor in order to protect your content monetization, or just simply because you want to make sure if you did say certain word or phrase.

It uses a slightly altered version of WhisperX under the hood.

## What do I need to do prior start?

- You need Python < 3.10 which you can get from https://www.python.org/downloads/release/python-390/ and have python set as a system variable in order to use it as a command.

- You need to install PyTorch https://pytorch.org/get-started/locally/

### CUDA

> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

### NON-CUDA

> pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

## Ok, I have everything. So now?

Now all you got to do is get a video or audio and create a file with the words you want to spot in the video, each in a new line.

Example 1:

> .banned

```
dumb
shit
ass
stupid
... etc
```

Example 2:

> spot.txt

```
monster
motorbike
cake
... etc
```

Then run `python .\transcript.py -f [filename].[ext] --words_list [words_file] -p [processor]` ,
where:

- [filename].[ext] could be **_test.mp4_**.
- [words_file] could be **_.spot_** where all the words to spot in an audio are listed.
- [processor] can be **_cuda_** or **_cpu_**. Default is set to **_cpu_**.

The process will start and the output will be a file with the same name as the video/audio with all the terms selected and their timestamp inside the video with the format **_HH:mm:ss,ms_**. Example of output file:

> output.txt:

```
monster - 00:04:44,112
cake - 00:07:49,052
cherry - 00:08:47,058
motorbike - 00:09:02,029
programming - 00:09:03,530
booger - 00:09:39,080
```

## Can I use it to help me edit videos?

Sure. Use it. But I would appreciate if you could help me:

[![](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://paypal.me/ShiftALM?country.x=ES&locale.x=es_ES)

## Can I contribute?

Please! For sure! I hope people want to make this tool more advanced! It could evolve to a really good open source video editor with really original functionalities.
