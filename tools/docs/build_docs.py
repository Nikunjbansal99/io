# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Modified from the tfdocs example api reference docs generation script.

This script generates API reference docs.

Build whl file in wheelhouse, note:
1) The `docker` installation is needed.
2) There are 4 whl files in wheelhouse for 2.7, 3.5, 3.6, 3.7
   The `Install pre-requisites` will selectively only install one version.

$ bash -x -e .travis/python.release.sh

Install pre-requisites.

$> python -m pip pip install -U git+https://github.com/tensorflow/docs
$> python -m pip install wheelhouse/tensorflow_io-*-cp$(python -c 'import sys; print(str(sys.version_info[0])+str(sys.version_info[1]))')*.whl

Generate Docs:

$> from the repo root run: python tools/docs/build_docs.py

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from absl import app
from absl import flags

import tensorflow_io as tfio

from tensorflow_docs.api_generator import generate_lib
from tensorflow_docs.api_generator import parser
from tensorflow_docs.api_generator import public_api

from tensorflow.python.util import tf_inspect

# Use tensorflow's `tf_inspect`, which is aware of `tf_decorator`.
parser.tf_inspect = tf_inspect

PROJECT_SHORT_NAME = 'tfio'
PROJECT_FULL_NAME = 'TensorFlow I/O'

FLAGS = flags.FLAGS

flags.DEFINE_string(
    'git_branch',
    default='master',
    help='The name of the corresponding branch on github.')

flags.DEFINE_string(
    'output_dir',
    default='docs/api_docs/python/',
    help='Where to write the resulting docs to.')


def main(argv):
    if argv[1:]:
        raise ValueError('Unrecognized arguments: {}'.format(argv[1:]))

    code_url_prefix = ('https://github.com/tensorflow/io/tree/'
                       '{git_branch}/tensorflow_io'.format(
                           git_branch=FLAGS.git_branch))

    doc_generator = generate_lib.DocGenerator(
        root_title=PROJECT_FULL_NAME,
        # Replace `tensorflow_docs` with your module, here.
        py_modules=[(PROJECT_SHORT_NAME, tfio)],
        code_url_prefix=code_url_prefix,
        private_map={'tfio': ['__version__', 'utils', 'version']},
        # This callback cleans up a lot of aliases caused by internal imports.
        callbacks=[public_api.local_definitions_filter])

    doc_generator.build(FLAGS.output_dir)

    print('Output docs to: ', FLAGS.output_dir)


if __name__ == '__main__':
    app.run(main)