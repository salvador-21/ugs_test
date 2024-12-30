$(document).ready(function(){


    $(document).on('click','.subscribe_btn',function(){
        movie=$(this).attr('id')
        mname=$(this).attr('mname')
        chk_subscription(movie,mname)
        
    })


    function chk_subscription(movie,mname){
        $.ajax({
            method:'POST',
            url:'../../chk_subscibe',
            data:{movie},
            success:function(res){
                if(res.data == 'bad'){
                    // 
                    Swal.fire({
                        title: "Watch for only P10 ?",
                        text: mname,
                        icon: "warning",
                        showCancelButton: true,
                        confirmButtonColor: "#3085d6",
                        cancelButtonColor: "#d33",
                        confirmButtonText: "Proceed!"
                    }).then((result) => {
                        if (result.isConfirmed) {
                            
                            $.ajax({
                                method:'POST',
                                url:'../../add_subscribe',
                                data:{movie},
                                success:function(res){
                                    // console.log(res.data)
                                    if(res.data =='ok'){
                                        // console.log(res.data)
                                        window.location.href="/movie_arena/"+movie;
                                    }else{

                                        Swal.fire({
                                            title: res.data,
                                            icon: "error"
                                        });
                                    }
                                }
                            })

                        }
                    });
                    // 
                }else{
                  
                    window.location.href="/movie_arena/"+movie;

                }
            }
        })
    }

    $(document).on('click','#g_type',function(){
        type=$(this).attr('type')
    
        if(type == 'E-SABONG'){
            $('#e_sabong').addClass('lnk_active')
            $('#e_sports').removeClass('lnk_active')
            $('#e_perya').removeClass('lnk_active')
            $('#e_movies').removeClass('lnk_active')
        }else if(type == 'E-SPORTS'){
            $('#e_sports').addClass('lnk_active')
            $('#e_sabong').removeClass('lnk_active')
            $('#e_perya').removeClass('lnk_active')
            $('#e_movies').removeClass('lnk_active')
        }else if(type == 'E-PERYA'){
            $('#e_perya').addClass('lnk_active')
            $('#e_sports').removeClass('lnk_active')
            $('#e_sabong').removeClass('lnk_active')
            $('#e_movies').removeClass('lnk_active')
        }else if(type == 'E-MOVIES'){
            $('#e_movies').addClass('lnk_active')
            $('#e_sports').removeClass('lnk_active')
            $('#e_sabong').removeClass('lnk_active')
            $('#e_perya').removeClass('lnk_active')
        }
    
        $.ajax({
            method:'POST',
            url:'player_games',
            data:{type:type},
            success:function(res){
                $('#games').html('')
                if(res.data.length > 0){
                    for(g in res.data){
                        console.log(res.data[g].gname)
                        data='<div class="col-6 col-md-3 mb-4">\
                          <div class="card">\
                          <a  id="'+res.data[g].g_id+'" href="/player/arena/'+res.data[g].g_id+'">\
                           <div class="card-body">\
                            <img class="rounded-3 mb-4 w-100" src="uploads/'+res.data[g].g_image+'" alt="">\
                              <h2 class="card-title mb-2">'+res.data[g].g_name+'</h2>\
                                <p class="card-text">'+res.data[g].g_desc+'</p>\
                                 </div></a></div></div>'
        
                        $('#games').append(data)
                    }
    
    
                }else{
                    $('#games').append('<h4 class="text-danger fw-bolder text-center">NO AVAILABLE IN '+type+'</h4>')
                }
                
    
    
            }
        })
    
        // $('#games').html('')
        // $('#games').append(type)
    
    })


    $(document).on('change', '.fightEvents', function() {
        var geventval = $(this).val();
        if (geventval !== "") {
            $('.tablespinner').show();
            $.ajax({
                method: 'POST',
                url: 'bettingevent',
                data: {
                    geventval: geventval,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                },
                success: function(res) {
                    $("#betglogstbl").html(res);
                },
                error: function(xhr, status, error) {
                    console.error("Error:", error);
                }
            });
        }
    });
    
    
    })