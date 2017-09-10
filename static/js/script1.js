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

    function set_fancybox(){
        $(".product-card-body, .product-link").fancybox({
            margin: [0, 0],
            animationEffect : "fade",
            baseClass: 'fancybox-overlay js-fix-scroll fancybox-overlay-fixed',
            btnTpl : {
                smallBtn: '<a data-fancybox-close class="close-button-base close-button-position-top-right" title="{{CLOSE}}"></a>'
            },
            spinnerTpl : '<div id="fancybox-loading"><div id="fancybox-loading-spinner"></div></div>',
            content: this,
            afterLoad: function (instance) {
                console.log(instance);
                window.history.pushState("object or string", "Title", instance.current.src);
            },
            afterClose: function () {
                window.history.back();
            },
            clickContent : function(current, e ) {

                var prev_item= current.opts.$orig.parent();

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
                            console.log(prev_item);
                            if(prev_item.parents('.ProductCard').length){
                                $ico = prev_item.parents('.ProductCard').find('.like-action-link');
                                active_class = 'is-liked';
                                deactive_class = '';
                            } else {
                                active_class = 'icon-heart-red';
                                deactive_class = 'icon-heart';
                                $ico = prev_item.find('.like-action-icon');
                            }
                            console.log($ico);
                            $like_count = prev_item.find('.like-action-number');

                            if('added' in data) {
                                $btn.addClass('is-liked');
                                $ico.removeClass(deactive_class).addClass(active_class);
                            } else if('removed' in data){
                                $btn.removeClass('is-liked');
                                $ico.removeClass(active_class).addClass(deactive_class);
                            }
                            $like_count.text(data['likes_count'])
                        }
                    })
                }
            }
        });
    }

    function work_with_item() {
        set_fancybox();
        $("#items, #search-results").on('click', function (e) {
            console.log('asda');
            if($(e.target).parents('.like-action-link').length || e.target.className === 'like-action-link'){
                e.preventDefault();
                console.log('sadas');

                if(e.target.className === 'like-action-link'){
                    $btn = $(e.target);
                }
                else{
                    $btn = $(e.target).parents('.like-action-link');
                }
                var url = $btn.attr('href');

                $like_count = $btn.find('.like-action-number');

                var active_class = '';
                var deactive_class = '';

                if($btn.parents('.ProductCard').length){
                    $ico = $btn;
                    active_class = 'is-liked';
                    deactive_class = ''
                } else {
                    active_class = 'icon-heart-red';
                    deactive_class = 'icon-heart';
                    $ico = $btn.find('.like-action-icon');
                }

                console.log($ico);

                $.ajax({
                    url: url,
                    contentType: 'application/json',
                    success: function (data) {
                        if('added' in data) {
                            $ico.removeClass(deactive_class).addClass(active_class);
                        }
                        else if('removed' in data){
                            $ico.removeClass(active_class).addClass(deactive_class);
                        }
                        $like_count.text(data['likes_count'])
                    }
                })
            }
        });
    }
    work_with_item();

    $("#items, #search-results").on('DOMNodeInserted DOMNodeRemoved', function (e) {
        set_fancybox();
    });


    var share = function () {
        $(function () {
            var e, t, n, r, o;
            return r = !1, e = .9, n = function (e) {
                if (e.keyCode !== 27) ;
                else if ($(".PageHeader-wrapper").hasClass("is-viewingHeaderShare")) return t()
            }, o = function (r) {
                var o, i, a, s, l, u;
                return console.log("click"), i = $(r.target).closest(".js-headerShareCanvas"), l = $("<div class='Scrim Scrim--headerShare'></div>"), s = $(".js-headerShareButton"), u = $(".js-triggerHeaderShare"), o = $(".js-closeButtonAnimateTarget"), a = $(".js-pageHeaderCreatorAvatar"), i.append(l), o.velocity("transition.expandIn", {
                    delay: 200,
                    duration: 200,
                    display: null
                }), u.velocity("transition.fadeOut", {
                    duration: 200,
                    display: null
                }), a.velocity({
                    translateY: -32,
                    scale: .5,
                    opacity: 0
                }, {
                    duration: 75,
                    display: null,
                    ease: "ease-out"
                }), s.velocity("transition.expandIn", {
                    delay: 150,
                    stagger: 25,
                    duration: 150,
                    ease: "ease-out",
                    display: null
                }), l.velocity({
                    opacity: e
                }, {
                    duration: 400,
                    ease: "ease-out",
                    begin: function () {
                        return $("body").addClass("is-viewingHeaderShare")
                    },
                    complete: function () {
                        return $("body").on("keyup", n), $("body").on("click", ".js-closeHeaderShare", t), $("body").addClass("is-restingHeaderShare")
                    }
                })
            }, t = function () {
                var e, o, i, a, s;
                return r ? !0 : (r = !0, a = $(".Scrim--headerShare"), s = $(".js-triggerHeaderShare"), e = $(".js-closeButtonAnimateTarget"), i = $(".js-headerShareButton"), o = $(".js-pageHeaderCreatorAvatar"), e.velocity("transition.fadeOut", {
                    duration: 200,
                    display: null
                }), s.velocity("transition.expandIn", {
                    delay: 100,
                    duration: 200
                }), o.velocity({
                    translateY: 0,
                    scale: 1,
                    opacity: 1
                }, {
                    delay: 150,
                    duration: 100,
                    display: null,
                    ease: "ease-out"
                }), i.velocity("transition.expandOut", {
                    stagger: 50,
                    duration: 300,
                    display: null,
                    ease: "ease-out",
                    backwards: null,
                    begin: function () {
                        return $("body").removeClass("is-restingHeaderShare")
                    },
                    complete: function () {
                        return $("body").removeClass("is-viewingHeaderShare"), $("body").off("click", ".js-closeHeaderShare", t), $("body").off("keyup", n), a.remove(), r = !1
                    }
                }), a.velocity({
                    opacity: 0
                }, {
                    duration: 400,
                    ease: "ease-out"
                }))
            }, $("body").on("click", ".js-triggerHeaderShare", o)

        });
    }.call(this);
});
