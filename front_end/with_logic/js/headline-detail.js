/**
 * Created by python on 19-8-24.
 */

var detail = new Vue({
    el:"#detail",
    data:{
        host: HOST,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        headlines_detail : {
            author:{},
            user:{}
        },
        headlinescomments : 0,
        nickname:'',
        author_id :'',
        comments_detail:'',
        last_child_commnet:[],
        headline_id: '',
        category_id: '',
        content: '',
        collection_status: '',
        attention_status: '',
        current: -1,
        reply_content:'',
        user: '',
        hot_headlines: [],
        hot_talks: [],

    },

    mounted: function () {
            this.get_url_params();
            this.get_headline_detail();
            this.get_headline_comments();
            this.get_hot_headlines();
            this.get_hot_talks();
            if (this.token) {
                this.get_user()

            };

    },

    methods: {

        // 获取url参数
        get_url_params: function () {
             this.headline_id = get_query_string('id', null);
             this.category_id = get_query_string('category_id', null)
             if (this.headline_id == null) {
                location.href = '/'
             }
        },

        // 获取头条详情
        get_headline_detail: function () {
            if (this.token) {
                axios.get(this.host + '/headlines/' + this.headline_id + '/detail/', {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                })
                .then(response => {
                    this.headlines_detail = response.data
                    this.collection_status = response.data.collection_status
                    this.attention_status = response.data.attention_status
                    this.author_id = response.data.author.id
                    console.log(response.data.collection_status)
                })
                .catch(error => {
                    console.log(error.response.data);
                });
            } else {
                axios.get(this.host + '/headlines/' + this.headline_id + '/detail/', {
                    responseType: 'json',
                })
                .then(response => {
                    this.headlines_detail = response.data
                    this.collection_status = response.data.collection_status
                    console.log(response.data.collection_status)
                })
                .catch(error => {
                    console.log(error.response.data);
                });
            }

        },

        // 获取头条评论
        get_headline_comments: function () {
            axios.get(this.host + '/headlines/' + this.headline_id + '/comments', {
                responseType: 'json',
            })
            .then(response => {
                this.comments_detail = response.data
                this.control_comments_count(this.comments_detail)
            })
            .catch(error => {
                // console.log(error.response.data);
            });
        },

        // 收藏头条
        collect: function () {
            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }
            axios.post(this.host + '/headlines/collections/', {
                "headlines": this.headline_id
            },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                this.collection_status = 1;
                // alert(response.data.message);

            })
            .catch(error => {
                // alert(error.response.data.message);
            })
        },

        // 取消收藏头条
        uncollect: function () {
            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }
            axios.delete(this.host + '/headlines/'+ this.headline_id +'/collections/',{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                if (response.status == 204) {
                    this.collection_status = 0;
                    // alert('取消收藏成功');
                }

            })
            .catch(error => {
                // alert(error.response.data.message);
            })
        },

        // 跳转登陆页面
        login: function () {
            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }
        },

        // 阻止默认表单提交
        onSubmit: function () {
            return false;
        },

        // 提交头条评论
        headline_comment: function() {
            if (this.content && this.headline_id) {
                axios.post(this.host + '/headlines/comments/', {
                    content: this.content,
                    headlines:this.headline_id,
                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                })
                .then(response => {
                    this.comments_detail.unshift(response.data)
                    this.control_comments_count(this.comments_detail)
                    this.content = ''
                    this.headlines_detail.comment_counts += 1
                })
                .catch(error => {
                    // alert(error.response.data.message);
                });
            } else {
                alert('内容不能为空')
            }
        },

        // 显示回复框
        show_reply: function (index) {
            this.current = index
        },

        // // 隐藏回复框
        // hidden: function () {
        //     this.current = -1
        // },

        // 回复评论
        reply_comment: function (parent_id, index) {
            if (parent_id && this.reply_content && this.headline_id) {
                axios.post(this.host + '/headlines/comments/', {
                    content:  this.reply_content,
                    headlines: this.headline_id,
                    parent_id: parent_id
                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                })
                .then(response => {
                    this.comments_detail[index].child_comments = response.data
                    this.comments_detail[index].child_counts += 1
                    this.headlines_detail.comment_counts += 1
                    this.reply_content = ''
                    this.current = -1
                })
                .catch(error => {
                    // alert(error.response.data.message);
                });
            }

        },

        // 控制显示评论数量(只显示最新的十条评论)
        control_comments_count: function (arr) {
            if (arr.length > 10) {
                arr.splice(9, arr.length - 10)
            }
        },

        // 跳转到其他新闻详情
        target: function (headline_id, category_id) {
            location.href = '/headline-detail.html?id=' + headline_id + '&category_id=' + category_id
        },

        // 获取用户信息
        get_user: function (){
        axios.get(this.host +'/user/' ,{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                this.user = response.data
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },

        // 关注作者
        attention: function () {
            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }
            axios.post(this.host + '/user/follow/', {
                "followeds": this.author_id,
            },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                this.attention_status = 1;
                // alert(response.data.message);

            })
            .catch(error => {
                // alert(error.response.data.message);
            })
        },

        // 取消关注作者
        unattention: function () {
            if (!this.token) {
                location.href = '/person-loginsign.html?next=' + location.href
            }
            axios.delete(this.host + '/user/'+ this.author_id +'/follow/',{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                if (response.status == 204) {
                    this.attention_status = 0;
                    // alert('取消关注成功');
                }

            })
            .catch(error => {
                // alert(error.response.data.message);
            })
        },

        // 显示热门头条
        get_hot_headlines: function () {
            axios.get(this.host + '/headlines/' + this.category_id + '/hot/', {
                responseType: 'json',
            })
            .then(response => {
                this.hot_headlines = response.data
            })
            .catch(error => {
                // console.log(error.response.data);
            });
        },

        // 显示热门吐槽
        get_hot_talks: function () {
            axios.get(this.host + '/talks/hot/', {
                responseType: 'json',
            })
            .then(response => {
                this.hot_talks = response.data
            })
            .catch(error => {
                // console.log(error.response.data);
            });
        },

    },

})
