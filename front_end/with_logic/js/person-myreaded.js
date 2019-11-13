/**
 * Created by python on 19-8-28.
 */
/**
 * Created by python on 19-8-25.
 */
var my_brosing_history = new Vue({
        el: '#my_brosing_history',
        data: {
            host: HOST,
            id: '',
            username: sessionStorage.username || localStorage.username,
            user_id: sessionStorage.user_id || localStorage.user_id,
            token: sessionStorage.token || localStorage.token,
            broswing_history:[]
        },
        methods: {
            get_broswing_history: function () {

                    axios.get(this.host + '/broswing_hitory/', {
                         headers: {
                    'Authorization': 'JWT ' + this.token
                    },
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            console.log(response.data)
                            this.broswing_history = response.data;
                        })
                        .catch(
                            error => {
                                // console.log(error.response.data)
                            }
                        )
                    },
                },
            mounted: function () {
                this.get_broswing_history()
            },
        })
