/**
 * Created by wyj on 2017/5/8.
 */



$(document).ready(function(){
    //检查登录状态
    (function () {
        check_login_status();
    })();
    //注册
    $(".w-btn-signup").click(function() {
        var name = $("#r-name").val();
        var password = $("#r-password").val();
        var email = $("#r-email").val();
        var reg = new RegExp("^[A-Za-z0-9]+$");

         if(name.length>=3 && name.length<=16){
            if(reg.test(name)){
                var check_name = new Object();
                check_name.username=name;
                check_name.email=email;
                check_name.password=password;
                var check_name_str = JSON.stringify(check_name);  //从一个对象解析出字符串
                console.log(check_name_str);
                $.ajax({url:"api/signup",
                        async:true,
                        type:"POST",
                        data :check_name_str,
                        success:
                            function(data) {
                                console.log(data);
                                if(data.status == 1){
                                    $(".w-login-close").click();
                                    alert("注册成功,请登录!")
                                }else {
                                    alert("此用户名已存在!")
                                }
                            }
                })
            }else{
                alert("名称需要3-16个数字和字母组成！");
            }
         }else{
             alert("名称需要3-16个数字和字母组成！");
         }
    });

    $(".logout-box").click(
        function () {
         var user_data = new Object();
         user_data.username = getCookie("name");
         user_data.password = getCookie("password");
         var user_data_str = JSON.stringify(user_data);
         $.ajax({url:"api/logout",
                async:true,
                type:"POST",
                data :user_data_str,
                success:
                    function(data) {
                        if(data.status == 1){
                            delCookie("name");
                            delCookie("password");
                            delCookie("user_id");
                            check_login_status();
                            console.log(1);
                        }else{
                            alert("登出失败!")
                        }

                    }
                })
        }
    );
    $(".w-btn-login").click(function() {
        var name = $("#l-name").val();
        var password = $("#l-password").val();
        var check_login = new Object();
        check_login.username = name;
        check_login.password = password;
        var check_loginstr = JSON.stringify(check_login);  //从一个对象解析出字符串
        $.ajax({url:"api/login",
                async:true,
                type:"POST",
                data :check_loginstr,
                success:function(data) {
                    var data_auth;
                    var data_pwd;
                    var UserId;
                    if (data.status == 1) {
                        $(".w-login-close").click();
                        $(".login-box").css("display", "none");
                        $(".logout-box").css("display", "block");
                        data_auth = data.username;
                        data_pwd = data.password;
                        UserId = data.user_id;
                        $(".login-welcome a").html(data_auth);
                        setCookie("user_id", UserId);
                        setCookie("name", data_auth);
                        setCookie("password", data_pwd);
                        console.log(data)
                    }
                    if(data.status == 0){
                        $("#login-msg").css("display","block");
                        console.log(data)
                    }

                }
        })
    });

    $(".read-cookie-btn").click(function(){
       console.log(getCookie("user_id"));
       console.log(getCookie("name"));
       console.log(getCookie("password"));
    });
    $(".del-cookie-btn").click(function(){
       console.log(delCookie("user_id"));
       console.log(delCookie("name"));
       console.log(delCookie("password"));
    });
});
//检查是登录状态
function check_login_status() {
    if ((getCookie("name") != null)&&(getCookie("password") != null)&&(getCookie("user_id") != null)){
        $(".login-box").css("display", "none");
        $(".logout-box").css("display", "block");
        $(".login-welcome a").html(getCookie("name"));
    }else{
        $(".login-box").css("display", "block");
        $(".logout-box").css("display", "none");
        $(".login-welcome a").html("");
    }
}

//写cookies
function setCookie(name,value) {
    var Days = 1;
    var exp = new Date();
    exp.setTime(exp.getTime() + Days*24*60*60*1000);
    document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}
//读取cookies
function getCookie(name) {
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}
//删除cookies
function delCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval=getCookie(name);
    if(cval!=null)
    document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}

