
var pub_headline = new Vue({
     el: '#pub_headline',
    data: {
        host:HOST,
        title: '',
        content: '',
        category_id: '',
        categories: [],
        token: sessionStorage.token || localStorage.token,
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
        checkedLabels: [],
        labels: []

    },
    methods: {
        // 阻止默认表单提交
        onSubmit: function () {
            return false;
        },

        // 获取头条分类
        get_headlines_category: function () {
            axios.get(this.host + '/headline/categories/', {
                responseType: 'json',
            })
            .then(response => {
                this.categories = response.data;
            })
            .catch(error => {
                console.log(error.response.data);
            })
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
        submit_headline: function () {
            // console.log(CKEDITOR.instances.financial.getData())
            var content = CKEDITOR.instances.financial.getData();
            if (this.title && content && this.category_id) {
                axios.post(this.host + '/headlines/' + this.category_id + '/', {
                    "title": this.title,
                    "content": content,
                    "labels": this.checkedLabels
                }, {
                    headers: {
                    'Authorization': 'JWT ' + this.token
                },
                    responseType: 'json',
                })
                .then(response => {
                    alert('发布成功')
                    location.href = '/'
                    // alert(response.data.message)
                })
                .catch(error => {
                    alert(error.response.data.message);

                })
            }
        },



    },
    mounted: function () {
        this.get_headlines_category();
        this.get_labels();

        CKEDITOR.replace('financial', this.data_config);
    }

});

