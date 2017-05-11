/**
 * Created by wyj on 2017/5/9.
 */
	//文章加载
$(document).ready(function(){
    data = {"user":"wang"};
    $.ajax({url:"/index/",
        async:true,
        type:'POST',
        data :data,
        success:
            function(data){
                var  article_data = JSON.parse(data);
                var  article_arr = article_data['data'];
                for(var i in article_arr){
                    console.log(article_arr[i]["id"]);
                    var strhtml = '<div class="row  text-center">\
                                    <div class="col-xs-8 col-xs-offset-2">\
                                    <h3><a href="javascript:void(0)" onclick="get_article(this);"  id="'+article_arr[i]["id"]+'" >'+article_arr[i]["title"]+'</a></h3>\
                                    <p><span class="label label-warning">'+article_arr[i]["category"]+'</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="glyphicon glyphicon-calendar"></span>&nbsp;<span>'+article_arr[i]["pub_date"]+'</span>&nbsp;&nbsp;&nbsp;&nbsp;<span class="glyphicon glyphicon-user"></span>&nbsp;<span>'+article_arr[i]["author_name"]+'</span> </p>\
                                    <p>'+article_arr[i]["content"]+'</p>\
                                    </div>\
                                    </div>';

                    $(".my_article").append(strhtml);
                }
            }
    });

});
// 文章ID
function get_article(m) {
    var id_number = m.id;
    location.href="article/"+id_number;
}