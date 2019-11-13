/**
 * Created by python on 19-8-28.
 */
/**
 * Created by python on 19-8-25.
 */
var my_focus = new Vue({
        el: '#my_focus',
        data: {
            host: HOST,
            id: '',
            focus: [],
            username: sessionStorage.username || localStorage.username,
            user_id: sessionStorage.user_id || localStorage.user_id,
            token: sessionStorage.token || localStorage.token,
            questions:'',
            question_detail: '',
            useful_status: '',
        },
        methods: {
            get_my_focus: function () {

                    axios.get(this.host + '/focus_question/', {
                         headers: {
                    'Authorization': 'JWT ' + this.token
                    },
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            console.log(response.data)
                            this.focus = response.data;
                            // console.log(this.my_focus.questions.title)

                        })
                        .catch(
                            error => {
                                // console.log(error.response.data)
                            }
                        )
                    },
            // 取消点赞问题
            cancel: function (id,index) {
                if (!this.token) {
                    location.href = '/person-loginsign.html'
                }
                axios.delete(this.host + '/questions/'+ id +'/useful/',{
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                })
                .then(response => {
                    if (response.status == 204) {
                        this.focus.splice(index,1)
                        // alert('取消收藏成功');
                    }

                })
                .catch(error => {
                    alert(error.response.data.message);
                })
            },
        },
            mounted: function () {
                this.get_my_focus()
            },
        })
