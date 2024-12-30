$(document).ready(function(){
    $("form").attr('autocomplete', 'off');

    $('#passform').on('submit',function(e){
        e.preventDefault()
        data=$(this).serializeArray()
        $('.set_notif').html('')
        p1=$('.p1').val()
        p2=$('.p2').val()
        user=$('.username').val()

        console.log(data)
        if(p1 != p2){
            $('.set_notif').append('<div class="alert alert-danger alert-dismissible fade show" role="alert">\
                <strong>Password Not Matched!</strong>\
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                </div>')
        }else{

            $.ajax({
                method:'POST',
                url:'uppass',
                data:data,
                success:function(res){
                   if(res.data == 'ok'){
                    $('#passform').trigger('reset')
                    $('.set_notif').append('<div class="alert alert-success alert-dismissible fade show" role="alert">\
                        <strong>Account Update Successfully!</strong>\
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                        </div>')
                    $('.username').val(user)
                    $('.usertext').text(user)
                   }else{
                    $('.set_notif').append('<div class="alert alert-danger alert-dismissible fade show" role="alert">\
                        <strong>'+res.data+'!</strong>\
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
                        </div>')
                   }
                }
            })


        }

        
        
    })



})