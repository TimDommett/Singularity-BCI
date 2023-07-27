![](https://github.com/TimDommett/Singularity-BCI/blob/TimDommett-uploading-repo-art/singularity_github_bannrt.png?raw=true)

# 🧠 Singularity 🧠

## Thought to Text BCI Project 🧠⌨️

Welcome to our exciting new open source BCI project! This project is a prototype for converting thoughts to text. It trains on your raw EEG brain data using the Neurosity Crown and employs machine learning and a LSTM model to predict what you would type with just your brain data. Get ready to type without typing! 🚀
Credit where credit is due, the data capture component of the platform was originally a fork from the official Neurosity Python SDK, all other parts of the system are part of the Singularity GNU license.

## Documentation 📚

- [Getting Started](#getting-started) 🚀
- [Authentication](#authentication) 🔒
- [Brainwaves](#brainwaves) 🌊
- [Training the Model](#training-the-model) 🏋️‍♀️
- [Predicting Text](#predicting-text) 📝
- [Device Info](#device-info) 📟
- [Device Status](#device-status) 🚦
- [Device Settings](#device-settings) ⚙️

## Getting Started 🚀

To get started with this thought-to-text project, you'll need:

- Your device ID
- Your Neurosity account email
- Your Neurosity account password

To get your 32-character Neurosity device ID, use the Neurosity mobile app available for iOS and Android. Go to `Settings -> Device Info`.

> 💡 Never hardcode your email and password directly in your Python code. Instead, create a `.env` file in the root of your project and add:

```bash
NEUROSITY_EMAIL=your email here
NEUROSITY_PASSWORD=your password here
NEUROSITY_DEVICE_ID=your device id here

```

Once you have these, you're ready to start training your brain to type! 🧠⌨️

## Authentication

We take data privacy very seriously at Neurosity. This is why we have designed the Neurosity OS to require authentication and authorization for streaming data.

When you sign up for an account on the Neurosity mobile app or console.neurosity.co and claim a device you have three new important items: deviceId, email, and password. If your device is not added to your Neurosity account, you will not be able to authenticate with it.

```python
from neurosity import NeurositySDK
from dotenv import load_dotenv
import os

load_dotenv()

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})
```

## Brainwaves

The brainwaves API is what we always wished for when it came to inventing the future: an easy way to get lossless brainwaves. Sometimes we wanted to manipulate the raw data and other times we wanted to analyze the power in each frequency bin. With brainwaves, our goal is to enable new APIs and powerful programs to be built. We expect that someone working with the brainwaves API has a bit of experience working with EEG data or a strong desire to learn.

### Sampling Rate

The sampling rate will vary depending on the model of your device.

- Crown -> 256Hz

A sampling rate of 250Hz means the data contains 250 samples per second.

### Metrics

There are four brainwaves metrics:

- raw
- rawUnfiltered
- psd
- powerByBand

### Raw

The `raw` brainwaves parameter emits events of 16 samples for Crown and 25 for Notion 1 and 2. We call these groups of samples Epochs.

```python
from neurosity import NeurositySDK
from dotenv import load_dotenv
import os

load_dotenv()

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

def callback(data):
    print("data", data)

unsubscribe = neurosity.brainwaves_raw(callback)
```

The code above will output new epochs of 16 samples approximately every 62.5ms (see the `data` property). Here's an example of 1 event:

```
{
  label: 'raw',
  data: [
    [
        4.457080580994754,   4.851055413759571,
       2.7564288713972513, -0.5027899221971044,
       -2.738312652550817, -1.4222768509324195,
       3.7224881424127774,  10.026623768677425,
       13.387940036943913,   10.26958811063134,
      0.40214439930276313,  -10.90689891807639,
       -16.32031531728357,  -13.21110292437311,
       -4.346339152926361,   5.098462672115731
    ],
    [
       1.5414324608328491,   1.352550875105505,
       0.6428681224481866,  0.3647622839064659,
        1.106405158893898,    3.33535030106603,
        6.439447624257519,   8.453867322080404,
        7.755719477492251,  3.8854840128526726,
       -2.468418708869076,  -8.666576946507902,
      -11.279063910921169,   -9.32163910159064,
      -4.6549399985975555, 0.22830321396497988
    ],
    [
       6.2342484244030345,   5.845156697083605,
       3.8819440822537112,   1.452431055127227,
      -0.5878084105038387, -0.7746780077287738,
       1.8154316196085094,   6.074662974618359,
        9.322430831260775,   8.910160063433407,
       3.5874046672323043,  -4.554187036159066,
        -10.5813322711113, -11.267696723897789,
       -6.818338145262863,  0.6177864457464617
    ],
    [
      -0.03815349843983071, -0.3068494494059635,
       -2.2075671327003255,  -3.776991642244289,
        -3.708252867923816, -1.2505125622236009,
        3.2487010722502587,   7.931368090269462,
        10.511652358411597,   9.297157466389192,
         4.118487064147775,  -2.970255165231891,
        -8.603434324519576, -10.495401970387743,
        -8.913968355428027,  -5.576315727924461
    ],
    [
      0.4087987173450871, 1.9781686568610883,
      2.4009012312957907, 2.3444623435812657,
       2.017191526524595,  2.021880260660721,
       2.982232584662937,  4.815498699074363,
      6.7093290202119835,  7.201157697368587,
       5.116090777276677, 0.6675802498302112,
      -4.274751517565271, -7.425134286013973,
      -7.838523284654038, -5.779233789541195
    ],
    [
       5.2762700288652935,   6.831919893235682,
        6.468141714172544,   5.147606136919876,
        4.117592132996127,   4.788874365858218,
        7.116782027901927,    9.33554991116211,
        9.233167024756574,   5.130966403760715,
      -2.8162586562506586,  -11.22160733448037,
      -15.538132012307846, -13.939535958562475,
        -7.83032193319038, -0.5139467086717411
    ],
    [
      -1.0706877843314648,  1.6368537502872518,
        2.022946637839514,   0.940183871324582,
      -0.2837858448921892,  0.3170369574339986,
        3.778225479624427,   8.805770181583913,
       12.446309024446833,  11.648691354684154,
        5.113617281379798,  -4.345975093596486,
       -11.05811376487729, -11.719256256733335,
       -7.336025188705039,  -1.276174494743728
    ],
    [
        7.286685329938873,    8.201842402616839,
        5.517128178717949,   1.2864058791627557,
      -1.5101995538838966, -0.19819079250913285,
        5.195437241439434,   11.512563735679437,
       14.388370410845482,   10.711863367882668,
       0.8428177428317678,  -10.126402143316568,
       -15.75585412249734,  -13.887360795976967,
       -6.836657125920971,   1.1706118773123455
    ]
  ],
  info: {
    channelNames: [
      'CP3', 'C3',
      'F5',  'PO3',
      'PO4', 'F6',
      'C4',  'CP4'
    ],
    notchFrequency: '60Hz',
    samplingRate: 256,
    startTime: 1628194299499
  }
}
```

Epochs are pre-filtered on the device's Operating System to give you the cleanest data possible with maximum performance. These filters include:

- Notch of `50Hz` or `60Hz` and a bandwidth of `1`.
- Band Pass with cutoff between `2Hz` and `45Hz`.

The order of these filters is set to `2`, and the characteristic used is `butterworth`.

To apply your own filters, you can use the `brainwaves_raw_unfiltered` SDK method (see next section) and use a library like MNE or Brainflow for fine-grained filter customization.

#### Unsubscribe from brainwaves

To unsubscribe from brainwaves and stop the emission of data events, you can do the following:

```python
unsubscribe = neurosity.brainwaves_raw(callback)

timer.sleep(5)

unsubscribe()
```

This last example will emit data for 5 seconds.

### Raw Unfiltered

The unfiltered raw data follows the same shape as `brainwaves_raw` data shape, just without signal filters applied. This data comes directly from the analog to digital converter, and does not include any processing. We only recommend using the unfiltered data for advanced scenarios.

Note that unfiltered raw data will include environmental noise in the signal, as well as DC drift, which is expected when working with EEG.

```python
from neurosity import NeurositySDK
from dotenv import load_dotenv
import os

load_dotenv()

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

def callback(data):
    print("data", data)

unsubscribe = neurosity.brainwaves_raw_unfiltered(callback)
```

The code above will output new epochs of 16 samples approximately every 62.5ms (see the `data` property).. Here's an example of 1 event:

```
{
  label: 'rawUnfiltered',
  data: [
    [
       1385.227003,   861.056247,
      -1835.167617, -1321.189256,
        999.860579,  1414.597195,
      -1246.623837, -1840.934367,
        406.757043,  1596.652153,
       -476.360375, -2080.790935,
       -222.556318,  1579.754234,
        355.660956, -2065.368232
    ],
    [
        774.21972,    286.25879,
      -951.714922,  -427.812387,
       650.368705,   611.744891,
      -746.391799,    -732.3102,
       398.039863,   770.732848,
       -412.99318,  -923.417614,
       122.174635,   823.840593,
         7.040799, -1004.286225
    ],
    [
       797.085555,   234.693316,
       -1099.4376,  -499.427375,
       669.613557,   598.870286,
      -859.916308,  -839.665628,
       420.369256,    765.63665,
      -515.185355,  -1057.66219,
       114.195062,   849.388636,
       -42.177742, -1155.495775
    ],
    [
       192.783795, -156.909245,
      -538.654687, -173.673053,
       210.084045,   13.008715,
      -496.208724, -314.354932,
       130.355373,  111.244632,
      -422.783244, -437.267174,
        43.116515,  179.573914,
      -267.952711, -512.234925
    ],
    [
       228.256013, -147.253292,
      -549.249414, -160.731394,
       234.961536,   16.093256,
      -506.803451, -304.162537,
       164.553542,   135.31746,
      -437.870671, -440.217605,
        71.212657,  207.267725,
       -272.04308, -523.634314
    ],
    [
        654.66024,   123.64985,
      -906.720861, -336.013773,
       578.217274,  426.337171,
      -751.487996, -629.246306,
       371.821267,  573.791629,
      -480.853076,  -827.26041,
       143.028812,  673.435705,
      -121.839358, -934.682893
    ],
    [
       764.362601,   258.095592,
      -996.172541,  -464.826875,
       639.975144,   603.094766,
      -765.368429,  -772.208063,
       384.829982,   745.453025,
       -437.46834,  -963.851919,
        93.139719,   807.747337,
       -22.865834, -1044.519364
    ],
    [
       1454.293893,   821.493659,
      -1599.334362,  -991.813951,
       1131.892333,  1364.506936,
      -1098.431772, -1494.459978,
        603.228876,  1578.815461,
        -421.71036, -1753.024956,
         21.860006,  1608.252708,
        343.859235, -1787.089015
    ]
  ],
  info: {
    channelNames: [
      'CP3', 'C3',
      'F5',  'PO3',
      'PO4', 'F6',
      'C4',  'CP4'
    ],
    samplingRate: 256,
    startTime: 1628194299499
  }
}
```


## Code of Conduct

This project has adopted a [Code of Conduct](CODE_OF_CONDUCT.md). 

## License for Singularity Software

This project is licensed under the [GNU General Public License v3.0](LICENSE). 
 
This means that you can copy, modify, distribute and even sell this software, but you must make your changes available to others under the same license. We believe in the power of open source and are committed to ensuring this 
 project remains open and free for all. 🌍🚀  

## License for Neurosity Software

Copyright (c) Neurosity, Inc. All rights reserved.

Originally licenced under the [MIT license](LICENSE).

## Note on Dual License Structure

The MIT license applies to any data capture component of the repository, however any training, predicition or any other software developed as part of the Singularity BCI platform is covered under the GNU license.
