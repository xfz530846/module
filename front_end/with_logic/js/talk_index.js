/**
 * Created by python on 19-8-24.
 */

// [
//     {
//         "id": 1,
//         "detail": "过了要回去等offer，现在都两周了，还说在ceo审批，两天联系hr一次",
//         "user_id": 1,
//         "comment_count": 0,
//         "create_time": "2019-08-24T17:38:27.733486+08:00"
//     },
//     {
//         "id": 2,
//         "detail": "过了要回去等offer，现在都两周了，还说在ceo审批，两天联系hr一次",
//         "user_id": 1,
//         "comment_count": 0,
//         "create_time": "2019-08-24T17:57:01.561523+08:00"
//     },
//     {
//         "id": 5,
//         "detail": "过了要回去等offer，现在都两周了，还说在ceo审批，两天联系hr一次",
//         "user_id": 1,
//         "comment_count": 0,
//         "create_time": "2019-08-24T18:02:36.079223+08:00"
//     }
// ]

var talk_list =new Vue({
    el: '#talk_list',
    data: {
        host:HOST,
        detail_list:"",
        talks:[],
        talk_id:"",
        is_active:true,
        has_error:false,
        // user:vm.user,
        is_collect:"",
        is_like:"",


        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,

    },
    methods:{
        talklist:function(){

             if(this.username){
            axios.get(this.host+'/talklist/' ,{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                this.talks = response.data
                 console.log(response.data)

                // alert("haha")
                // alert(response.data[0].detail)


            })
            .catch(error => {

                console.log(response.data)

            });}
            else {
        axios.get(this.host+'/talklist/' ,{
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                this.talks = response.data
                 console.log(response.data)

                // alert("haha")
                // alert(response.data[0].detail)


            })
            .catch(error => {

                console.log(response.data)

            });

             }

            
        },
         talklike:function(index){
            axios.post(this.host+'/talklike/' ,{

                        talk_id:this.talks[index].id,

                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                    withCredentials: true
                })
            .then(response => {

                // this.talks = reponse.data
                if (response.data.msg == 'like_success')
                {this.talks[index].like_count +=1
                    this.talks[index].is_like = 1

                }else if(response.data.msg == 'cancel_like'){
                    this.talks[index].like_count -=1
                    this.talks[index].is_like = 0
                }


                // location.reload()



            })
            .catch(error => {
                // alert(like_count)
                location.href = 'person-loginsign.html?next=' + location.href
                console.log(response.data)
            });
        },
        talkcollections:function(index){
            axios.post(this.host+'/talkcollections/' ,{

                        talk_id:this.talks[index].id,

                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                    withCredentials: true
                })
            .then(response => {
                 if (response.data.msg == 'collect_success')
                {this.talks[index].is_collect =1}
                else if(response.data.msg == 'cancel_collect'){
                     this.talks[index].is_collect =0
                }


            })
            .catch(error => {
                // alert(like_count)
                location.href = 'person-loginsign.html'
                console.log(response.data)
            });
        },

    },
       mounted: function(){
        this.talklist();
    },
    
})
