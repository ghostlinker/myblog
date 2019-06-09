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

//点赞或者踩的事件
$("#div_digg .action").click(function () {
    if ($(".info").attr("username")) {
        //点赞或者踩
        var is_up = $(this).hasClass("diggit");
        var article_id = $(".info").attr("article_id");
        //发ajax请求
        $.ajax({
            url: "/blog/api/up_down/",
            type: "POST",
            data: {
                csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
                is_up: is_up,
                article_id: article_id,
            },
            success: function (data) {
                if (data.status) {
                    //赞或者灭成功后重新加载页面刷新出结果
                    window.location.reload();
                } else {
                    //重复提交
                    if (data.first_action) {
                        $("#digg_tips").html("你已经赞过");
                    } else {
                        $("#digg_tips").html("你已经踩过");
                    }
                    setTimeout(function () {
                        $("#digg_tips").html("")
                    }, 1000)
                }
            }
        })
    } else {
        alert("请登录后再点赞");
        location.href = "/login/";
    }
});

$(document).ready(function () {
    $('code.hljs').each(function (i, block) {
        hljs.lineNumbersBlock(block);
    });
});
