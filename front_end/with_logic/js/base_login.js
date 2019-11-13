/**
 * Created by python on 19-7-30.
 */
$(".footer").load("/footer.html")

const HOST = 'http://127.0.0.1:8000';

Vue.filter('str2date', function (value) {

    return new Date(value)

})


Vue.filter('date2ymd', function (value) {
        var year = value.getFullYear();
        var month = value.getMonth() +1;
        var day = value.getDate();
    return year + "-"+ month + "-" + day

})


function get_query_string(name) {
        var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        var r = window.location.search.substr(1).match(reg);
        if (r != null) {
            return decodeURI(r[2]);
        }
        return null;
    }
