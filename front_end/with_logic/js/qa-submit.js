
var pub_question = new Vue({
    el: '#pub_question',
    data: {
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
        host:HOST,
        token: sessionStorage.token || localStorage.token,
        tag_id: '',
        labels: [],
        title: '',
    },
    methods: {
        // 阻止默认表单提交
        onSubmit: function () {
            return false;
        },

        // 获取头条标签
        get_labels: function () {
            axios.get(this.host + '/headlines/labels/', {
                responseType: 'json',
            })
            .then(response => {
                this.labels = response.data;
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },

        // 发布头条
        submit_question: function () {
            // console.log(CKEDITOR.instances.financial.getData())
            var content = CKEDITOR.instances.financial.getData();
            if (this.title && content && this.tag_id) {
                axios.post(this.host + '/questions/submit/', {
                    "title": this.title,
                    "detail": content,
                    "label": this.tag_id,
                    "answers_count": 0,
                }, {
                    headers: {
                    'Authorization': 'JWT ' + this.token
                },
                    responseType: 'json',
                })
                .then(response => {
                    alert('发布成功')
                    location.href = '/qa-submit.html'
                    // alert(response.data.message)
                })
                .catch(error => {
                    alert(error.response.data.message);

                })
            }
        },


    },
    mounted: function () {

         this.get_labels();
         CKEDITOR.replace('financial', this.data_config);
    }

});

