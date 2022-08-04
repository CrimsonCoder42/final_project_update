document.addEventListener('DOMContentLoaded', function () {

  // main views
  document.querySelector('#home_feed_bttn').addEventListener('click', () => home_feed() );
  document.querySelector('#your_profile_bttn').addEventListener( 'click', () => your_profile() );
  document.querySelector('#following_bttn').addEventListener( 'click', () => youFollowing() );
  document.querySelector('#wish_list_bttn').addEventListener( 'click', () => yourWishList() );
  document.querySelector('#notifications_bttn').addEventListener( 'click', () => notificationsMessaging() );
  document.querySelector('#update_profile').addEventListener( 'click', () => update_profile() );


    // get reply email element
  document.querySelector('#message_reply').addEventListener('click', () => reply() );





  // notification views

  document.querySelector('#messages_btn').addEventListener( 'click', () => message_view() );
  document.querySelector('#friend_request_btn').addEventListener( 'click', () => friend_requests() );
  document.querySelector('#booking_offers_btn').addEventListener( 'click', () => booking_offers() );


  // add event listener to all message subject lines so full message can be viewed.
  let links = document.getElementsByClassName('subject_link')
  Array.from(links).forEach(element => {

        element.addEventListener('click', () => view_message(element.id))
        });


 // add an event listener to every delete button.

let delete_ele = document.querySelectorAll('[data-name="Delete"]')
  Array.from(delete_ele).forEach(element => {
         element.addEventListener('click', () => remove_notice(element.dataset.id) );
         });

let delist_ele = document.querySelectorAll('[data-name="Delist"]')
  Array.from(delist_ele).forEach(element => {
            console.log( element.dataset.status)
         element.addEventListener('click', () => delist(element.dataset.id ,element.dataset.status) );

         });



  home_feed()

});

// declare all views in global variables and make hidden class in html.

  let home_view =document.querySelector('#home_feed')
  let profile_view =document.querySelector('#your_profile')
  let following_view =document.querySelector('#following')
  let wish_list =document.querySelector('#wish_list')
  let notifications_view =document.querySelector('#notifications')
  let property_listing_view =document.querySelector('#property_listing')
  let update_profile_view =document.querySelector('#update_profile_view')
  let messages_view =document.querySelector('#messages_view')
  let friend_requests_view =document.querySelector('#friend_requests_view')
  let booking_offers_view =document.querySelector('#booking_offers_view')
  let compose_view =document.querySelector('#compose-view')
  let emails_view =document.querySelector('#emails-view')


// Reset all views to hide classname so they won't appear cuts down on code and cleans UI

function view_reset() {
  home_view.className = 'hidden'
  wish_list.className = 'hidden'
  profile_view.className = 'hidden'
  following_view.className = 'hidden'
  notifications_view.className = 'hidden'
  property_listing_view.className = 'hidden'
  update_profile_view.className = 'hidden'
  friend_requests_view.className = 'hidden'
  booking_offers_view.className = 'hidden'
  compose_view.className = 'hidden'
  emails_view.className = 'hidden'
  messages_view.className = 'hidden'

}


// All visuals separated out.

function home_feed(){
    view_reset()
    home_view.className = 'display'

}

function your_profile(){
    view_reset()
    profile_view.className = 'display'

}

function youFollowing(){
  view_reset()
    following_view.className = 'display'

}

function yourWishList(){
    view_reset()
    wish_list.className = 'display'

}

function notificationsMessaging(){
  view_reset()
  notifications_view.className = 'display'

  message_view()
}


function message_view(){
    view_reset()
    notifications_view.className = 'display'
    messages_view.className = 'display'

}

function friend_requests(){
    view_reset()
    notifications_view.className = 'display'
    friend_requests_view.className = 'display'

}

function booking_offers(){
    view_reset()
    notifications_view.className = 'display'
    booking_offers_view.className = 'display'

}


function propertyListing(){
  document.querySelector('#home_feed').style.display = 'none';
  document.querySelector('#your_profile').style.display = 'none';
  document.querySelector('#following').style.display = 'none';
  document.querySelector('#wish_list').style.display = 'none';
  document.querySelector('#notifications').style.display = 'none';
  document.querySelector('#property_listing').style.display = 'block';
  document.querySelector('#update_profile_view').style.display = 'none';

}

function update_profile(){
    view_reset()
    update_profile_view.className = 'display'
}




function view_message(id) {
  let delete_in_view = document.getElementById('message_delete_view');


    fetch(`/notice/${id}`)
        .then(response => response.json())
        .then(message => {
            console.log(message.id)
          delete_in_view.addEventListener('click', () => remove_notice(message.id) );
          fill_in_values(message)
          console.log(delete_in_view)
        });

}

function fill_in_values(data) {
    view_reset()
    emails_view.className = 'display'
    notifications_view.className = 'display'

    console.log("fill in",data)
    let whoSent = data.sender

        document.querySelector('#email_sent_by').innerText = whoSent;

        document.querySelector('#dateTime').innerText = data.timestamp;
        document.querySelector('#email-subject').innerText = data.subject;
        document.querySelector('#email-body').value = data.body;

}


function reply() {


    let senderEmail = document.getElementById('email_sent_by').innerText
    let subject = document.getElementById('email-subject').innerText
    let body = document.getElementById('email-body').value
    let datetime = document.getElementById('dateTime').innerText

    console.log(senderEmail)
    console.log(subject)
    console.log(body)
    console.log(datetime)


    document.querySelector('#compose-recipients').value = senderEmail
    document.querySelector('#compose-subject').value = `Re: ${subject}`
    document.querySelector('#compose-body').value = `on ${datetime}, ${senderEmail} wrote: ${body}`

    view_reset()
    compose_view.className = 'display'
    notifications_view.className = 'display'
}

function remove_notice(id) {
    // get element by ID which is also dataset for delete button and apply hidden for auto removal

    let remove_ele =document.getElementById(`${id}`)
    remove_ele.className = 'hidden'
    view_reset()
    notifications_view.className = 'display'
    messages_view.className = 'display'

    fetch(`/notice/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
    })

  }

  // runs like remove_notice except that you can toggle the real estate listing between active and inactive

  function delist(id,bool) {

    let new_bool = bool_switch(bool)

    fetch(`/property/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            active: bool_switch(bool)
        })
    }).then(location.reload())

  }

// simple helper bool switch function
  function bool_switch(bool) {

      if(bool === "True"){
          return false
      }else {
          return true
      }

}



