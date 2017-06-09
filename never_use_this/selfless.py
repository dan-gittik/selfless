import io
import functools
import opcode
import struct
import types


def selfless(cls):
    for key, value in vars(cls).items():
        if callable(value):
            value = add_self(value)
            setattr(cls, key, value)
    return cls


def disassemble(function):
    bytecode = io.BytesIO(function.__code__.co_code)
    while True:
        # Read the next opcode.
        op = bytecode.read(1)
        # If we're done, break.
        if not op: 
            break
        op, = struct.unpack('<b', op) 
        arg = None
        # If it's a high opcode, then it also has a 2-byte argument.
        if op > opcode.HAVE_ARGUMENT:
            arg, = struct.unpack('<h', bytecode.read(2))
        yield op, arg


def add_self(function):
    code     = function.__code__
    index    = code.co_names.index('self')
    bytecode = []
    for op, arg in disassemble(function):
        # Increase argument of LOAD/STORE_FAST (because we're adding self to varnames).
        if op in (opcode.opmap['LOAD_FAST'], opcode.opmap['STORE_FAST']):
            arg += 1
        # Change LOAD_GLOBAL of self to LOAD_FAST.
        elif op == opcode.opmap['LOAD_GLOBAL'] and arg == index:
            op, arg = opcode.opmap['LOAD_FAST'], 0
        # Change STORE_GLOBAL of self to STORE_FAST.
        elif op == opcode.opmap['STORE_GLOBAL'] and arg == index:
            op, arg = opcode.opmap['STORE_FAST'], 0
        # Decrease argument of LOAD/STORE_GLOBAL/NAME/ATTR if it's after index (because we're removing self from names).
        elif op in (opcode.opmap['LOAD_NAME'], opcode.opmap['STORE_NAME'],
                    opcode.opmap['LOAD_ATTR'], opcode.opmap['STORE_ATTR'],
                    opcode.opmap['LOAD_GLOBAL'], opcode.opmap['STORE_GLOBAL']):
            if arg > index:
                arg -= 1
        bytecode.append(struct.pack('<b', op))
        if arg is not None:
            bytecode.append(struct.pack('<h', arg))
    names     = tuple(name for name in code.co_names if name != 'self')
    varnames  = ('self',) + code.co_varnames
    code_args = [
        code.co_argcount + 1, # Add self to arguments.
        code.co_nlocals + 1,  # Add self to locals.
        code.co_stacksize,
        code.co_flags,
        b''.join(bytecode),   # Changed bytecode.
        code.co_consts,
        names,                # Remove self from names.
        varnames,             # Add self to varnames.
        code.co_filename,
        code.co_name,
        code.co_firstlineno,
        code.co_lnotab,
        code.co_freevars,
        code.co_cellvars,
    ]
    # Python 3 code object difference:
    if hasattr(code, 'co_kwonlyargcount'):
        code_args.insert(1, code.co_kwonlyargcount)
    function.__code__ = types.CodeType(*code_args)
    return function
