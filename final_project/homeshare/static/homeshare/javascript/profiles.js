document.addEventListener('DOMContentLoaded', function () {

  document.querySelector('#messagebttn').addEventListener('click', () => message_toggle() );
  document.querySelector('#message').addEventListener('click', send_message);
  document.querySelector('#friend_request_btn').addEventListener('click', friend_request);

  document.querySelector('#compose-view').style.display = 'none';


});

let messge_view = false;

function message_toggle(){

  if (messge_view == true) {
    document.querySelector('#compose-view').style.display = 'block';
    messge_view=false;
  } else{
    document.querySelector('#compose-view').style.display = 'none';
    messge_view=true;
  }

}

// sends a simple written message from one user to another.
function send_message() {

    fetch('/create_alert', {
            method: 'POST',
            body: JSON.stringify({
                recipients: document.querySelector('#compose-recipients').value,
                subject: document.querySelector('#compose-subject').value,
                body: document.querySelector('#compose-body').value
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            clearout()
        });

}

function friend_request() {

    fetch('/create_alert', {
            method: 'POST',
            body: JSON.stringify({
                recipients: document.querySelector('#friend_receiver').value,
                subject: document.querySelector('#friend_subject').value,
                body: document.querySelector('#friend_body').value,
                follow_request: true
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result)

        });

}

function clearout(){
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    message_toggle()
}
