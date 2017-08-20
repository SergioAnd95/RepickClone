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
    $("#modal-window .close").on('click', function () {

        var parent = $(this).parent().parent();
        parent.animateCss('fadeOut', function () {
            parent.removeClass('visible transition');
        });
        $("body").removeClass('dimmed');

    });
    $('.product-grid-link').on('click', function (e) {
        e.preventDefault();
        var url = $(this).attr('href');
        $.ajax({
            url: url,
            success: function (data) {
                $("#modal-content").html(data);

                $("#modal-window").addClass('visible transition').animateCss('fadeIn');

                $("body").addClass('dimmed')
            },
            error: function(textStatus){
                console.log(textStatus);
                if(textStatus.status == 404 ){
                    alert('Данный товар не найден');
                }
            }
        })
    });
});
