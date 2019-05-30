//提交评论
var pid = "";
$("#comment_btn").click(function () {
    var article_id = $(".info").attr("article_id");
    var content = $("#comment_content").val();
    if (pid) {
        var index = content.indexOf("\n");
        content = content.slice(index + 1);
    }

    $.ajax({
        url: "/blog/api/comment/",
        type: "POST",
        data: {
            article_id: article_id,
            content: content,
            pid: pid,
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
        },
        success: function (data) {
            //后台成功返回数据后直接刷新页面显示最新评论
            window.location.reload();
            //清空pid
            pid = "";
        }
    })
});

//回复按钮事件
$(".list-group-item .reply_btn").click(function () {
    $("#comment_content").focus();
    var def_value = "@" + $(this).attr("username") + "\n";
    $("#comment_content").val(def_value);
    //给pid赋值
    pid = $(this).attr("comment_pk");
});
