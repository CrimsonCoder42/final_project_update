document.addEventListener('DOMContentLoaded', function () {

  document.querySelector('#booking').addEventListener('click', () => message_toggle() );
  document.querySelector('#book').addEventListener('click', send_message);

  document.querySelector('#property_compose-view').style.display = 'none';


});

let messge_view = false;

function message_toggle(){

  if (messge_view == true) {
    document.querySelector('#property_compose-view').style.display = 'block';
    messge_view=false;
  } else{
    document.querySelector('#property_compose-view').style.display = 'none';
    messge_view=true;
  }

}

// sends a simple written message from one user to another.
function send_message() {

    let subject = document.querySelector('#compose-subject').value
    let body = document.querySelector('#compose-body').value
    let sender = document.querySelector('#compose-body').value

    fetch('/create_alert', {
            method: 'POST',
            body: JSON.stringify({
                recipients: document.querySelector('#compose-recipients').value,
                subject: `${sender}  would is interested in your property from ${subject} to ${body}  `,
                body: document.querySelector('#compose-body').value,
                book_location: true

            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            clearout()
        });

}


function clearout(){
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

    message_toggle()
}

