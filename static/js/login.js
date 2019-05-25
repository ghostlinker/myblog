$('li.dropdown').mouseover(function () {
    $(this).addClass('open');
}).mouseout(function () {
    $(this).removeClass('open')
});


$("#reg_submit").click(function () {
    // 取到用户填写的注册数据，向后端发送AJAX请求
    var formData = new FormData();
    formData.append("username", $("#id_username").val());
    formData.append("password", $("#id_password").val());
    formData.append("re_pwd", $("#id_re_pwd").val());
    formData.append("email", $("#id_email").val());
    formData.append("phone_num", $("#id_phone_num").val());
    formData.append("csrfmiddlewaretoken", $("[name='csrfmiddlewaretoken']").val());

    $.ajax({
        url: "/reg/",
        type: "post",
        processData: false,  // 告诉jQuery不要处理我的数据
        contentType: false,  // 告诉jQuery不要设置content类型
        data: formData,
        success:function (data) {
            if (data.status){
                // 有错误就展示错误
                console.log(data.msg);
                // 将报错信息填写到页面上
                $.each(data.msg, function (k,v) {
                    console.log("id_"+k, v[0]);
                    console.log($("#id_"+k));
                    $("#id_"+k).next("span").text(v[0]).parent().parent().addClass("has-error");
                })

            }else {
                //没有错误就跳转到指定页面
                alert("注册成功")
                location.href = data.msg;
            }
        }
    })
});

//清空错误信息
$("form input").focus(function () {
    $(this).next().text("").parent().parent().removeClass("has-error")
})

//用户名注册提示
$("#id_username").on("input", function () {
    //获取用户填写的用户名
    var username = $(this).val();
    $.ajax({
        url: "/api/check_user/",
        type: "get",
        data: {"username": username},
        success: function (data) {
            if(data.status){
                //用户名已被注册，给出提示信息
                $("#id_username").next().text(data.msg).parent().parent().addClass("has-error");
            }
        }
    })
});

//登录请求
$("#login-button").click(function () {
    var username = $("#username").val();
    var password = $("#password").val();
    $.ajax({
        url: "/login/",
        type: "post",
        data:{
            "username": username,
            "password": password,
            "csrfmiddlewaretoken":  $("[name='csrfmiddlewaretoken']").val()
        },
        success: function (data) {
            if (data.status){
                //页面上显示报错信息
                $(".login-error").text(data.msg);
            }else {
                location.href = data.msg;
            }
        }
    })
})

//重新获取焦点时清空之前的错误信息
$("#username, #password").focus(function () {
    $(".login-error").text("");
});

