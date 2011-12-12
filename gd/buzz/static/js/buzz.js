/* Copyright (C) 2011 Governo do Estado do Rio Grande do Sul
 *
 *   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
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


function Buzz(base_url, params) {
    var args = $.extend({
        new_buzz: function (msg) {},
        buzz_accepted: function (msg) {},
        buzz_selected: function (msg) {},
        buzz_removed: function (msg) {},
        buzz_published: function (msg) {},
        buzz_unpublished: function (msg) {},
        done: function() {}
    }, params);

    var last_public_id = 0;
    var moderated_ids = [];
    var selected_ids = [];
    var last_published_id = 0;

    var requests = 0;
    function compute_requests() {
        requests++;
        if (requests == 4) {
            requests = 0;
            args.done();
        }
    }

    setInterval(function () {
        $.ajax({
            url: base_url+'audience/'+AUDIENCE_ID+'/public_buzz',
            type: 'get',
            data: {from_id:last_public_id},
            success: function(data) {
                var notices = JSON.parse(data);
                if (notices.length > 0) {
                    last_public_id = notices[0].id;
                    $.each(notices, function() {
                        args.new_buzz(this);
                    });
                }
                compute_requests();
            }
        });

        $.ajax({
            url: base_url+'audience/'+AUDIENCE_ID+'/moderated_buzz',
            type: 'get',
            success: function(data) {
                var notices = JSON.parse(data);
                $.each(notices, function() {
                    if (moderated_ids.indexOf(this.id) == -1) {
                        moderated_ids.push(this.id);
                        args.buzz_accepted(this);
                    }
                });
                compute_requests();
            }
        });

        $.ajax({
            url: base_url+'audience/'+AUDIENCE_ID+'/selected_buzz',
            type: 'get',
            success: function(data) {
                var notices = JSON.parse(data);
                $.each(notices, function() {
                    if (selected_ids.indexOf(this.id) == -1) {
                        selected_ids.push(this.id);
                        args.buzz_selected(this);
                    }
                });
                compute_requests();
            }
        });

        $.ajax({
            url: base_url+'audience/'+AUDIENCE_ID+'/last_published',
            type: 'get',
            success: function(msg) {
                var notice = JSON.parse(msg);
                if (notice && last_published_id != notice.id) {
                    last_published_id = notice.id;
                    args.buzz_published(notice);
                }
                compute_requests();
            }
        });
    }, 2000);
}
