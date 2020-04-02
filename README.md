# Sequences

- Linear Feedback Shift Register, LFSR. The Fibonacci Implementation.
- Gold sequence (constructed with 2 maximum length sequences (MLS) LFSR).
- Zadoff-Chu


## Setup
IF you whish to work in a virtual environment, run
```sh
VENV=$HOME/VirtualEnvironments/sequences

python3 -m venv $VENV
source $VENV/bin/activate

pip3 install -U pip
pip3 install -U -r requirements.txt
```
Will create a python3 venv environment in your home-folder, in $HOME/VirtualEnvironments/sequences.
It will also download numpy.

Else, if you don't whish to use venv you will need python3 and numpy.

## Run
```
python3 sequences/Gold.py
```

## Ref
[Wikipedia: Gold code](https://en.wikipedia.org/wiki/Gold_code)

[Wikipedia: LFSR (The Fibonacci Implemenation)](https://en.wikipedia.org/wiki/Linear-feedback_shift_register#Fibonacci_LFSRs)

[Wikipedia: Maximum Length Sequences (MLS)](https://en.wikipedia.org/wiki/Maximum_length_sequence)

[NewWaveInstruments (WebArchive)](http://web.archive.org/web/20180419035811/http://www.newwaveinstruments.com/resources/articles/m_sequence_linear_feedback_shift_register_lfsr.htm)
