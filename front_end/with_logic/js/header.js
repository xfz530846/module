/**
 * Created by python on 19-8-24.
 */
//模块点亮
var modules = new Vue({
    el: '#modules',
    data: {
        host:HOST,
        headline:'',
		qa: '',
        activity:'',
        talk:''
    },
    mounted: function(){
        var url = location.href
        var headline = RegExp('headline')
        var qa = RegExp('qa')
        var activity = RegExp('activity')
        var talk = RegExp('talk')

       if (headline.test(url) || url == 'http://127.0.0.1:8080/index.html' || url == 'http://127.0.0.1:8080/')
       {
           this.headline = 'active'
       }else if(qa.test(url))
       {
            this.qa= 'active'
       }else if(activity.test(url))
       {
            this.activity = 'active'
       }else if(talk.test(url))
       {
            this.talk = 'active'
       }
    },
})



// 用户信息
var user_info = new Vue({
    el: '#user_info',
    data: {
        host:HOST,
        user:'',
		username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        nickname:'',
        url:'',
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
        this.url = location.href
        if (this.token) {
            this.get_user()

        }
    },
});
