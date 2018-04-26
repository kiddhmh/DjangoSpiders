/**
 * Created by huminghao on 2018/4/23.
 */

function check_form(){
    if($("#keywordInput").val() == ""){
        var alert = $("#alert_noKeyword")
        if(!alert.hasClass("show")){
            $("#alert_noKeyword").addClass("show");
            setTimeout(function(){
                $("#alert_noKeyword").removeClass("show");
            },1500);
        }
        return false;
    }
}

$('#selectMenu').selectpicker();
