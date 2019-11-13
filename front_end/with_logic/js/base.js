/**
 * Created by python on 19-7-30.
 */

$(".sui-navbar").load("/header.html")
$(".footer").load("/footer.html")

const HOST = 'http://api.malonghui.com:8000';

// 全局过滤器
//字符串转日期对象  str2date
//日期对象转年月日  date2ymd
//日期对象转时分秒  date2hms
//日期对象转周几    date2week
Vue.filter('str2date', function (value) {

    return new Date(value)

})

Vue.filter('date2ymd', function (value) {

        var oNow=new Date();
        var yearToday = oNow.getFullYear();
        var monthToday = oNow.getMonth() +1;
        var dayToday = oNow.getDate();
        var year = value.getFullYear();
        var month = value.getMonth() +1;
        var day = value.getDate();

        var today_str = yearToday + "-"+monthToday + "-" + dayToday
        var oToday = new Date(today_str)


        if (Number(oNow) -Number(value) < Number(oNow) - Number(oToday)){
            return '今天'
        }
        else {
            return year + "-"+month + "-" + day
        }



})

Vue.filter('date2hm', function (value) {
        var hour = value.getHours();
        var minute = value.getMinutes();
    return hour + ":"+minute
})

const WEEK =["周日","周一","周二","周三","周四","周五","周六"]
Vue.filter('date2week', function (value) {
        var intDay = value.getDay();
    return WEEK[intDay]
})

//获取url参数
function get_query_string(name,defValue) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return defValue;
}