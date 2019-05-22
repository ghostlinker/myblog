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
        type: "POST",
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
                location.href = data.msg;
            }
        }
    })
});

//清空错误信息
$("form input").focus(function () {
    $(this).next().text("").parent().parent().removeClass("has-error")
})
