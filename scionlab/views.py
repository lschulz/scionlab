# Copyright 2018 ETH Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class PlaceholderView(View):
    def get(self, request, *args, **kwargs):
        if request.user.id:
            return HttpResponse('Hello, this is a placeholder. You are logged in as %s.' % request.user.username)
        else:
            return HttpResponse('Hello, this is a placeholder. You are not logged in.')


class PlaceholderUserView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, this is a placeholder view with login required. You are logged in as %s' % request.user.username)


