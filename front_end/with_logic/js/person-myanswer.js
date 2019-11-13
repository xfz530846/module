/**
 * Created by python on 19-8-25.
 */
var my_answer = new Vue({
        el: '#my_answer',
        data: {
            host: HOST,
            id: '',
            answers: '',
            username: sessionStorage.username || localStorage.username,
            user_id: sessionStorage.user_id || localStorage.user_id,
            token: sessionStorage.token || localStorage.token,
        },
        methods: {
            get_answers: function () {

                    axios.get(this.host + '/my_answers/', {
                         headers: {
                    'Authorization': 'JWT ' + this.token
                    },
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            this.answers = response.data
                        })
                        .catch(error => {
                            console.log(error.response.data);
                        })
                    },
                },
            mounted: function () {
                this.get_answers()
            },
        })
