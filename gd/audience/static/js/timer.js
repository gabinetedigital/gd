/* Copyright (C) 2011 Governo do Estado do Rio Grande do Sul
 *
 *   Author: Thiago Silva <thiago@metareload.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

function Timer(interval) {
  var self = this;

  self._interval = interval || 13;
  self._fns = [];
  self._idx = 0;
  self._current = null;
  self._flag = null
  self._running = false;

  //initial stepper
  var step = 0;
  self._stepper = function() {
    return step++;
  };

  self.then = function(fn) {
    self._fns.push(fn);
    return self;
  }

  self.stepper = function(fn) {
    self._stepper = fn;
  }

  self.run = function() {
    self._running = true;
    self._idx = 0;
    self.exec();
  }

  self.exec = function() {

    self._current = setInterval(function() {
      self._fns[self._idx](self, self._stepper(), self._flag)
    }, self._interval);
  }

  self.next = function() {
    clearInterval(self._current);
    self._idx++;
    self._fns[self._idx] ? self.exec() : self.stop();
  }

  self.flag = function(arg) {
    self._flag = arg;
  }

  self.stepper = function(fn) {
    self._stepper = fn;
  }

  self.isRunning = function() {
    return self._running;
  }

  self.stop = function() {
    self._running = false;
    clearInterval(self._current);
  }
}
