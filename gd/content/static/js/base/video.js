/* Copyright (C) 2013  Guilherme Guerra <guerrinha@comum.org>
 * Copyright (C) 2011  Lincoln de Sousa <lincoln@comum.org>
 * Copyright (C) 2011  Governo do Estado do Rio Grande do Sul
 *
 *   Author: Lincoln de Sousa <lincoln@gg.rs.gov.br>
 *   Author: Guilherme Guerra <guerrinha@comum.org>
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

$(window).load(function() {
    //Dos videos em destaque
    $('.carousel').carousel();

    var video_page = 1;
    $(".thumbnails").append("")
    $("#readmorevideos").click(function(){
        $.ajax({
            url:"/videos/nextpage/" + video_page + "/",
            success: function(resp){
                if(!resp){
                    $("#readmorevideos").attr("disabled", "disabled");
                    $("#readmorevideos").html("Não há mais vídeos!");
                    return;
                }
                $(".thumbnails").append(resp);
                //alert(resp);
                video_page = video_page + 1;
                window.setTimeout(function(){
                    $('.thumbnails').masonry('reload');
                },1000);
            }
        });
    });

    $('video').mediaelementplayer({});

    $('#facebook').click(function() {
        window.open(
            'https://www.facebook.com/sharer/sharer.php?u='+encodeURIComponent(location.href),
            'facebook-share-dialog',
            'width=626,height=436');
        return false;
     });

    $('#twitter').click(function() {
        window.open(
            'https://twitter.com/share?url='+encodeURIComponent(location.href),
            'Twitter-share-dialog',
            'width=626,height=436');
        return false;
     });

    $('#googleplus').click(function() {
        window.open(
            'https://plus.google.com/share?url='+encodeURIComponent(location.href),
            'googleplus-share-dialog',
            'width=626,height=436');
        return false;
     });
});
