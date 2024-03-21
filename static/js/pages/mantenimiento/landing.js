let form_landing = document.getElementById('form_landing');

$( async function () {

	// LABS SEND FORM
	form_landing.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_landing);
        await SendDataJsonForm(type_actions['landing'][action.value], parameters, async () => {  
            $("#form_landing")[0].reset(); 
            window.location.reload();
        });
    });
    
});