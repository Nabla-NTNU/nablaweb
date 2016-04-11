$("button.likeButton").click(function (e) {
    var button = $(this);
    $.ajax({
        method: "POST",
        url: likeToggleUrl,
        data: button.data(),
        success: function(result){
            button.parent().find(".likeCount").text(result.count);
            button.find(".likeText").text(result.liked ? "Liker ikke" : "Liker");
        },
    });
    button.blur();
});
