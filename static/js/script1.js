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
    $loader = $("#loader");
    $("#modal-window .close").on('click', function () {

        var parent = $(this).parent().parent();
        parent.animateCss('fadeOut', function () {
            parent.removeClass('visible transition');
        });
        $("body").removeClass('dimmed');
        $("#modal-window-content").hide();
        $("#modal-loader").hide();

    });

    $(".search-form").on('submit', function (e) {
        e.preventDefault();
        var data = $(this).serialize();
        var url = $(this).attr('action');
        console.log(url, data);
        $loader.show();
        $("#__blaze-root .site-content").load(url+'?'+data+' .site-content', function () {
            $("#loader").hide();
            work_with_item();
        });
    });


    function work_with_item() {
        $('#modal-content, .product-standalone').on('click', function (e) {

        $modal = $(this);
        var target = e.target;

        if(target.id == 'like-button' || $(target).parents('#like-button').length > 0){
            e.preventDefault();
            if(target.id == 'like-button'){
                $btn = $(target);
            } else {
                $btn = $(target).parents('#like-button');
            }

            var url = $btn.attr('href');
            $.ajax({
                url: url,
                contentType: 'application/json',
                success: function (data) {
                    $icon = $btn.find('.icon');
                    if('added' in data) {
                        $icon.addClass('active');
                    }
                    else if('removed' in data){
                        $icon.removeClass('active');
                    }
                    //console.log(data.likes_count);
                    var l = $('.product-grid-link[data-id = "'+$btn.attr('data-id')+'"]').find('.love-this-count');
                    console.log(l);
                    var likes = data['likes_count'];
                    l.each(function () {
                        $(this).html(''+likes);

                    });

                }
            })
        } else if((target.className.substr('big-related-product') > 0 || $(target).parent().hasClass('big-related-product')) || (target.className.substr('related-product') > 0 || $(target).parent().hasClass('related-product'))){
            e.preventDefault();
            if(target.className.substr('big-related-product') > 0 || target.className.substr('related-product') > 0){
                $item = $(target);
            } else {
                $item = $(target).parent();
                console.log($item);
            }
            var url = $item.attr('href');

            $.ajax({
                url: url,
                success: function (data) {
                $modal.html(data);
                },
                error: function(textStatus){
                    console.log(textStatus);
                    if(textStatus.status == 404 ){
                        alert('Данный товар не найден');
                    } else if(textStatus.status == 500){
                        alert('Извините за временные неудобства, попробуйте позже')
                    }
                }
            });

        }
    });

    $("#items").on('click', function (e) {
        console.log(e.target.className);
        if($(e.target).parents('.amazon-product').length) {

            e.preventDefault();
            $parent = $(e.target).parents(".product-grid-link");
            var url = $parent.attr('href');

            $loader.show();
            $("#modal-window").addClass('visible transition').animateCss('fadeIn');
            $.ajax({
                url: url,
                success: function (data) {
                $("#modal-content").html(data);

                $loader.hide();
                $("body").addClass('dimmed');
                $("#modal-window-content").show();
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
                    $("body").removeClass('dimmed');
                    $loader.hide();
                }

            })
        }
    });
    }

    $("#loadmore").on('click', function () {}
    );

    work_with_item();

    $(".search-form input").focus(function(e){
        $parent = $(this).parent()
        $parent.addClass("width_100p");
    });

    $(".search-form input").focusout(function () {
        $parent = $(this).parent();
        $parent.removeClass("width_100p");
    })


});
