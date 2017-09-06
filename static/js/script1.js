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
        $container = $search_mode.find(".js-results-container");
        $("#browse-mode").hide();
        $container.html('');
        $container.load(url+'?'+data+' #search-results', function (responseText) {
            work_with_item();
            console.log(responseText);
            $spinner.hide();
            window.history.pushState("object or string", "Title", url+'?'+data);
        });
    });


    function work_with_item() {
        var prev_item = '';
        $(".product-card-body").fancybox({
            margin: [0, 0],
            animationEffect : "fade",
            baseClass: 'fancybox-overlay js-fix-scroll fancybox-overlay-fixed',
            btnTpl : {
                smallBtn: '<a data-fancybox-close class="close-button-base close-button-position-top-right" title="{{CLOSE}}"></a>'
            },
            spinnerTpl : '<div id="fancybox-loading"><div id="fancybox-loading-spinner"></div></div>'
            touch : {
                vertical : false,  // Allow to drag content vertically
                momentum : false   // Continue movement after releasing mouse/touch when panning
            },
            afterLoad: function (instance) {
                prev_item = $(instance.$lastFocus[0]).parent();
                window.history.pushState("object or string", "Title", instance.current.src);
            },
            afterClose: function () {
                window.history.back();
            },
            clickContent : function( current, e ) {

                if($(e.target).parents('.CardAction').length || $(e.target).hasClass('CardAction')){
                    e.preventDefault();
                    if($(e.target).parents('.CardAction').length){
                        $btn = $(e.target).parents('.CardAction');
                    } else {
                        $btn = $(e.target);
                    }
                    var url = $btn.attr('href');
                    $.ajax({
                        url: url,
                        contentType: 'application/json',
                        success: function (data) {
                            $ico = prev_item.find('.like-action-icon');
                            $like_count = prev_item.find('.like-action-number');

                            if('added' in data) {
                                $btn.addClass('is-liked');
                                $ico.removeClass('icon-heart').addClass('icon-heart-red');
                            } else if('removed' in data){
                                $btn.removeClass('is-liked');
                                $ico.removeClass('icon-heart-red').addClass('icon-heart');
                            }
                            $like_count.text(data['likes_count'])
                        }
                    })
                }
            }
        });

        $("#items, #search-results").on('click', function (e) {

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
    work_with_item();


});
