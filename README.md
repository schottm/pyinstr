# PyINSTR

![Release](https://img.shields.io/github/v/release/schottm/pyinstr)
![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)

A simple and robust instrumentation framework with easy virtualization.

This project takes strong inspiration from [PyMeasure](https://github.com/pymeasure/pymeasure) while addressing and improving upon some of its limitations, particularly strict typing.
Furthermore, it offers a straightforward method for instrument virtualization, enabling the development of larger projects off-site when physical instruments are unavailable or disconnected.

## Requirements

- Python 3.12+ (tested on 3.13)
- VISA drivers for the connected instruments (NI-VISA, lakeshore, etc.)

## Getting Started

You can download the wheel from [here](https://github.com/schottm/pyinstr/releases/latest) or just clone and add the library manually to your python project. 

```shell
# wheel
pip install <file>.whl

# clone
git clone https://github.com/schottm/pyinstr
cd <your-project>
pip install [-e] <pyinstr-directory>
```

## Usage

PyINSTR comes with a limited selection of predefined instruments and implemented controls.
To access an instrument, you only need to specify the connection and the type of instrument.

```python
from pyinstr.instruments import Keithley2182
from pyinstr.adapters import VISAAdapter

# connect to a Keithley2182 using a GPIB connection.
instr = Keithley2182(VISAAdapter.make_gpib(1))

# print instrument identity (*IDN?)
print(instr.identity)
```

While developing bigger control software, instruments are often not available for debugging. For this case, the library provides an easy way to virtualize instruments with the function 'make_virtual'. Individual instances that are created using this method behave like a normal Python class, with each control returning a default value of the correct type, even if no value is explicitly provided.

```python
from pyinstr.instruments import Keithley2182
from pyinstr import make_virtual

# create a virtual Keithley2182
instr = make_virtual(Keithley2182)

print(instr.identity) # 
print(type(instr.function)) # <enum 'ChannelFunction'>
print(instr.read) # 0.0
```

If you want to create a new or extend the interface/controls of any instrument please take a look at the [examples](examples).

## To-Do

- [ ] Add a virtual class cache.
- [ ] Add support controls of unitful quantities (e.g. using pint). 
- [ ] Create missing examples.

## License

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for details.
