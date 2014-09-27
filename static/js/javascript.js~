// Scroll globals
var pageNum = {{ page.number }}; // The latest page loaded
var hasNextPage = {{ page.has_next|lower }}; // Indicates whether to expect another page after this one
var baseUrl = '{% url 'store:infinite' %}'; // The root for the JSON calls

// loadOnScroll handler
var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    if ($(window).scrollTop() > $(document).height() - ($(window).height()*3)) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(window).unbind();
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        loadItems();
    }
};

var loadItems = function() {
    // If the next page doesn't exist, just quit now
    if (hasNextPage === false) {
        return false
    }
    // Update the page number
    pageNum = pageNum + 1;
    // Configure the url we're about to hit
    var url = baseUrl + "json/" + pageNum + '/';
    $.ajax({
        url: url,
        dataType: 'json',
        success: function(data) {
            // Update global next page variable
            hasNextPage = data.hasNext;
            // Loop through all items
            var html = [];
            $.each(data.itemList, function(index, item){
                /* Format the item in our HTML style */
                html.push('<div class="media">',
                    '<a class="index-icon pull-left" href="/store/', item.appid, '">',
                    '<img class=" media-object" src="', item.icon, '" alt="app.icon"></a>',
                    '<div class="media-body">',
                    '<h4 class="media-heading">', item.names, '</h4>',
                    '<p>评分：', item.rating, '</p>',
                    '<p>大小：', item.fileSize, '</p>',
                    '<p>系统：', item.operatingSystems, '</p></div></div>'
                    )
            });
            // Pop all our items out into the page
            $("#newtwitter-anchor").before(html.join(""));
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(window).bind('scroll', loadOnScroll);
        }
    });
};
$(document).ready(function(){
   $(window).bind('scroll', loadOnScroll);
});
