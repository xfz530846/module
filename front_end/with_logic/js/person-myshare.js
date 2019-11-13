/**
 * Created by python on 19-8-28.
 */
/**
 * Created by python on 19-8-25.
 */
var get_headlines = new Vue({
        el: '#my_headlines',
        data: {
            host: HOST,
            id: '',
            headlines: '',
            username: sessionStorage.username || localStorage.username,
            user_id: sessionStorage.user_id || localStorage.user_id,
            token: sessionStorage.token || localStorage.token,
        },
        methods: {
            get_headlines: function () {

                    axios.get(this.host + '/my_headlines/', {
                         headers: {
                    'Authorization': 'JWT ' + this.token
                    },
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            console.log(response.data)
                            this.headlines = response.data;
                        })
                        .catch(
                            error => {
                                // console.log(error.response.data)
                            }
                        )
                    },
                },
            mounted: function () {
                this.get_headlines()
            },
        })
