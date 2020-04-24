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
import os
from IPython.lib import passwd

c.NotebookApp.ip = '*'
c.NotebookApp.port = int(os.getenv('PORT', 8888))
c.NotebookApp.open_browser = False
c.MultiKernelManager.default_kernel_name = 'python3'
c.NotebookApp.token = ''
c.NotebookApp.password = u'sha1:a658c59030b6:910b8fff6920f60a451b19a82e465c60f4880b60'
c.NotebookApp.allow_credentials = True
c.NotebookApp.allow_origin = '*'
c.NotebookApp.allow_remote_access = True
c.NotebookApp.disable_check_xsrf = True
c.NotebookApp.tornado_settings = { 'headers': { 'Content-Security-Policy': "" }}
# sets a password if PASSWORD is set in the environment
# if 'PASSWORD' in os.environ:
#   password = os.environ['PASSWORD']
#   if password:
#     c.NotebookApp.password = passwd(password)
#   else:
#     c.NotebookApp.password = 'quantaxis'
#     c.NotebookApp.token = ''
#   del os.environ['PASSWORD']
