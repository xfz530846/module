var qa_detail = new Vue({
    el:"#qa_detail",
    data:{
        host: HOST,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        question_detail : {
            author:{},
            label:{}
        },
        question_id: '',
        question_detail: '',
        useful_status: '',
        author_id: '',
        answers: [],
        show: false,
        current_index: -1,
        user_answer:'',
        user_comment:'',
        comment:[]


    },

    mounted: function () {

        this.get_url_params();
        this.get_question_detail();
        this.get_answers();

    },

    methods:{

        // 获取url参数
        get_url_params: function () {
             this.question_id = get_query_string('id', null);
             if (this.question_id == null) {
                location.href = '/qa-index.html'
             }
        },

        // 获取问题详情
        get_question_detail: function () {
            if (this.token) {
                axios.get(this.host + '/questions/' + this.question_id + '/', {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                })
                .then(response => {
                    this.question_detail = response.data
                    this.useful_status = response.data.useful_status
                    this.author_id = response.data.author.id
                    console.log(response.data.useful_status)
                })
                .catch(error => {
                    console.log(error.response.data);
                });
            } else {
                axios.get(this.host + '/questions/' + this.question_id + '/', {
                    responseType: 'json',
                })
                .then(response => {
                    this.question_detail = response.data
                    this.useful_status = response.data.useful_status
                    console.log(response.data.useful_status)
                })
                .catch(error => {
                    console.log(error.response.data);
                });
            }

        },

        // 获取问题回答
        get_answers: function () {

            if (this.token) {
                axios.get(this.host + '/questions/' + this.question_id + '/answers/', {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                })
                .then(response => {
                    this.answers = response.data

                })
                .catch(error => {
                    // console.log(error.response.data);
                });
            } else {
                axios.get(this.host + '/questions/' + this.question_id + '/answers/', {
                    responseType: 'json',
                })
                .then(response => {
                    this.answers = response.data

                })
                .catch(error => {
                    // console.log(error.response.data);
                });
            }

        },

        // 显示问题回复框
        show_question_comment_box: function () {
            this.show = true;
        },

        // 显示答案回复框
        show_answer_comment: function (index) {
            this.current_index = index;
        },
        
        // 阻止默认表单提交
        onSubmit: function () {
            return false;
        },
        
        // 提交回答
        submit_answer: function () {
            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }
            if (this.user_answer && this.question_id) {
                axios.post(this.host + '/questions/useranswer/', {
                    content: this.user_answer,
                    question:this.question_id,

                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                })
                .then(response => {
                    this.answers.unshift(response.data)
                    this.show=false
                    this.question_detail.answers_count+=1
                })
                .catch(error => {
                    // alert(error.response.data.message);
                });
            } else {
                alert('内容不能为空')
            }
        },
        
        // 提交评论
        submit_comment: function (answer_id) {
            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }
            if (this.user_comment) {
                axios.post(this.host + '/questions/usercomment/', {
                    content: this.user_comment,
                    answer:answer_id,
                    parent:this.parent

                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                })
                .then(response => {
                    this.comment.unshift(response.data)


                })
                .catch(error => {
                    // alert(error.response.data.message);
                });
            } else {
                alert('内容不能为空')
            }
        },

        // 点赞问题
        question_useful: function () {
            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }

            axios.post(this.host + '/questions/useful/', {
                "questions": this.question_id
            },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                this.question_detail.useful_status = 1;
                this.question_detail.useful_count += 1;
                // alert(response.data.message);

            })
            .catch(error => {
                // alert(error.response.data.message);
            })
        },

        // 取消点赞问题
        question_unuseful: function () {

            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }
            axios.delete(this.host + '/questions/'+ this.question_id +'/useful/',{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                if (response.status == 204) {
                    this.question_detail.useful_status = 0;
                    this.question_detail.useful_count -= 1;
                    // alert('取消收藏成功');
                }

            })
            .catch(error => {
                // alert(error.response.data.message);
            })
        },

        // 点赞回答
        answer_useful: function (answer_id, index) {
            if (!this.token) {
                location.href = '/person-loginsign.html'
            }
            axios.post(this.host + '/answers/useful/', {
                "answer": answer_id
            },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                this.answers[index].useful_status = 1;
                this.answers[index].useful_count += 1;
                // alert(response.data.message);

            })
            .catch(error => {
                // alert(error.response.data.message);
            })
        },

        // 取消点赞回答
        answer_unuseful: function (answer_id, index) {
            if (!this.token) {
                location.href = '/person-loginsign.html'
            }
            axios.delete(this.host + '/answers/'+ answer_id +'/useful/',{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                if (response.status == 204) {
                    this.answers[index].useful_status = 0;
                    this.answers[index].useful_count -= 1;
                    // alert('取消收藏成功');
                }

            })
            .catch(error => {
                // alert(error.response.data.message);
            })
        },


    },
})


var qa_categories = new Vue({
     el: '#qa_categories',
    data: {
        categories:null,
        default_cat: {
            "name": "全部",
            "id": "0"
        },
        activeClass: 0,
        id:'',
    },
   methods: {
        get_categories: function(){
            axios.get(HOST+'/qa_categories?order=')
            .then(response=>{
             console.log(this.activeClass)
            this.categories=response.data
            this.categories.unshift(this.default_cat)

            })
        },
   },
    mounted: function(){
        this.activeClass = get_id()
        this.get_categories()

    },
})


function get_id() {
    var id = get_query_string('id', null)
    if (id == null) {
        location.href = '/'
    } else {
        return id
    }}

