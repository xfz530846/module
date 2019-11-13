/**
 * Created by python on 19-8-28.
 */
/**
 * Created by python on 19-8-25.
 */
var collect_articals= new Vue({
        el: '#collect',
        data: {
            host: HOST,
            id: '',
            collect_articles: [],
            collect_talks:[],
            username: sessionStorage.username || localStorage.username,
            user_id: sessionStorage.user_id || localStorage.user_id,
            token: sessionStorage.token || localStorage.token,
        },
        methods: {
            get_collect_articles: function () {

                    axios.get(this.host + '/collect_articles/', {
                         headers: {
                    'Authorization': 'JWT ' + this.token
                    },
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            console.log(response.data)
                            this.collect_articles = response.data;
                        })
                        .catch(
                            error => {
                                // console.log(error.response.data)
                            }
                        )
                    },
            get_collect_talks: function () {

                    axios.get(this.host + '/collect_talks/', {
                         headers: {
                    'Authorization': 'JWT ' + this.token
                    },
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            console.log(response.data)
                            this.collect_talks = response.data;
                        })
                        .catch(
                            error => {
                                // console.log(error.response.data)
                            }
                        )
                    },
                },
            mounted: function () {
                this.get_collect_articles()
                this.get_collect_talks()
            },
        })
