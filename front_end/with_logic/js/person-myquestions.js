/**
 * Created by python on 19-8-28.
 */
/**
 * Created by python on 19-8-25.
 */
var my_questions = new Vue({
        el: '#my_questions',
        data: {
            host: HOST,
            id: '',
            questions: [],
            username: sessionStorage.username || localStorage.username,
            user_id: sessionStorage.user_id || localStorage.user_id,
            token: sessionStorage.token || localStorage.token,
        },
        methods: {
            get_my_questions: function () {

                    axios.get(this.host + '/my_questions/', {
                         headers: {
                    'Authorization': 'JWT ' + this.token
                    },
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            console.log(response.data)
                            this.questions = response.data;
                        })
                        .catch(
                            error => {
                                // console.log(error.response.data)
                            }
                        )
                    },
                },
            mounted: function () {
                this.get_my_questions()
            },
        })
