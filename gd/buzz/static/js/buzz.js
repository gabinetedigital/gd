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


function Buzz(base_url, params, updatepage) {
    var args = $.extend({
        new_buzz: function (msg) {},
        buzz_accepted: function (msg) {},
        buzz_selected: function (msg) {},
        buzz_removed: function (msg) {},
        buzz_published: function (msg) {},
        buzz_unpublished: function (msg) {},
        buzz_all: function (msg) {},
        done: function() {}
    }, params);

    var public_ids = [];
    var moderated_ids = [];
    var selected_ids = [];
    var last_published_id = 0;
    var allbuzz_ids = [];
    
    var receiver = {
        public: function(notices) {
            $.each(notices, function() {
                if ($.inArray(this.id,public_ids) == -1) {
                    public_ids.push(this.id);
                    args.new_buzz(this);
                }
            });
        },
        moderated: function(notices) {
            $.each(notices, function() {
                if ($.inArray(this.id, moderated_ids) == -1) {
                    moderated_ids.push(this.id);
                    args.buzz_accepted(this);
                }
            });
        },
        selected: function(notices) {
            $.each(notices, function() {
                if ($.inArray(this.id,selected_ids) == -1) {
                    selected_ids.push(this.id);
                    args.buzz_selected(this);
                }
            });
        },
        published: function(notice) {
            if (notice && last_published_id != notice.id) {
                args.buzz_published(notice);
                last_published_id = notice.id;
            }
        },
        public_all: function(notices) {
        	$.each(notices, function() {
        		allbuzz_ids.push(this.id);
                args.buzz_all(this);	
            });
        }
    }

    _recv = []
    if(!updatepage){
    
	    function request_notices(first) {
	        $.ajax({
	            url: base_url+'audience/'+AUDIENCE_ID+'/buzz_stream',
	            type: 'GET',
	            data: {public_limit:first?-1:10,
	                   public_ids:public_ids,
	                   selected_ids:selected_ids,
	                   moderated_ids:moderated_ids,
	                   last_published_id:last_published_id,
	                  },
	            success: function(data) {
	                var json = JSON.parse(data);
	                _recv.push(json);
	                var types = ['public','moderated','selected','published'];
	                $.each(types, function() {
	                    receiver[this](json[this]);
	                });
	                args.done();
	            }
	        });
	    }
	    
	    setInterval(request_notices, 3000);
	    request_notices(true);
    
    } else {
    
	    function request_notices_all() {
	        $.ajax({
	            url: base_url+'audience/'+AUDIENCE_ID+'/all_stream',
	            type: 'POST',
	            data: {allbuzz_ids:allbuzz_ids},
	            success: function(data) {
	                var json = JSON.parse(data);
	                _recv.push(json);
	                var types = ['public_all'];
	                $.each(types, function() {
	                    receiver[this](json[this]);
	                });
	                args.done();
	            }
	        });
	    }
	    
	    request_notices_all();
    
    }
}

