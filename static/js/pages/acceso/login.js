// CONFIG FORM
const SendDataJSONForm = async (url, form, callback) => {
	try {
		const formData = new FormData(form);

		const response = await fetch (url, {
			method: "POST",
			body: formData
		});
		const data = await response.json();

		notifier.show(data['response']['title'], data['response']['data'], data['response']['type_response'], '', 4000);
		if (data['response']['type_response'] === 'danger') {
			console.log(data);
			return false
		}

		callback();

	} catch (error) {
		notifier.show('Ocurrió un error!', error, 'danger', '', 4000);
		console.log(error);
	}
}

// FORM VIEW LOGIC

let form_login = document.getElementById('form_login');

$( async function () {

	// LOGIN SEND FORM
	form_login.addEventListener('submit', async (e) => {
        e.preventDefault();
        await SendDataJSONForm(window.location.pathname, form_login, async () => {  
            setTimeout(() => {
                window.location.replace('/inicio/');
            }, 1000); // Espera 3 segundos antes de ejecutar el código dentro de setTimeout
        });
    });
    

});