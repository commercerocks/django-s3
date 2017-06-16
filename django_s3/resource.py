"""
Copyright (2017) Raydel Miranda 

This file is part of Django-S3.

    Django-S3 is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Django-S3 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Django-S3.  If not, see <http://www.gnu.org/licenses/>.
"""

import re

from django.utils.translation import ugettext_lazy as _

from django_s3.category import Category
from django_s3.exceptions import ResourceError, ResourceNameError
from django_s3.s3_settings import django_s3_settings

url_pattern = re.compile(r'^(?P<folder_name>[\w-]+)_[\w-]+\.(?P<extension>\w{3})$')
cat_pattern = re.compile(r'^(?P<category_code>[A-Z]+)\d+.+$')


class Resource(object):
    """
    Represents a resource in a bucket
    """

    def __init__(self, name):
        self.__name = name
        self.__category = Category()
        self.__url = None

    def __compute_url(self):
        match = url_pattern.match(self.__name)
        if match is not None:

            BASE_URL = django_s3_settings.S3_AWS_BASE_URL
            BASE_URL = BASE_URL[:-1] if BASE_URL.endswith('/') else BASE_URL

            return "{}/{}/{}/{}".format(
                BASE_URL,
                django_s3_settings.S3_BUCKET_NAME,
                match.groupdict()['folder_name'],
                self.__name
            )
        else:
            raise ResourceNameError()

    @property
    def name(self):
        return self.__name

    @name.getter
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise ResourceError(_("This attribute is readonly, is set at creation time."))

    @property
    def category(self):
        return self.__category

    @category.getter
    def category(self):
        match = cat_pattern.match(self.__name)
        if match is not None:
            return django_s3_settings.S3_CATEGORY_MAP[match.groupdict()['category_code']]

    @category.setter
    def category(self, value):
        raise ResourceError(_("This attribute is readonly, see S3_CATEGORY_MAP."))

    @property
    def url(self):
        return self.__url

    @url.getter
    def url(self):
        if self.__url is None:
            self.__url = self.__compute_url()
        return self.__url

    @url.setter
    def url(self, value):
        raise ResourceError(_("This attribute readonly, It is calculated using the resource name"))

    @property
    def code(self):
        pass

    @code.getter
    def __get_code(self):
        raise ResourceError(_("This attribute readonly, It is calculated using the resource name"))

    @code.setter
    def __set_code(self, value):
        pass
