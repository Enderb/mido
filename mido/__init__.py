# -*- coding: utf-8 -*-
"""
MIDI Objects for Python

Mido is a library for working with MIDI messages and ports. It's
designed to be as straight forward and Pythonic as possible.

Creating messages:

    Message(type, **parameters) -- create a new message
    MetaMessage(type, **parameters) -- create a new meta message

Frozen messages (immutable and hashable):

    FrozenMessage(type, **parameters)
    FrozenMetaMessage(type, **parameters)
    freeze(msg)

Ports:

    open_input(name=None, virtual=False, callback=None) -- open an input port
    open_output(name=None, virtual=False,               -- open an output port
                autoreset=False)
    open_ioport(name=None, virtual=False,        -- open an I/O port (capable
                callback=None, autoreset=False)     of both input and output)

    get_input_names() -- return a list of names of available input ports
    get_output_names() -- return a list of names of available output ports
    get_ioport_names() -- return a list of names of available I/O ports

MIDI files:

    MidiFile(filename, **kwargs) -- open a MIDI file
    MidiTrack()  -- a MIDI track
    bpm2tempo()  -- convert beats per minute to MIDI file tempo
    tempo2bpm()  -- convert MIDI file tempo to beats per minute
    merge_tracks(tracks)  -- merge tracks into one track

SYX files:

    read_syx_file(filename)  -- read a SYX file
    write_syx_file(filename, messages,
                   plaintext=False)  -- write a SYX file
Parsing MIDI streams:

    parse(bytes) -- parse a single message bytes
                    (any iterable that generates integers in 0..127)
    parse_all(bytes) -- parse all messages bytes
    Parser -- MIDI parser class

Parsing objects serialized with str(message):                                  

    parse_string(string) -- parse a string containing a message
    parse_string_stream(iterable) -- parse strings from an iterable and
                                     generate messages
 
Sub modules:

    ports -- useful tools for working with ports
"""
from __future__ import absolute_import
import os
from .backends.backend import Backend
from . import ports, sockets
from .messages import Message
from .messages import parse_string, parse_string_stream, format_as_string
from .frozen import FrozenMessage, FrozenMetaMessage, freeze
from .parser import Parser, parse, parse_all
from .midifiles import MidiFile, MidiFileError, MidiTrack, merge_tracks
from .midifiles import MetaMessage, bpm2tempo, tempo2bpm
from .syx import read_syx_file, write_syx_file

__author__ = 'Ole Martin Bjorndalen'
__email__ = 'ombdalen@gmail.com'
__url__ = 'https://mido.readthedocs.io/'
__license__ = 'MIT'
__version__ = '1.1.18'

# Prevent splat import.
__all__ = []

def set_backend(name=None, load=False):
    """Set current backend.

    name can be a module name like 'mido.backends.rtmidi' or
    a Backend object.

    If no name is passed, the default backend will be used.

    This will replace all the open_*() and get_*_name() functions
    in top level mido module. The module will be loaded the first
    time one of those functions is called."""

    glob = globals()

    if isinstance(name, Backend):
        backend = name
    else:
        backend = Backend(name, load=load, use_environ=True)
    glob['backend'] = backend

    for name in dir(backend):
        if name.split('_')[0] in ['open', 'get']:
            glob[name] = getattr(backend, name)

set_backend()

del os, absolute_import
