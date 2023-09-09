new Vue({
    el: '#doc_id',
    data: {docs: []},
    created: function() {
        const vm = this;
        axios.get('/docs/api/')
        .then(function (response){
        console.log(response.data)
        vm.docs = response.data
        })
    }
})