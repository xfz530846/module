/**
 * Created by python on 19-8-26.
 */
var my_info = new Vue({
    el: '#my_info',
    data: {
        host: HOST,
        user: '',
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        my_file: '',
        display:'',
        edit:'编辑',
        edit_flag:0,
        name:'',
        sex:'男',
        birthday:'',
        website:'',
        mobile:'',
        email:'',
        city:'',
        address:'',
        company:'',
        error_msg_show:false,
        error_msg:[],
    },
    methods: {
        get_my_file :function () {
            axios.get(this.host + '/my_file/', {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                    console.log(response.data)
                    this.my_file = response.data
                    if (this.my_file.gender == '1'){
                        this.my_file.gender = '男'
                    }else if(this.my_file.gender == '2'){
                         this.my_file.gender = '女'
                    }
                })
            .catch(
                error => {
                    console.log(error.response.data)
                }
            )
        },
        show:function () {
            if (this.edit_flag == 0){
            this.edit_flag+=1
            this.edit ='取消'
            this.display = 'block'}
            else {
                this.edit_flag = 0
                this.edit = '编辑'
                this.display = 'none'
            }

        },
        submit_myfile:function () {
            axios.put(this.host + '/edit_myfile/', {
                realname: this.name,
                gender: this.sex,
                birthdate: this.birthday,
                website: this.website,
                real_mobile: this.mobile,
                email:this.email,
                city: this.city,
                address: this.address,
                company: this.company,

                    }, {
                        headers: {
                            'Authorization': 'JWT ' + this.token
                        },
                            responseType: 'json',
                            withCredentials: true
                    })
                    .then(response => {
                        window.location.reload()
                    })
                .catch(error => {
                    // console.log(error.response.data)
                    this.error_msg_show = true
                    this.error_msg = error.response.data
                })



        },
},
    mounted: function () {
        this.get_my_file()
    },
})

var experience = new Vue({
    el: '#experience',
    data: {
        host: HOST,
        user: '',
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        experience: '',
        display:'',
        edit:'编辑',
        edit_flag:0,
        error_msg_show:false,
        error_msg:[],
    },
     methods: {
          show:function () {
            if (this.edit_flag == 0){
            this.edit_flag = 1
            this.edit ='取消'
            this.display = 'block'}
            else {
                this.edit_flag = 0
                this.edit = '编辑'
                this.display = 'none'
            }

        },

     },
})

