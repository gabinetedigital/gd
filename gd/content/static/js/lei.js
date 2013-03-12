$(document).ready(function(){

	if (HABILITAR_ABAS){
		$(".post-child-title-button").click(function(){
			var icones = $('.img-comments');
			// icones.hide();

			$('.post-child').hide();
			var o = $('#div-aba-'+$(this).attr('data-id'));
			o.show();

			var options = {
			    "my": "right center",
			    "at": "left center",
			    "of": o.find('.post-child-content')
			};
			icones.position(options);
		});
	}

	if (HABILITAR_SANFONA){
	    $(".post-child-content").hide();
	    $(".post-child-title").click(function(){
			var icones = $('.img-comments');
	    	icones.hide();
	        $(".post-child-content").slideUp("slow");
	        var o = $(this).next();
	        o.slideDown("slow", function(){

	        	if(HABILITAR_COMENTARIO_FILHOS && o.attr('data-inibir-comentarios') != 'S'){
			        icones.show();

		        	$('#nomefilho').html( o.attr('data-title') );
		        	$('#form_comentario_filho #post_id').val( o.attr('data-id') );
		        	$('#view-comments').attr('href', '#comentarios'+o.attr('data-id') );

					$('div.error').hide();
		            $('div.success').hide();
					$('#form_comentario_filho textarea').val('');

					var options = {
					    "my": "right center",
					    "at": "left center",
					    "of": o
					};
					icones.position(options);
				}

	        });
	        return false;
	     });
	}else{
		if(HABILITAR_COMENTARIO_FILHOS){
			//Aqui habilita somente os comentários, pois a sanfona está desativada
			var icones = $('.img-comments');
			$('.post-child-content').hover(function(){

		        icones.show();

		        $('#nomefilho').html( $(this).attr('data-title') );
		        $('#form_comentario_filho #post_id').val($(this).attr('data-id'));
		        $('#view-comments').attr('href', '#comentarios'+$(this).attr('data-id') );

				$('div.error').hide();
	            $('div.success').hide();
				$('#form_comentario_filho textarea').val('');

				var options = {
				    "my": "right center",
				    "at": "left center",
				    "of": $(this)
				};
				icones.position(options);

			})
		}
	};

	$("#add-comment").fancybox({
		'scrolling'		: 'no',
		'overlayShow'   : false,
		'titleShow'		: false,
		'autoDimensions': true,
		'width'         : 400,
		'beforeShow'    : function(){
			$('div.error-filho').hide();
			$('div.success-filho').hide();
		}
	});


	$("#view-comments").fancybox({
		'scrolling'		: 'auto',
		'overlayShow'   : false,
		'titleShow'		: false,
		'autoDimensions': true,
		'width'         : 400,
	});

	$('#form_comentario_filho').ajaxForm({
	    beforeSubmit: function () {
	        var form = $('#form_comentario_filho');
	        var field = form.find('textarea');

	        if ($.trim(field.val()) === '') {
	            field.addClass('fielderror');
	            return false;
	        } else {
	            field.removeClass('fielderror');
	        }

	        /* Saving the success callback to be called when the user is
	         * properly logged */
	        var options = this;
	        if (!auth.isAuthenticated()) {
	        	$('div.error-filho').fadeIn().html('É necessário estar logado.');
	            auth.showLoginForm({
	                // success: function () {
	                //     form.ajaxSubmit(options.success);
	                //     return true;
	                // }
	            });
	            return false;
	        }
	        return true;
	    },

	    success: function (data) {
	        var pData = $.parseJSON(data);

	        /* It's everything ok, let's get out */
	        if (pData.status === 'ok') {
	            $('div.error-filho').fadeOut();
	            $('div.success-filho').fadeIn().html(pData.msg);
	            $('#form_comentario_filho textarea').val('');
	            setTimeout('$.fancybox.close()', 2000);
	        } else {
	            $('div.success-filho').fadeOut();
	            $('div.error-filho').fadeIn().html(pData.msg);
	        }
	    }
	});

	$("#btnSearch").click(function () {
		if (HABILITAR_SANFONA){
	        $("div.post-child-content:contains('"+$('#txtSearch').val()+"')").slideDown('slow');
	        $("div.post-child-content:not(:contains('"+$('#txtSearch').val()+"'))").hide();
		}
    });



});
