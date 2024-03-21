function PagePrevious() {
	window.history.back();
}

//Solo numeros
function Solo_Numero(e){
	var keynum = window.event ? window.event.keyCode : e.which;
	if ((keynum == 8) || (keynum == 46))
	return true;
	return /\d/.test(String.fromCharCode(keynum));
}
  
//Solo texto
function Solo_Texto(e) {
	var code;
	if (!e) var e = window.event;
	if (e.keyCode) code = e.keyCode;
	else if (e.which) code = e.which;
	var character = String.fromCharCode(code);
	var AllowRegex  = /^[\ba-zA-Z\s]$/;
	if (AllowRegex.test(character)) return true;     
	return false; 
}
  //Solo numeros sin puntos 
function Solo_Numero_ci(e){
	var keynum = window.event ? window.event.keyCode : e.which;
	if ((keynum == 8))
	return true;
	return /\d/.test(String.fromCharCode(keynum));
}
  
  // solo numeros y letras sin caracteres especiales
function Texto_Numeros(e) {
	var code;
	if (!e) var e = window.event;
	if (e.keyCode) code = e.keyCode;
	else if (e.which) code = e.which;
	var character = String.fromCharCode(code);
	var AllowRegex  = /^[A-Za-z0-9\s\.,-]+$/g;
	if (AllowRegex.test(character)) return true;     
	return false; 
}

$(function() {

	$('#listado').DataTable({
		responsive: true,
		autoWidth: false,
		destroy: true,
		deferRender: true,
		ordering: false,
		searching: true,
		paging: true,
		"language": {
			"sProcessing": "Procesando...",
			"sLengthMenu": "Mostrar _MENU_ registros",
			"sZeroRecords": "No se encontraron resultados",
			"sEmptyTable": "Ningún dato disponible en esta tabla",
			"sInfo": "Mostrando del _START_ al _END_ de un total de _TOTAL_ registros",
			"sInfoEmpty": "Mostrand del 0 al 0 de un total de 0 registros",
			"sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
			"sInfoPostFix": "",
			"sSearch": "Buscar:",
			"sUrl": "",
			"sInfoThousands": ",",
			"sLoadingRecords": "Cargando...",
			"oPaginate": {
				"sFirst": "<span class='fa fa-angle-double-left'></span>",
				"sLast": "<span class='fa fa-angle-double-right'></span>",
				"sNext": "<span class='fa fa-angle-right'></span>",
				"sPrevious": "<span class='fa fa-angle-left'></span>"
			},
			"oAria": {
				"sSortAscending": ": Activar para ordenar la columna de manera ascendente",
				"sSortDescending": ": Activar para ordenar la columna de manera descendente"
			}
		},
		initComplete: function(settings, json) {
	
		}
	});
	
});

/** TABLA DINAMICA PARA NO REPETIR CODIGO */
const getDataTable = async (paging_p, searching_p, ordering_p, id_table, data_params, data_columns, data_columns_def, data_url) => {

	tblCate = $(id_table).DataTable({
		responsive: true,
		autoWidth: false,
		destroy: true,
		deferRender: true,
		ordering: ordering_p,
		searching: searching_p,
		paging: paging_p,
		"aaSorting": [], 
		"language": {
			"sProcessing": "Procesando...",
			"sLengthMenu": "Mostrar _MENU_ registros",
			"sZeroRecords": "No se encontraron resultados",
			"sEmptyTable": "Ningún dato disponible en esta tabla",
			"sInfo": "Mostrando del _START_ al _END_ de un total de _TOTAL_ registros",
			"sInfoEmpty": "Mostrand del 0 al 0 de un total de 0 registros",
			"sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
			"sInfoPostFix": "",
			"sSearch": "Buscar:",
			"sUrl": "",
			"sInfoThousands": ",",
			"sLoadingRecords": "Cargando...",
			"oPaginate": {
				"sFirst": "<span class='fa fa-angle-double-left'></span>",
				"sLast": "<span class='fa fa-angle-double-right'></span>",
				"sNext": "<span class='fa fa-angle-right'></span>",
				"sPrevious": "<span class='fa fa-angle-left'></span>"
			},
			"oAria": {
				"sSortAscending": ": Activar para ordenar la columna de manera ascendente",
				"sSortDescending": ": Activar para ordenar la columna de manera descendente"
			}
		},
		ajax: {
			url: data_url,
			type: 'POST',
			data: data_params,
			dataSrc: ""
		},
		columns: data_columns,
		columnDefs: data_columns_def,
		initComplete: function (settings, json) {

		},

	});


}


const SendDataJsonBuyForm = async (url, parameters, callback) => {
	try {

		const response = await fetch (url, {
			method: "POST",
			body: parameters
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

const SendDataJsonForm = async (url, parameters, callback) => {
	try {
		const response = await fetch (url, {
			method: "POST",
			body: parameters
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

let type_actions = {
	'labs': {
		'nuevo_lab': '/registro-de-laboratorio/',
		'edit_lab': '/actualizar-laboratorio/',
	},
	'type_ins': {
		'nuevo_tipo_insu': '/registro-de-tipos-de-insumos/',
		'edit_t_ins': '/actualizar-tipos-de-insumos/',
	},
	'almacen': {
		'nuevo_almacen': '/registro-de-almacen/',
		'edit_almacen': '/actualizar-almacen/',
	},
	'tipo_movi': {
		'nuevo_tipo_movi': '/agregar-tipos-movimientos/',
		'edit_tipo_movi': '/editar-tipos-movimientos/',
	},
	'zonas': {
		'nueva_zona': '/registro-de-zona/',
		'edit_zona': '/actualizar-zona/',
	},
	'productos': {
		'nuevo_producto': '/registro-de-productos/',
		'edit_producto': '/actualizar-producto/',
	},
	'user': {
		'cambiar_clave': '/actualizar-clave/',
		'nuevo_usuario': '/registrar-perfil/',
		'reset_password': '/reset-password/',
	},
	'landing': {
		'edit_landing': '/actualizar-landing/',
		'edit_producto': '/actualizar-producto/',
	}
}

let form_cambiar_clave = document.getElementById('form_cambiar_clave');
$(function () {

	// cambiar contraseña
	$('a[rel="cambiar_clave"]').on('click', function () {
        $('input[name="action_password"]').val('cambiar_clave');
		$('#id_modal_password').modal('show');
    });

	form_cambiar_clave.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_cambiar_clave);
		if ($('input[name="new_password"]').val() === $('input[name="new_password2"]').val() ) {
			await SendDataJsonForm(type_actions['user'][action_password.value], parameters, async () => {
				setTimeout(() => {
					$('#id_modal_password').modal('hide');   
					$("#form_cambiar_clave")[0].reset(); 
					window.location.replace('/ingresar/')
				}, 1000); // Espera 3 segundos antes de ejecutar el código dentro de setTimeout  
				
			});
		}else{
            notifier.show('Ocurrió un error!', 'Las contraseñas nueva no coinciden', 'danger', 4000);
        }
    });
});