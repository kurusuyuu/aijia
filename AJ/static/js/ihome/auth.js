
function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){});
        },1000)
    });
}

$.get('/user/auths/', function(data){
    if(data.code == '200'){
        $('#real-name').val(data.id_name);
        $('#id-card').val(data.id_card);
        $('.btn-success').hide();
    }
});

$('#form-auth').submit(function () {
    $.ajax({
        url: '/user/auths/',
        type: 'PUT',
        dataType: 'json',
        data: {
            'id_name': $('#real-name').val(),
            'id_card': $('#id-card').val(),
        },
        success: function (data) {
            if(data.code == '200'){
                $('.btn-success').hide();
                $('.error-msg').hide();
            }else{
                $('.error-msg').html('<i class="fa fa-exclamation-circle">身份信息有误</i>');
                $('.error-msg').show();
            }
        },
        error: function (data) {
            alert('请求失败')
        }
    });
    return false
})