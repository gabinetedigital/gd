/*
	jAni jQuery Plugin
	© 2009 ajaxBlender.com
	For any questions please visit www.ajaxblender.com 
	or email us at support@ajaxblender.com
*/

;(function($){
	var settings = {}; 
	var element = {};
	var currFrame = 0;
	var tm = null;
	
	$.fn.jani = function(sett){
		element = $(this);
		settings = $.extend({}, $.fn.jani.defaults, sett);
        
		function _build(){
			element.width(settings.frameWidth);
			element.height(settings.frameHeight);
			element.css('background-position', '0 0');
		};
		
		//    Entry point
		_build();
	};

	$.fn.jani.pause = function(){
		if(tm){ clearTimeout(tm); }
		tm = null;
	}
	
	$.fn.jani.stop = function(){
		if(tm){ clearTimeout(tm); }
		tm = null;
		currFrame = 0;
		element.css('background-position', '0 0');
	}
	
	$.fn.jani.pause = function(){
		clearTimeout( tm );
		tm = null;
	}
	
	$.fn.jani.play = function(){
		if(settings.totalFrames <= 0 || !element || !element.length){ return; }
		
		function _animate(){
			var tmFn = function(){ _animate(); };
			var bgPos = element.css('background-position');
			var ie = true;
			
			if(bgPos == 'undefined' || bgPos == null){
				bgPos = parseInt(element.css('background-position-y'));
			} else {
                bgPos = bgPos.split(' ');
                bgPos = parseInt(bgPos[1]);
                ie = false;
			}
		
			bgPos -= settings.frameHeight - 1;
			
			if(ie){ element.css('background-position-y', bgPos + 'px'); } 
			else { element.css('background-position', ('0px ' + bgPos + 'px')); }
			
			currFrame++;
			if(currFrame > (settings.totalFrames - 1)){
				currFrame = 0;
				element.css('background-position', '0 0');
				
				if(!settings.loop){ return; }
			}
			tm = setTimeout(tmFn, settings.speed);
		}
		
		if(tm){ element.jani.stop(); }
		_animate();
	}
	
    /*  Default Settings  */
    $.fn.jani.defaults = {
        frameWidth:      100,
        frameHeight:     100,
        speed:           100,
        totalFrames:     0,
        loop:            true
    };
		
})(jQuery);