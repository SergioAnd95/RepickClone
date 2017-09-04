$.fn.extend({
    animateCss: function (animationName, complete) {

        this.addClass('animated ' + animationName);
        this.one('animationend', function(event) {

            $(this).removeClass('animated ' + animationName);

            if(complete){
                complete()
            }

        });
        return this;
    }
});

$(document).ready(function(){
    $("#modal-window").on('click', function (e) {
        $modal = $(this);
        if(e.target.className==='fancybox-overlay js-fix-scroll fancybox-overlay-fixed' || e.target.className==='close-button-base close-button-position-top-right' ){
            $modal.fadeOut(function () {
                $('html').removeClass('fancybox-margin fancybox-lock')
            });
        }

        if($(e.target).parents('.CardAction').length || e.target.className === 'CardAction--showText CardAction CardAction--like'){
            if($(e.target).parents('.CardAction').length){
                $btn = $(e.target).parents('.CardAction')
            } else {
                $btn = $(e.target);
            }

            var url = $btn.attr('href');
            $.ajax({
                url: url,
                contentType: 'application/json',
                success: function (data) {
                    $prev_item = $('.feed-card[data-product-id="'+$modal.attr('data-product-id')+'"]');
                    $ico = $prev_item.find('.like-action-icon');
                    $like_count = $prev_item.find('.like-action-number');

                    if('added' in data) {
                        $btn.addClass('is-liked');
                        $ico.removeClass('icon-heart').addClass('icon-heart-red');
                    }
                    else if('removed' in data){
                        $btn.removeClass('is-liked');
                        $ico.removeClass('icon-heart-red').addClass('icon-heart');
                    }
                    $like_count.text(data['likes_count'])
                }
            })
        }

    });

    $(".search-form").on('submit', function (e) {
        e.preventDefault();
        $search_mode = $("#search-mode");
        console.log($search_mode);
        $spinner = $search_mode.find('.js-spinner.product-search-spinner');
        $spinner.show();
        var data = $(this).serialize();
        var url = $(this).attr('action');
        //$loader.show();
        $search_mode.show();
        $("#browse-mode").hide();
        $search_mode.find(".js-results-container").load(url+'?'+data+' #search-results', function (responseText) {
            work_with_item();
            console.log(responseText);
            $spinner.hide();
        });
    });


    function work_with_item() {


    $("#items, #search-results").on('click', function (e) {

        e.preventDefault();
        if($(e.target).parents('.product-card-body').length) {
            console.log(e.target.className);
            e.preventDefault();
            $parent = $(e.target).parents(".product-card-body");
            $feed = $parent.parents('.feed-card');
            var url = $parent.attr('href');

            //$loader.show();
            //$("#modal-window").animateCss('fadeIn');
            $modal = $("#modal-window");
            $modal.fadeIn();
            $.ajax({
                url: url,
                success: function (data) {
                    $modal.find(".fancybox-inner .wrapper").html(data);
                    $modal.attr('data-product-id', $feed.attr('data-product-id'));
                    //$loader.hide();
                    $("html").addClass('fancybox-margin fancybox-lock');
                },
                error: function(textStatus){
                    console.log(textStatus);
                    if(textStatus.status == 404 ){
                        alert('Данный товар не найден');
                    } else if(textStatus.status == 500){
                        alert('Извините за временные неудобства, попробуйте позже')
                    }
                    var parent = $(this).parent().parent();
                    parent.animateCss('fadeOut', function () {
                        parent.removeClass('visible transition');
                    });
                    $("html").removeClass('fancybox-margin fancybox-lock');
                    //$loader.hide();
                }

            })
        }

        if($(e.target).parents('.like-action-link').length || e.target.className === 'like-action-link'){
            e.preventDefault();
            if(e.target.className === 'like-action-link'){
                $btn = $(e.target);
            }
            else{
                $btn = $(e.target).parents('.like-action-link');
            }

            var url = $btn.attr('href');
            $ico = $btn.find('.like-action-icon');
            $like_count = $btn.find('.like-action-number');
            $.ajax({
                url: url,
                contentType: 'application/json',
                success: function (data) {
                    if('added' in data) {
                        $ico.removeClass('icon-heart').addClass('icon-heart-red');
                    }
                    else if('removed' in data){
                        $ico.removeClass('icon-heart-red').addClass('icon-heart');
                    }
                    $like_count.text(data['likes_count'])
                }
            })
        }
    });
    }

    $("#loadmore").on('click', function () {}
    );

    work_with_item();

    $(".search-form input").focus(function(e){
        $parent = $(this).parent();
        $parent.addClass("width_100p");
    });

    $(".search-form input").focusout(function () {
        $parent = $(this).parent();
        $parent.removeClass("width_100p");
    })


});
