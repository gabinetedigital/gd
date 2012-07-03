/* Copyright (C) 2012  Lincoln de Sousa <lincoln@comum.org>
 * Copyright (C) 2012  Governo do Estado do Rio Grande do Sul
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

function changeCurrentPic(link) {
    var $link = $(link);

    /* Resseting the css class */
    $('ul.images li a').removeClass('selected');
    $link.addClass('selected');

    /* Loading the new text and picture */
    $('#currentgallery .currentpic p').html($link.attr('title'));
    $('#currentgallery .currentpic img')
        .attr('src', '')
        .attr('src', $link.attr('href'));

    /* Moving the focus to the top of the image */
    $('html,body').animate({ scrollTop: 270 }, 100);
    return false;
}


function nextPic() {
    var link = $('ul.images li a.selected').parent().next().find('a');
    changeCurrentPic(link);
}


function prevPic() {
    var link = $('ul.images li a.selected').parent().prev().find('a');
    changeCurrentPic(link);
}

$(document).ready(function(){

    var show_per_page = 10;
    var number_of_items = $('.images').children().size();
    var number_of_pages = Math.ceil(number_of_items/show_per_page);

    $('#current_page').val(0);
    $('#show_per_page').val(show_per_page);

    var navigation_html = '<a class="previous_link" href="javascript:previous();">Prev</a>';
    var current_link = 0;
    while(number_of_pages > current_link){
	navigation_html += '<a class="page_link" href="javascript:go_to_page(' + current_link +')" longdesc="' + current_link +'">'+ (current_link + 1) +'</a>';
	current_link++;
    }

    navigation_html += '<a class="next_link" href="javascript:next();">Next</a>';

    $('#page_navigation').html(navigation_html);

    //add active_page class to the first page link
    $('#page_navigation .page_link:first').addClass('active_page');

    //hide all the elements inside content div
    $('.images').children().css('display', 'none');

    //and show the first n (show_per_page) elements
    $('.images').children().slice(0, show_per_page).css('display', 'block');

});    

function previous(){

    new_page = parseInt($('#current_page').val()) - 1;
    //if there is an item before the current active link run the function
    if($('.active_page').prev('.page_link').length==true){
	go_to_page(new_page);
    }

}

function next(){
    new_page = parseInt($('#current_page').val()) + 1;
    //if there is an item after the current active link run the function
    if($('.active_page').next('.page_link').length==true){
	go_to_page(new_page);
    }

}
function go_to_page(page_num){
    //get the number of items shown per page
    var show_per_page = parseInt($('#show_per_page').val());

    //get the element number where to start the slice from
    start_from = page_num * show_per_page;

    //get the element number where to end the slice
    end_on = start_from + show_per_page;

    //hide all children elements of content div, get specific items and show them
    $('.images').children().css('display', 'none').slice(start_from, end_on).css('display', 'block');

    /*get the page link that has longdesc attribute of the current page and add active_page class to it
      and remove that class from previously active page link*/
    $('.page_link[longdesc=' + page_num +']').addClass('active_page').siblings('.active_page').removeClass('active_page');

    //update the current page input field
    $('#current_page').val(page_num);
}
