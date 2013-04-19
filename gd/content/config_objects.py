# -*- coding: UTF-8 -*-
# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Sergio Berlotto <sergio.berlotto@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gd.content.wp import wordpress

class WordpressConfiguration(object):

	def __init__(self):
		"""
			Method that read the xml-rpc method from wordpress and
			set all dictionary content to this class,  to configure
			the Flask app.
		"""
		print "Configurando via WORDPRESS..."
		CONFIGS_WP = {}
		CONFIGS_WP = wordpress.gabdig.getConfiguration()
		for key in CONFIGS_WP:
			setattr(self, key.upper(), CONFIGS_WP[key])
