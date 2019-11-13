    /**
 * Created by python on 19-8-24.
 */

$("#user_center_archives").load("/user_center_archives.html")
var vm = new Vue({
    el: '#user_info',
    data: {
        host:HOST,
        user:'',
		username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
    },
   methods: {
       get_user: function (){
        axios.get(this.host +'/user/' ,{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                this.user = response.data
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
       logout: function () {
        sessionStorage.username =''
        sessionStorage.user_id = ''
        sessionStorage.token = ''
        localStorage.username = ''
        localStorage.user_id = ''
        localStorage.token = ''
        location.reload()
    }
   },
    mounted: function(){

        if (this.token) {
            this.get_user()

        }else {
            if (window.location.href != 'http://127.0.0.1:8080/') {
                window.location = '/'
            }
        }
    },
});
