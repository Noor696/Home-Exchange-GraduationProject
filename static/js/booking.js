var updateBtns = document.getElementsByClassName('update-booking')


for (var i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var homeId = this.dataset.home
		var action = this.dataset.action
		console.log('homeId:', homeId, 'Action:', action)
		
        console.log('USER:', user)

		if (user == 'AnonymousUser'){
            console.log('not logged in')
			// addCookieItem(homeId, action)
		}else{
            console.log('user logged in , sending data')
			updateUserBooking(homeId, action)
		}
	})
}

function updateUserBooking(homeId, action){
	console.log('User is authenticated, sending data...')

	var url = '/update_home/'
// to send our post data we are using the fatch
// we want to define what kind of data we are going to send to the back end
	fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'homeId':homeId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})

		.then((data) => {
            console.log('data:',data)
		    location.reload()
		})
}
