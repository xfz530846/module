/**
 * Created by python on 19-8-24.
 */

var qa_list = new Vue({
    el: '#qa_list',
    data: {
        questions:[],
        new_:'active',
        hot:'',
        wait:'',
        page:1,
        page_size:6,
        count:0,

    },
    computed: {
        total_page: function(){  // 总页数
            return Math.ceil(this.count/this.page_size);
        },
        next: function(){  // 下一页
            if (this.page >= this.total_page) {
                return 0;
            } else {
                return this.page + 1;
            }
        },
        previous: function(){  // 上一页
            if (this.page <= 0 ) {
                return 0;
            } else {
                return this.page - 1;
            }
        },
        page_nums: function(){  // 页码
            // 分页页数显示计算
            // 1.如果总页数<=5
            // 2.如果当前页是前3页
            // 3.如果当前页是后3页,
            // 4.既不是前3页，也不是后3页
            var nums = [];
            if (this.total_page <= 5) {
                for (var i=1; i<=this.total_page; i++){
                    nums.push(i);
                }
            } else if (this.page <= 3) {
                nums = [1, 2, 3, 4, 5];
            } else if (this.total_page - this.page <= 2) {
                for (var i=this.total_page; i>this.total_page-5; i--) {
                    nums.push(i);
                }
            } else {
                for (var i=this.page-2; i<this.page+3; i++){
                    nums.push(i);
                }
            }
            return nums;
        }
    },
   methods: {
        get_question_list: function(order,filter,category_id){

            axios.get(HOST+'/questions?order='+order +'&filter='+filter+'&category_id=' +category_id, {
                    params: {
                        page: this.page,
                        page_size: this.page_size,

                    },
                    responseType: 'json'
                })
            .then(response=>{
                this.questions=response.data.results
                this.count=response.data.count
            })

            .catch(error => {
                console.log(error.response.data);
            })}
            ,
       check_active: function (num) {
            if (num=='new'){
                this.new_='active'
                this.hot=''
                this.wait=''
            }else if (num=='hot'){
                this.new_=''
                this.hot='active'
                this.wait=''
            }else{
                this.new_=''
                this.hot=''
                this.wait='active'
            }

        },
         // 点击页数
        on_page: function(num){
            if (num != this.page){
                this.page = num;
                this.get_question_list('-create_time','new',0);
            }
        },
   },
    mounted: function(){
        this.get_question_list('-create_time','new',0)
    },
})

var qa_categories = new Vue({
     el: '#qa_categories',
    data: {
        categories:null,
        default_cat: {
            "name": "首页",
            "id": "0"
        },
        activeClass: 0,
    },
   methods: {
        get_categories: function(){
            axios.get(HOST+'/qa_categories?order=')
            .then(response=>{

            this.categories=response.data
            this.categories.unshift(this.default_cat)
            })
        },
         get_qa_list: function (category_id, index) {
            qa_list.get_question_list('-create_time','',category_id)
            this.activeClass = index
        },
   },
    mounted: function(){
        this.get_categories()
    },
})





var login_check = new Vue({
    el: '#login_check',
    data: {
        host:HOST,
		username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        is_login:"",
         error_username: false,
        error_pwd: false,
        error_pwd_message: '请填写密码',
        username: '',
        password: '',
        remember: false,
        url:'',
        categories:'',

    },
   methods: {
       check_login: function (){
        axios.get(this.host +'/user/' ,{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                if (response.data)
                {this.is_login = true
                }
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
       // 检查数据
        check_username: function(){
            if (!this.username) {
                this.error_username = true;
            } else {
                this.error_username = false;
            }
        },
        check_pwd: function(){
            if (!this.password) {
                this.error_pwd_message = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
            }
        },
        // 表单提交
        login: function(){
            this.check_username();
            this.check_pwd();
            if (this.error_username == false && this.error_pwd == false) {
                axios.post(this.host+'/authorizations/', {
                        username: this.username,
                        password: this.password
                    }, {
                        responseType: 'json',
                        withCredentials: true
                    })
                    .then(response => {
                        // 使用浏览器本地存储保存token
                        if (this.remember) {
                            // 记住登录
                            sessionStorage.clear();
                            localStorage.token = response.data.token;
                            localStorage.user_id = response.data.user_id;
                            localStorage.username = response.data.username;
                        } else {
                            // 未记住登录
                            localStorage.clear();
                            sessionStorage.token = response.data.token;
                            sessionStorage.user_id = response.data.user_id;
                            sessionStorage.username = response.data.username;
                        }

                        window.location.reload()
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            this.error_pwd_message = '用户名或密码错误';
                        } else {
                            this.error_pwd_message = '服务器错误';
                        }
                        this.error_pwd = true;
                    })
            }
        },
        get_categories: function(order){
            axios.get(HOST+'/qa_categories?order=' + order)
            .then(response=>{
            this.categories=response.data
            })
        },
    },
    mounted: function(){
        this.url = location.href
        if (this.token) {
            this.check_login()
        }
        this.get_categories('-create_time')
    },

})
