/**
 * Created by python on 19-8-23.
 */

// 头条列表
var headline_info = new Vue({
     el: '#headline_info',
    data: {
        host:HOST,
        headlines: [],
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        category_id : '',
        page_size: 17,
        next: '',
        page: 1,
    },
    methods: {

        // 获取头条列表
        get_headlines: function (category_id){
            this.category_id = category_id;
            if (!this.token) {
                axios.get(this.host + '/headlines/', {
                    params: {
                        "category_id": this.category_id,
                        "page_size": this.page_size,
                    },
                    responseType: 'json',
                })
                .then(response => {
                    this.headlines = response.data.results;
                    this.next = response.data.next;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
            }else {
                axios.get(this.host + '/headlines/', {
                    params: {
                        "category_id": this.category_id,
                        "page_size": this.page_size,
                    },
                    headers: {
                    'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                })
                .then(response => {
                    this.headlines = response.data.results;
                    this.next = response.data.next;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
            }

        },
        // 移除头条
        delete_headline: function (index) {
            this.headlines.splice(index, 1);
        },

        // 关注作者
        attention: function (headline_id, author_id, index) {
            if (!this.token) {
                location.href = '/person-loginsign.html'
            }
            axios.post(this.host + '/user/follow/', {
                "followeds": author_id,
            },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                this.headlines[index].attention_status = 1;
                // alert(response.data.message);

            })
            .catch(error => {
                console.log(error.response.data.message);
            })
        },

        // 取消关注作者
        unattention: function (headline_id, author_id, index) {
            if (!this.token) {
                location.href = '/person-loginsign.html'
            }
            axios.delete(this.host + '/user/'+ author_id +'/follow/',{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                if (response.status == 204) {
                    this.headlines[index].attention_status = 0;
                    // alert('取消关注成功');
                }

            })
            .catch(error => {
                console.log(error.response.data.message);
            })
        },



    },
    mounted: function(){
        this.get_headlines(this.category_id);
        console.log(this.page)
        // 设置开关避免负重请求数据
        let sw = true;
        // 注册scroll事件并监听
        window.addEventListener('scroll',function(){
            // scrollTop 滚动条滚动时，距离顶部的距离
            var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            // windowHeight 可视区的高度
            var windowHeight = document.documentElement.clientHeight || document.body.clientHeight;
            // scrollHeight 滚动条的总高度
            var scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;

            // 滚动条到底部的条件
            if(scrollTop + windowHeight == scrollHeight) {
                // console.log(sw);
                // 如果开关打开则加载数据
                if(sw==true){
                    // 将开关关闭
                    sw = false;
                    // console.log(headline_info.next)
                    axios.get(headline_info.next, {
                        // params: {
                        //     "category_id": this.category_id,
                        //     "page_size": this.page_size,
                        // },
                        responseType: 'json',
                    })
                    .then(response => {
                        response.data.results.forEach(function (val, index) {
                            headline_info.headlines.push(val);
                        });
                        console.log(this.headlines)
                        headline_info.next = response.data.next;
                        // 数据更新完毕，将开关打开
                        sw = true
                    })
                    .catch(error => {
                        // console.log(this.next)
                        console.log(error.response.data);
                    })
                }
            }
        });


    },
});

// 头条分类列表
var category_info = new Vue({
     el: '#category_info',
    data: {
        host:HOST,
        categories: [],
        default_cat: {
            "name": "热门",
            "id": ""
        },
        activeClass: 0
    },
    methods: {
        // 获取头条分类
        get_headlines_category: function () {
            axios.get(this.host + '/headline/categories/', {
                responseType: 'json',
            })
            .then(response => {
                this.categories = response.data;
                this.categories.unshift(this.default_cat)
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
        get_headline_list: function (category_id, index) {
            headline_info.get_headlines(category_id)
            this.activeClass = index
        },

    },
    mounted: function(){

        this.get_headlines_category();
    },
});

// 轮播图列表
var carousel_info = new Vue({
    el: '#carousel_info',
    data: {
        host:HOST,
        carousels: [],
        currentIndex: 0,
        timer: '',
    },
    created() {
        this.$nextTick(() => {
            this.timer = setInterval(() => {
                this.autoPlay()
            }, 4000)
        })
    },
    methods: {

        // 获取轮播图列表
        get_carousels: function () {
            axios.get(this.host + '/carousels/', {
                responseType: 'json',
            })
            .then(response => {
                this.carousels = response.data;
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },

        go() {
            this.timer = setInterval(() => {
                this.autoPlay()
            }, 4000)
        },
        stop() {
            clearInterval(this.timer)
            this.timer = null
        },
        change(index) {
            this.currentIndex = index
        },
        autoPlay() {
            this.currentIndex++
            if (this.currentIndex > this.carousels.length - 1) {
                this.currentIndex = 0
            }
        },


    },
    mounted: function(){

        this.get_carousels();
    },
});

// 热门问题
var questions_info = new Vue({
    el: '#questions_info',
    data: {
        host:HOST,
        hot_questions: [],
    },
    methods: {

        // 获取轮播图列表
        get_questions: function () {
            axios.get(this.host + '/questions/hot', {
                responseType: 'json',
            })
            .then(response => {
                this.hot_questions = response.data;
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },

    },
    mounted: function(){

        this.get_questions();
    },
});


