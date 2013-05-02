#!/usr/bin/env python
#
# Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
#
#   Author: Sérgio Berlotto <sergio.berlotto@gmail.com>
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

"""The consumer of SME webservice"""

import requests
import json
from app import conf

class Obra(object):

	def __init__(self, dados):
		self.__dict__.update(dados)


class SMEApi(object):

	def __init__(self):
		self.sme_url = conf.SME_WS_URL

	def _connect(self):
		self.connected = True

	def get_obras(self):
		dados = {
			'obras' : [{'id':1,'titulo':'Obra da OSPA'}],
			'total' : 1
		}
		if not self.connected:
			self._connect()

		return json.dumps(dados)

	def put_evidencia(self):
		pass


def process_sme():

	sme = SMEApi()
	obras = sme.get_obras()
	for obra in obras:
		print "Obra"
		pass

if __name__=='__main__':
	process_sme()
