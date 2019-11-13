/**
 * Created by python on 19-8-24.
 */

// $(".sui-navbar").load("/header.html")

var  user_archives= new Vue({
    el: '#user_archives',
    data: {
        host:HOST,
        user:'',
		username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        user_archives:"",
        user_archives_count:"",
        edit:'none',
    },
    methods: {
        create_user_archives:function () {
            axios.post(this.host + '/user_detail/',{}, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {
                    this.user_archives = response.data
                    window.location.reload()
                })
                .catch(error => {
                    // console.log(error.response.data);
                })
        },
        get_user_info: function () {

            axios.get(this.host + '/user_center/', {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
                .then(response => {

                    // console.log(response.data)
                    this.user_archives = response.data
                    if (user_archives.city==''){
                        user_archives.city='请填写现居住城市'
                    }
                })
                .catch(error => {
                    // console.log(error.response.data);
                })
        },
        check_user_archives: function () {
            axios.get(this.host + '/user_archive/', {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            }).then(response => {
                    this.user_archives_count = response.data.count

                    if (this.user_archives_count == 0){
                        this.create_user_archives()
                    }else {
                        this.get_user_info()
                    }
                }).catch(error => {
                    // console.log(error.response.data);
                })
        },
        live_city: function () {
            // alert('点击事件')
            console.log(event.target)
            $(event.target).parents(".fill").siblings(".edit-item").toggle();
        },

    },
    mounted: function () {
        var count =  this.check_user_archives()
    },
});

