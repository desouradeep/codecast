$(document).ready(function() {
    onResize();
    $(window).resize(function() {
        onResize();
    });

});

function onResize() {
    /**
    Redraw UI on resize, to remove posibilities of template breaking
    **/
    var window_height = $(window).height();
    var window_width = $(window).width();

    /**
     adjustments related to height
    **/
    $('.login').height($(window).height());
    // adjust textarea height
    $('.code-pane').height(window_height-80);

    $('.read-pane').height(window_height-80-39);
}

function loadPagelets(pagelets) {
    /**
    Send ajax requests to retrieve contents of every pagelet on the page
    **/
    for(var page in pagelets) {
        $.ajax({
            url: pagelets[page].url,
            async: false,
            success: function(result) {
                $('#' + pagelets[page].id).html(result);
            }
        });
    }
}

$("#dark-theme").click(function() {
    user_editor.setTheme("ace/theme/monokai");
    for(var key in ace_readers) {
        var reader = ace_readers[key];
        reader.setTheme("ace/theme/monokai");
    }
    $(".tab-link").removeClass("tab-link-light");
    $(".tab-link").addClass("tab-link-dark");
});

$("#light-theme").click(function() {
    user_editor.setTheme("ace/theme/textmate");
    for(var key in ace_readers) {
        var reader = ace_readers[key];
        reader.setTheme("ace/theme/textmate");
    }
    $(".tab-link").removeClass("tab-link-dark");
    $(".tab-link").addClass("tab-link-light");
});
