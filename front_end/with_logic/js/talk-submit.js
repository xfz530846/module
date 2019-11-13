
var pub_talk = new Vue({
     el: '#pub_talk',
    data: {
        host:HOST,
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,

        detail:"",
        data_config: {
            "filebrowserUploadUrl": HOST + '/ckeditor/upload/?token=' + sessionStorage.token || localStorage.token,
            "toolbar_Full": [["Styles", "Format",
                                "Bold", "Italic",
                                "Underline", "Strike",
                                "SpellChecker", "Undo", "Redo"],
                            ["Link", "Unlink", "Anchor"],
                            ["Image", "Flash", "Table", "HorizontalRule"],
                            ["TextColor", "BGColor"],
                            ["Smiley", "SpecialChar"], ["Source"]]
        },

    },
    methods: {
            publish_talk:function(){
                this.detail = CKEDITOR.instances.financial.getData()
                if (this.detail){
            axios.post(this.host+'/publishtalk/' ,{

                    detail:this.detail

                }, {
                    responseType: 'json',
                    headers:{
                        'Authorization': 'JWT ' + this.token
                    },
                    withCredentials: true
                })
            .then(response => {
                console.log(response.data)
                location.href=("talk-index.html")
            })
            .catch(error => {
                // alert(like_count)
                location.href = 'person-loginsign.html'
                console.log(error.response.data)
            });}else{
                    alert("请输入内容")
                }

        },


    },
    mounted: function () {

         CKEDITOR.replace('financial', this.data_config);
    }

});

