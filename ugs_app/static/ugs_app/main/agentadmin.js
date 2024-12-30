$(document).ready(function(){
    // /////////////////////////////////
    
    // $(document).on('click','.btn-stat',function(){
        
    //     $('#admin_upuser').modal('show')
    
        
    // })
    
    
    
    
    // $('#account_reg').on('submit',function(e){
    //     e.preventDefault()
    //     $('.adduser_err').html('')
    //     data=$(this).serializeArray()
    //     if($('.pass1').val() != $('.pass2').val()){
    //     $('.adduser_err').append('<div class="alert alert-danger alert-dismissible fade show" role="alert">\
    //     <strong>Password Not Matched!</strong>\
    //     <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
    //     </div>')
    //     }else{
            
    //         $.ajax({
    //             method:'POST',
    //             url:'account_reg',
    //             data:data,
    //             success:function(res){
    //                 if(res.data == 'ok'){
    //                   $('#account_reg').trigger('reset')
    //                 //   load_users()
    //                     $('.adduser_err').append('<div class="alert alert-success alert-dismissible fade show" role="alert">\
    //                     <strong>Account was Created!</strong>\
    //                     <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
    //                     </div>')
    //                 }
    //             }
    //         })
    
    //     }    
    // })
    // ///////////////////////////////
    })
    
    
    
    // $(document).on('click','.coutbtn',function(){
    //     requestor=$(this).attr('requestor')
    //     outid=$(this).attr('out_id')
    //     outamt=$(this).attr('out_amt')
    //     $('.requestor').text(requestor)
    //     $('.coutid').text(outid)
    //     $('.outamt').text(outamt)
    //     $('#vcoutid').val(outid)
    //     $('#coutstat').val('')
    //     $('.cstat').text('')
    //     $('#agentcashout').modal('show')
    // })
    
    // function cashoutaction(thisval){
    //     var selectedValue = thisval.value;
    //     if(selectedValue){
    //         document.getElementById('cashoutbtn').disabled = false;
    //         if(selectedValue == 1){
    //             $('.cstat').text('Approve')
    //         }else{
    //             $('.cstat').text('Decline')
    //         }
    //     }else{
    //         $('.cstat').text('Decline')
    //         document.getElementById('cashoutbtn').disabled = true;
    //     }
    // }
    
    // $(document).on('submit','#agenCahoutFrom',function(e){
    //     e.preventDefault()
    //     var coutstat   = document.getElementById("coutstat").value;
    //     var vcoutid   = document.getElementById("vcoutid").value;
    //     if(coutstat && vcoutid){
    //         Swal.fire({
    //             title: "Process cash out?",
    //             text: "Process now",
    //             icon: "question",
    //             showCancelButton: true,
    //             confirmButtonColor: "#3085d6",
    //             cancelButtonColor: "#d33",
    //             confirmButtonText: "Proceed!"
    //         }).then((result) => {
    //             if (result.isConfirmed) {
    //                 document.getElementById('cashoutbtn').disabled = true;
    //                 $.ajax({
    //                     method: 'POST',
    //                     url:'coutapproval',
    //                     data:{coutstat:coutstat,vcoutid:vcoutid},
    //                     success: function(res) {
    //                         document.getElementById('cashoutbtn').disabled = false;
    //                         if (res.data == 'approved') {
    //                             document.getElementById("agenttbal").innerHTML=res.bal;
    //                             document.getElementById("reqbal").innerHTML=res.reqbal;
    //                             document.getElementById("appbal").innerHTML=res.appbal;
                                
    //                             toastr["success"]("Player cashout was successfully approved!");
    //                             document.getElementById("coutstat").value="";
    //                             $('#agentcashout').modal('hide')
    //                             $("#import_new_table").load('loadagentcOut');
                            
    //                         }else if (res.data == 'declined') {
    //                             document.getElementById("reqbal").innerHTML=res.reqbal;
    //                             document.getElementById("decbal").innerHTML=res.decbal;
    //                             toastr["success"]("The cashout request was successfully declined.");
    //                             document.getElementById("coutstat").value="";
    //                             $('#agentcashout').modal('hide')
    //                             $("#import_new_table").load('loadagentcOut');
    //                         }
    //                         else if (res.data === 'error') {
    //                             toastr["error"]("Something went wrong. Please try again.");  
                    
    //                         }else if (res.data === 'bad') {
    //                             toastr["error"]("Something went wrong. Please try again....");  
                    
    //                         }else {
    //                             toastr["warning"]("Error: " + JSON.stringify(res.errors));
    //                         }
    //                     }
    //                 });
    //             }
    //         });
    //     }else{
    //         toastr["error"]("Invalid inputs!"); 
    //     }
    // })