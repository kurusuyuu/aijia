function logout() {
    $.get("/api/logout", function(data){
        if(date.code=='200'){
            location.href = "/user/login/";
        }


    })
}

$(document).ready(function(){
    
    $.get('/user/user/',function (data) {
        if(data.code=='200'){
            $('#user-mobile').html(data.user.phone);
            $('#user-name').html(data.user.name);
            $('#user-avatar').attr('src',data.user.avatar);
        }

    })
})