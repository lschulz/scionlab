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

import os
from .common import *
import huey

SCIONLAB_SITE = os.environ.get('SCIONLAB_SITE', 'http://localhost:8000')

# ##### DEBUG CONFIGURATION ###############################
ALLOWED_HOSTS = ['*']

# ##### DATABASE CONFIGURATION ############################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'ATOMIC_REQUESTS': True,
    },
}

# ##### HUEY TASK QUEUE CONFIGURATION #####################
HUEY = huey.RedisHuey('scionlab-huey', host='redis')

# ##### APPLICATION CONFIGURATION #########################
INSTALLED_APPS += [
    'django_nose',
]

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# ##### EXTENSIONS CONFIGURATION ##########################

# django-recaptcha2 test keys
RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

# ##### MAILER CONFIGURATION ##############################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ##### VPN CONFIG OVERRIDES ##############################
VPN_CA_KEY_PASSWORD = 'sci0nl4b'
VPN_CA_KEY_PATH = os.path.join(BASE_DIR, 'run', 'dev_root_ca_key.pem')
VPN_CA_CERT_PATH = os.path.join(BASE_DIR, 'run', 'dev_root_ca_cert.pem')