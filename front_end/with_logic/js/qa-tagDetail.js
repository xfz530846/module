/**
 * Created by python on 19-8-29.
 */

var qa_list = new Vue({
    el: '#qa_list',
    data: {
        questions: [],
        c_id:'',
        page:1,
        page_size:6,
        count:0,
        timeClass:'active',
        usefulClass:'',

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
            })},
         // 点击页数
        on_page: function(num){
            if (num != this.page){
                this.page = num;
                this.get_question_list('-create_time','' ,this.c_id);
            }
        },
    },
        mounted: function () {
            this.c_id = get_id()
            this.get_question_list('-create_time','' ,this.c_id)
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

var label_new = new Vue({
     el: '#label_new',
    data: {
        label:'',
        categories: '',
        id:'',
        default_cat: {
        "name": "全部",
        "id": "0"
        },
        label_id:'',
        is_focused:'',
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        attention_status:0,
    },
   methods: {
        get_cate: function(){
            axios.get(HOST+'/qa_category?label_id=' + this.id ,{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response=>{
            this.label =response.data
            })
        },
       // 关注
        attention: function (label_id) {
            if (!this.token) {
                location.href = '/person-loginsign.html?next='+location.href
            }
            axios.post(HOST + '/label_focus/', {
                "label": label_id,
            },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                this.label.attention_status = 1;
                // alert(response.data.message);

            })
            .catch(error => {
                alert(error.response.data.message);
            })
        },
        // 取消关注
        unattention: function (label_id) {
            if (!this.token) {
                location.href = '/person-loginsign.html'
            }
            axios.delete(HOST + '/label_unfocus/' + label_id ,{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                if (response.status == 204) {
                    this.label.attention_status = 0;
                    // alert('取消关注成功');
                }

            })
            .catch(error => {
                alert(1)
                alert(error.response.data.message);
            })
        },

   },
    mounted: function(){
       this.id =  get_id()
       this.get_cate()
    },
})

var hot_label = new Vue({

     el: '#hot_label',
    data: {
        categories:null,
    },
   methods: {
        get_categories: function(){
            axios.get(HOST+'/qa_categories?order=')
            .then(response=>{
            this.categories=response.data
            })
        },
   },
    mounted: function(){
        this.get_categories()

    },
})

function get_id() {
    var c_id = get_query_string('c_id', null)
    if (c_id == null) {
        location.href = '/'
    } else {
        return c_id
    }}