#!/usr/bin/env python
"""
vmako - Verilog Mako front end
Copyright (c) 2014 Edmond Cote <edmond.cote@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import argparse
import math
import os
import shutil
import string
import sys
import re

from mako.template import Template
from mako import exceptions


def log2(x):
    return int(math.log(x, 2))


def ev(x):
    return eval(str(x))

def connect(dest, src):
    if src[0] != '':
        return '// connect:dest={} src={}\nassign {}_{} = {}_{};'.format(dest, src, dest[0], dest[1], src[0], src[1])
    else:
        return '// connect:dest={} src={}\nassign {}_{} = {};'.format(dest, src, dest[0], dest[1], src[1])

def instance(file_name, inst_name, **kwargs):
    args = get_args()
    file_name = string.Template(file_name).substitute(os.environ)  # expand environment vars in string

    try:
        template = Template(filename=file_name)
        mako_output = template.render(**kwargs)
    except:
        print exceptions.text_error_template().render()

    # Write output to file
    out_file = get_out_file(args, file_name)
    f = open(out_file, 'a')
    f.write(mako_output)
    f.close()

    module_name = get_module_name(mako_output)
    input_list = get_input_list(mako_output)
    output_list = get_output_list(mako_output)

    input_wire  = ['wire {} {}_{};'.format(i[1], inst_name, i[0]).replace('  ', ' ') for i in input_list]
    output_wire = ['wire {} {}_{};'.format(o[1], inst_name, o[0]).replace('  ', ' ') for o in output_list]

    input_port  = ['.{}({}_{})'.format(i[0], inst_name, i[0]).replace('  ', ' ') for i in input_list]
    output_port = ['.{}({}_{})'.format(o[0], inst_name, o[0]).replace('  ', ' ') for o in output_list]
    port = input_port + output_port

    ret_val = '''\
// ---- instance:{} [begin] ----
{}
{}

{} {} (
 {}
);
// ---- instance:{} [end] ----
'''.format(inst_name, '\n'.join(input_wire), '\n'.join(output_wire), module_name, inst_name, '\n,'.join(port), inst_name)
    return ret_val


def get_module_name(module):
    m = re.search('module\s+(\w+)', module)
    if not m:
        raise Exception('Module name not found')
    return m.group(1)


def get_input_list(module):
    input_list = []
    for line in module.split('\n'):
        m0 = re.search('input\s+([\[\]0-9:]*)\s*(\w+)', line)
        if m0:
            input = list(m0.groups())
            input.reverse()
            input_list.append(input)
    return input_list


def get_output_list(module):
    output_list = []
    for line in module.split('\n'):
        m0 = re.search('output reg\s+([\[\]0-9:]*)\s*(\w+)', line)
        if m0:
            output = list(m0.groups())
            output.reverse()
            output_list.append(output)
    return output_list


def get_args():
    parser = argparse.ArgumentParser(description='Verilog Mako 1.0')
    parser.add_argument('-f','--filename',
                        help='Name of Mako file to process',required=True)
    parser.add_argument('-o','--output_dir', default='.',
                        help='Output dir')
    parser.add_argument('-v','--verbose',
                        help='Verbose output',action='store_true')

    return parser.parse_args()


def get_out_file(args, full_path):
    file_name = os.path.basename(full_path).replace('.mako', '')
    return '{}/{}'.format(args.output_dir, file_name)


def main():
    args = get_args()

    # Clean output directory
    if os.path.exists(args.output_dir):
        shutil.rmtree(args.output_dir)
    os.mkdir(args.output_dir)

    try:
        template = Template(filename=args.filename)
        out_file = get_out_file(args, args.filename)
        f = open(out_file, 'w')
        f.write(template.render(w=4))  # width = 4
        f.close()
    except:
        print exceptions.text_error_template().render()


if __name__ == "__main__":
    main()
