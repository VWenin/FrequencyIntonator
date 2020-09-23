# FrequencyIntonator
This is an experimental python script that filters frequencies that belong to a certain key out of audio material in wav form and returns a 'tuned' wav.

Operation is fairly simple. A conversion of a wav to a 'tuned' wav can be as simple as
```python
import FrequencyIntonator as fi

in_path='./input.wav'
out_path='./output.wav'

fi.intonate_frequencies(in_path,out_path)
```

This will return a file tuned to A-major with A=440Hz. To tune to a specific key, one has to provide the frequency of the major key root note. If we wanted to tune to A-Major with A=432, we'd enter

```python
fi.intonate_frequencies(in_path,out_path,432)
```

For A=440Hz equal temperament, frequency shorthands with keywords in the form `_NOTE_FREQ` are provided, which can be used in the following way

```python
fi.intonate_frequencies(in_path,out_path,fi._Gb_FREQ)
```

The frequencies are by default tuned in just intonation, making the result sound more harmonically 'whole'. The tuning system can also be set to equal temperament

```python
fi.intonate_frequencies(in_path,out_path,fi._E_FREQ,system=fi._TEMP)
```

There are two ways to set the window length of the Fourier transform applied. Either one can set the number of samples with the keyword `nperseg`

```python
fi.intonate_frequencies(in_path,out_path,fi._B_FREQ,nperseg=512)
```

or give the window time in seconds (with the closest increment chosen) with the keyword `window_time`

```python
fi.intonate_frequencies(in_path,out_path,fi._B_FREQ,window_time=0.001)
```

`window_time` takes precedence over `nperseg`. A short window will filter out low end and create low mid resonances, a moderate window will preserve lows and low mids but smear the high mids and highs into an organ like tone and a long window will smear all frequencies into ethereal organ-like swells, approximately timed to the input material.

The last parameter is the number of allowed frequencies adjacent to the exact frequencies. This filter `broadness` parameter will filter notes stronger for low values (with the lowest being 1) and will retain more of the input's form for higher values.

```python
fi.intonate_frequencies(in_path,out_path,fi._E_FREQ,broadness=4)
```

This script uses scipy's `wavfile` and is thus restricted to the supported formats, particularly not allowing 24 bit wav files. This script will always return a 32 bit floating point wav.
