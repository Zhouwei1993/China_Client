var cardnoPic="";
var vcode="";
$(function(){
    jeDate({//加载日期控件
        dateCell: '#testy',
        isinitVal: false,
        format: 'YYYY-MM-DD', // 分隔符可以任意定义，该例子表示只显示年月
        minDate: '2000-06-01', //最小日期
        maxDate: '2050-06-01' //最大日期
    });
    jeDate({
        dateCell: '#Born2',
        isinitVal: false,
        format: 'YYYY-MM-DD', // 分隔符可以任意定义，该例子表示只显示年月
        minDate: '1900-06-01', //最小日期
        maxDate: '2050-06-01' //最大日期
    });

});


function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return (r[2]); return null;
}

var init;

init = setInterval("readCard();",500);



function change() {
    var objS = document.getElementById("pid");
    var value = objS.options[objS.selectedIndex].value;
    if (value == 1) {
        $("#boat").css("display", "block");
        $("#work").css("display", "block");
        $("#carnumber").css("display", "none");
    } else if (value == 2) {
        $("#boat").css("display", "none");
        $("#work").css("display", "block");
        $("#carnumber").css("display", "none");
    } else if (value == 3) {
        $("#boat").css("display", "none");
        $("#work").css("display", "none");
        $("#carnumber").css("display", "block");
    }
}

function gtPage() {//手动输入
    window.clearInterval(init);
    $("#myPhoto").attr("src", "img/photo_bg.png");
    document.all['NameA'].value="";
    document.all['Sex2'].value="";
    document.all['Born2'].value="";
    document.all['cardno'].value="";
    document.all['Address'].value="";
    $(".tip").css("display", "none");
    $(".input").css("display", "none");
    $(".content").css("display", "block");


        var video = document.getElementById('video'),
        canvas = document.getElementById('canvas'),
        snap = document.getElementById('tack'),
        vendorUrl = window.URL || window.webkitURL;
    var image_save_blob;

    //媒体对象
    navigator.getMedia = navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia;
    navigator.getMedia({
        video: true, //使用摄像头对象
        audio: false  //不适用音频
    }, function(strem){
        console.log(strem);
        video.src = vendorUrl.createObjectURL(strem);
        video.play();
    }, function(error) {
        //error.code
        console.log(error);
    });
    snap.addEventListener('click', function() {

        //绘制canvas图形
        canvas.getContext('2d').drawImage(video, 0, 0, 160, 180);
        //把canvas图像转为img图片，显示在网页上
        img_url = canvas.toDataURL("image/png");

        $("#cardno_pic").val(img_url);
    })
}

var isInit=false;



/*读取身份证*/
function readCard(){

    //SynIDCard1.getCardInfo();

    //SynIDCard1.card_type;卡 片 类 型  2
    //SynIDCard1.isSuccess;读卡是否成功： 1
    //SynIDCard1.errorFlag;错误信息： 0 成功

    //document.all['Nation'].value=SynIDCard1.nationality; 名族

    SynIDCard1.getCardInfo();//读取
    var srmy=SynIDCard1.isSuccess;

    var photoUrl=SynIDCard1.image;//照片路径
    //2644
    //1136

    var uname=SynIDCard1.cust_name;//姓名
    var gender=SynIDCard1.gender;//性别
    if("1"==gender){
        gender="男";
    }else{
        gender="女";
    }
    var birthday=SynIDCard1.birthday;//出生日期
    var cardno=SynIDCard1.card_code;//身份证
    var address=SynIDCard1.address;//地址


    $("#NameA").val(uname);//姓名
    $("#Sex2").val(gender);//性别
    $("#testx").val(birthday);//出生年月yyyy-mm-dd
    $("#identity").val(cardno);//身份证
    $("#Address").val(address);//地址
    $("#myPhoto").attr("src", "data:image/png;base64,"+photoUrl);
    cardnoPic=photoUrl;

    if(1==srmy&&photoUrl.length!=1136){
        window.clearInterval(init);
        $(".tip").css("display", "none");
        $(".input").css("display", "none");
        $(".content").css("display", "block");//显示
    }

}

function validate() {
    vcode=GetQueryString("code");
    var uname=$("#NameA").val(); //姓名
    var gender=$("#Sex2").val();//性别
    var birthday=$("#testx").val();//出生年月yyyy-mm-dd
    var cardno=$("#identity").val();//身份证
    var address=$("#Address").val();//地址
    var cheph=$("#cheph").val();//车牌号

    if (""==uname) {
        alert("请输入姓名!");
        return;
    }
    if (""==gender) {
        alert("请输入性别!");
        return;
    }
    if (!"男"==gender||!"女"==gender) {
        alert("请输入性别,只能为男或女!");
        return;
    }
    if (""==birthday){
        alert("请选择出生日期");
        return;
    }

    var reg = new RegExp("^[0-9]*$");
    //if (cardno.length != 18) {
    //alert("请输入正确的身份证号!");
    //return;
    //}
    if (""==cardno){
        alert("请输入身份证号！");
        return;
    }
    if (""==address){
        alert("请输入地址！");
        return;
    }

    var objS1 = document.getElementById("pid");
    var value1 = objS1.options[objS1.selectedIndex].value;
    if (value1 == 0) {
        alert("请选择申请类型!");
        return;
    }

    var phone =$("#phone").val();
    if (!reg.test(phone) || phone.length != 11) {
        alert("请输入正确的手机号!");
        return;
    }
    //alert(value1);
    if (""==$("#danwei").val()&&value1==2||""==$("#danwei").val()&&value1==1){
        alert("请输入工作单位！");
        return;
    }
    if (""==$("#cheph").val()&&value1==3){
        alert("请输入车牌号！");
        return;
    }
    if (""==$("#zhiwu").val()){
        alert("请输入职务！");
        return;
    }
    if (""==$("#board").val()&&value1==1){
        alert("请输入所登的船舶！");
        return;
    }
    if (""==$("#testy").val()){
        alert("请选择申请时限！");
        return;
    }
    if (""==$("#shiyou").val()){
        alert("请输入申请事由！");
        return;
    }
    ///
    var dw="";
    if (value1==2||value1==1){
        dw=$("#danwei").val();
    }else if(value1==3){
        dw=$("#cheph").val();
    }
    if(value1==1){
        value1="登轮许可证";
    }
    if(value1==2){
        value1="口岸限定区域许可证";
    }
    if(value1==3){
        value1="口岸限定区域车辆通行证";
    }

    if(!$('#bhc').attr('checked')){
        if (""==value&&type_value==1){
            return '请输入所登的船舶！';
        }
    }

    $("#btn1").attr("disabled","disabled");
    $("#btn2").attr("disabled","disabled");

    jQuery.post("../SCert/goSCertSave.do",
        {"uname":uname,
            "gender":gender,
            "birthday":birthday,
            "cardno":cardno,
            "address":address,
            "mob":$("#phone").val(),
            "sqlx":value1,
            "danwei":dw,//单位
            "zhiwu": $("#zhiwu").val(),//职位
            "board": $("#board").val(),//船
            "shiyou": $("#shiyou").val(),//事由
            "sqsx": $("#testy").val(),//申请时限
            "cardnoPic":cardnoPic,//身份证照片
            "vcode":vcode,
            "fromW":"pc"
        },function(json){
            if(true==json.iserror){
                alert("提交错误，系统繁忙！");
                return;
            }else if(false==json.iserror){
                $(".tip").css("display","block");
                $(".input").css("display","block");
                $(".content").css("display","none");

                $("#NameA").val(""); //姓名
                $("#Sex2").val("");//性别
                $("#testx").val("");//出生年月yyyy-mm-dd
                $("#identity").val("");//身份证
                $("#Address").val("");//地址

                $("#phone").val("");//手机
                $("#danwei").val("");//单位
                $("#zhiwu").val("");//职位
                $("#board").val("");//船
                $("#shiyou").val("");//事由
                $("#cheph").val("");//车牌号
                cardnoPic="";

                $("#btn1").attr("disabled",false);
                $("#btn2").attr("disabled",false);
                init = setInterval("readCard();",500);
                //window.location.reload();
                //alert("提交成功！");
                return;
            }
        },"json");
}
  