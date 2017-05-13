/**
 * Created by wyj on 2017/5/8.
 */

$(document).ready(function(){
        $(".w-category-one,.w-category-two,.w-category-three,.w-category-four").click(function() {
            var category_val = $(this).html();
            $('.w-category').html(category_val);
        });


		$('#w-btn-publish').click(function(){
		    if(getCookie("name") != null){
                var title = $('#w-input-title').val();
                var content = $('#w-area-content').val();
                var author_name = getCookie('name');
                var author_id = getCookie('user_id');
                var category_str = $('.w-category').html();
                console.log(category_str);
                var finalInfo = new Object();
                    finalInfo.author_name = author_name;
                    finalInfo.title = title;
                    finalInfo.content = content;
                    finalInfo.category_str = category_str;
                    finalInfo.author_id = author_id;
                var finalInfoStr = JSON.stringify(finalInfo);  //从一个对象解析出字符串

                    if (title == "" && content == ""){
                        alert("标题和内容不能为空！");
                    }else{
                        $.ajax({url:"/publish/",
                            async:true,
                            type:'POST',
                            data :finalInfoStr,
                            success:function(data){
                                console.log(data);
                                    alert("文章发布成功，即将跳转到主页！");
                                    location.href="/index.html";
                                }});
                    }
            } else{
		        alert("请登录!")
            }
		});

    //读取cookies
    function getCookie(name) {
        var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
        if(arr=document.cookie.match(reg))
            return unescape(arr[2]);
        else
            return null;
    }
});
