// var id = ""
// var nickname = ""
var talk_detail = new Vue({

        el: '#talk_detail',
        data: {
            host: HOST,
            id: '',
            talk: '',
            user:"",
            take_id:"",

            username: sessionStorage.username || localStorage.username,
            user_id: sessionStorage.user_id || localStorage.user_id,
            token: sessionStorage.token || localStorage.token,
        },
        methods: {
               publish_comment:function(){
                talk_comments.publish_comment_show = true
                   talk_comments.user = get_user()

        },
              talkcollections:function(){
                   var talk_id = get_id()
            axios.post(this.host+'/talkcollections/' ,{

                        talk_id:talk_id,

                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                    withCredentials: true
                })
            .then(response => {

                 if (response.data.msg == 'collect_success')

                {
                    this.talk.is_collect =1}
                else if(response.data.msg == 'cancel_collect'){



                     this.talk.is_collect =0
                }


            })
            .catch(error => {
                // alert(like_count)
                // location.href = 'person-loginsign.html'
                console.log(error.response)
            });
        },

            get_talk: function () {
                if(this.username){
                    axios.get(this.host + '/talk/' + this.id + '/', {
                        headers: {
                            'Authorization': 'JWT ' + this.token
                        },
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            this.talk = response.data
                            console.log(response.data)
                        })
                        .catch(error => {
                            console.log(error.response.data);
                        })
                    }
                        else {
                    axios.get(this.host + '/talk/' + this.id + '/', {
                        responseType: 'json',
                        withCredentials: true
                    })
                        .then(response => {
                            this.talk = response.data
                            console.log(response.data)
                        })
                        .catch(error => {
                            console.log(error.response.data);
                        })

                }
                    },
            talklike:function(){
            axios.post(this.host+'/talklike/' ,{
                        talk_id:this.id
                }, {
                 headers:{
                    'Authorization': 'JWT ' + this.token
                },
                    responseType: 'json',
                    withCredentials: true
                })
            .then(response => {

               if (response.data.msg == 'like_success')
                {this.talk.like_count +=1
                    this.talk.is_like = 1

                }else if(response.data.msg == 'cancel_like'){
                    this.talk.like_count -=1
                    this.talk.is_like = 0
                }
            })
            .catch(error => {
                // // alert(like_count)
                // location.href = 'person-loginsign.html'
                console.log(response.data)
            });
        },
                },
            mounted: function () {
                this.id = get_id()
                this.get_talk()
                this.get_user()
            },
        })

var talk_comments = new Vue({
    el: '#talk_comments',
    data: {
        host: HOST,
        id: '',
        talk: talk_detail.talk,
        talk_id:"",
        avatar_url:"",

        comments:[],
        publish_comment_show:false,
        user1:"",
        talk_commment_message:"",
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
    },
    methods: {

        get_comments: function () {

            if (this.username) {
                axios.get(this.host + '/talk_comments/' + this.id + '/', {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                        this.comments = response.data
                        console.log(response.data)

                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
            else {
                axios.get(this.host + '/talk_comments/' + this.id + '/', {
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                        this.comments = response.data
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
        comment_like: function (index) {
            axios.post(this.host + '/talk_comment_like/', {

                comment_id: this.comments[index].id,

            }, {
                responseType: 'json',
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                withCredentials: true
            })
                .then(response => {
                    console.log(response.data)
                  if (response.data.msg == 'like_success')
                {this.comments[index].like_count +=1
                    this.comments[index].is_like = 1

                }else if(response.data.msg == 'cancel_like'){
                    this.comments[index].like_count -=1
                    this.comments[index].is_like = 0
                }

                })
                .catch(error => {
                    // alert(like_count)
                    // location.href = 'person-loginsign.html'
                    console.log(response.data)
                });
        },talklike:function(){
            axios.post(this.host+'/talklike/' ,{
                        talk_id:this.id
                }, {
                 headers:{
                    'Authorization': 'JWT ' + this.token
                },
                    responseType: 'json',
                    withCredentials: true
                })
            .then(response => {

                // location.reload()
            })
            .catch(error => {
                // // alert(like_count)
                // location.href = 'person-loginsign.html'
                console.log(response.data)
            });
        },
          talk_comment: function() {
            this.talk_id = get_id()


            if (this.talk_commment_message && this.talk_id ) {
                axios.post(this.host + '/talk/comments/', {
                    content: this.talk_commment_message,
                    talk_id:this.talk_id,
                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                })
                .then(response => {
                    this.comments.unshift(response.data)
                    // this.comments_detail.unshift(response.data)
                    // this.control_comments_count(this.comments_detail)
                    // this.content = ''
                    // this.headlines_detail.comment_counts += 1
                    console.log(response.data)
                    talk_detail.talk.comment_count+=1
                    // this.avatar_url = reaponse.data.user.avatar_url

                })
                .catch(error => {
                    location.href="person-loginsign.html"
                });
            } else {
                alert('内容不能为空')
            }
        },


    },

    mounted: function (){
        this.id = get_id()
        this.get_comments()
        this.user = get_user ()


    },
});


function get_query_string(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}

function get_id() {
    var talk_id = get_query_string('talk_id', null)
    if (talk_id == null) {
        location.href = '/'
    } else {
        return talk_id
    }}

function get_user(){
    axios.get(this.host +'/user/' ,{
            headers: {
                'Authorization': 'JWT ' + this.token
            },
            responseType: 'json',
            withCredentials: true
        })
        .then(response => {
            user = response.data
        })
        .catch(error => {
            console.log(error.response.data);
        })
    }

function get_id() {
    var talk_id = get_query_string('talk_id', null)
    if (talk_id == null) {
        location.href = '/'
    } else {
        return talk_id
    }}