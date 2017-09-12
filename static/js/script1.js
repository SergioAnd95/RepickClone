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
    
    var mobileSearch = function() {
        var e, t = function(e, t) {
            return function() {
                return e.apply(t, arguments)
            }
        };
        $(function() {
            return window.searchController = new e, searchController.searchOnLoad(), $(document.body).on("click", ".js-cancelSearchMode", function() {
                return $(document).trigger("Search:showSearchMode", !1)
            })
        }), e = function() {
            function e() {
                this.searchDispatch = t(this.searchDispatch, this), this.$document = $(document), this.$browseMode = $("#browse-mode"), this.$searchMode = $("#search-mode"), this.pendingSearches = {}, this.inSearchMode = !1, this.previousScrollPos = null, this.initListeners()
            }
            return e.prototype.initListeners = function() {
                return this.$document.on("Search:requestSearch", function(e) {
                    return function(t, n) {
                        return e.searchDispatch(n)
                    }
                }(this)), this.$document.on("Search:showSearchMode", function(e) {
                    return function(t, n) {
                        return e.showSearchMode(n)
                    }
                }(this)), this.$document.on("Search:requestMobileSearch", function(e) {
                    return function(t, n) {
                        return e.showMobileSearchInput(n)
                    }
                }(this)), window.addEventListener("popstate", function(e) {
                    return function(t) {
                        return t.state && t.state.query ? (e.showSearchMode(!0), e.searchDispatch(query)) : (e.showSearchMode(!1), e.$document.trigger("Search:requestClearSearchInput"), $(".js-globalSearchInput").blur())
                    }
                }(this))
            }, e.prototype.searchOnLoad = function() {
                var e, t;
                return window.location.pathname.indexOf("/search") > -1 && (e = window.location.search.parseQueryString(), e.q) ? (t = e.q, $(document).trigger("Search:updateQuery", t), $(document).trigger("Search:requestSearch", t)) : void 0
            }, e.prototype.showMobileSearchInput = function(e) {
                return e ? document.body.classList.add("is-showingMobileSearchInput") : (document.body.classList.remove("is-showingMobileSearchInput"), this.clearSearchResults(), this.showSearchMode(!1), this.$document.trigger("Search:requestClearSearchInput"), $("#mobileSearchInput").focus())
            }, e.prototype.showSearchMode = function(e) {
                return e ? (this.previousScrollPos = this.$document.scrollTop(), this.$browseMode.hide(), this.$searchMode.show(), this.inSearchMode = !0) : (this.$browseMode.show(), this.$document.scrollTop(this.previousScrollPos), this.$searchMode.hide(), this.inSearchMode = !1)
            }, e.prototype.clearSearchResults = function() {
                return $("#search-container").html("")
            }, e.prototype.search = function(e, t) {
                var n, r, o;
                return n = $(".js-" + e + "-search-section"), n.show(), n.find(".js-empty-state").hide(), n.find(".js-spinner").show(), n.find(".js-results-container").hide(), n.find(".js-message").hide(), r = function() {
                    return function(e) {
                        var t;
                        return n.find(".js-spinner").hide(), t = $(e.trim()), 0 === t.length ? n.find(".js-empty-state").show() : (n.find(".js-empty-state").hide(), n.find(".js-results-container").html(e), n.find(".js-results-container").show(), n.find(".js-message").show(), ReactRailsUJS.mountComponents()), setUpSmoothScroll()
                    }
                }(this), null != (o = this.pendingSearches[e]) && o.abort(), this.pendingSearches[e] = $.ajax("/ajax/" + e + "_search", {
                    dataType: "html",
                    data: {
                        query: t
                    },
                    success: r
                })
            }, e.prototype.searchDispatch = function(e) {
                var t, n, r, o, i;
                return $(".js-asin-search-section").hide(), $(".js-amazon-search-section").hide(), $(".js-product-search-section").hide(), $(".js-canopy-search-section").hide(), this.inSearchMode || this.clearSearchResults(), (null != e ? e.length : void 0) > 0 ? (this.clearSearchResults(), this.showSearchMode(!0)) : this.showSearchMode(!1), e = e.trim(), n = "Searched", o = {
                    originating: !0,
                    query: e
                }, SegmentAnalytics.canopyTrack(n, o), i = encodeURI(e.trim()), window.history.pushState({
                    query: e
                }, "Search: query", "/search?q=" + i), r = e.match("/([A-Z0-9]{10})(/|\\?|$)"), t = e.match(/canopy\.co.*\/products\/([0-9]+)/), r ? this.search("asin", r[1]) : t ? this.search("canopy", t[1]) : this.search("product", e), $("body").animate({
                    scrollTop: -$($(".search-summary")[0]).offset().top
                }, 200)
            }, e
        }()
    }.call(this);


    $('.NavAction--showSearch').on('click', function () {
        return $(document).trigger("Search:requestMobileSearch", !0)
    });

    $('.GlobalNav-cancelMobileSearch').on('click', function () {
        return $(document).trigger("Search:requestMobileSearch", !1)
    })
});
