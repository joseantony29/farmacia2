var $ = jQuery.noConflict();

jQuery(document).ready(function($) {

	"use strict";

	[].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
		new SelectFx(el);
	});

	jQuery('.selectpicker').selectpicker;


	

	$('.search-trigger').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').addClass('open');
	});

	$('.search-close').on('click', function(event) {
		event.preventDefault();
		event.stopPropagation();
		$('.search-trigger').parent('.header-left').removeClass('open');
	});

	$('.equal-height').matchHeight({
		property: 'max-height'
	});

	// var chartsheight = $('.flotRealtime2').height();
	// $('.traffic-chart').css('height', chartsheight-122);


	// Counter Number
	$('.count').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 3000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});


	 
	 
	// Menu Trigger
	$('#menuToggle').on('click', function(event) {
		var windowWidth = $(window).width();   		 
		if (windowWidth<1010) { 
			$('body').removeClass('open'); 
			if (windowWidth<760){ 
				$('#left-panel').slideToggle(); 
			} else {
				$('#left-panel').toggleClass('open-menu');  
			} 
		} else {
			$('body').toggleClass('open');
			$('#left-panel').removeClass('open-menu');  
		} 
			 
	}); 

	 
	$(".menu-item-has-children.dropdown").each(function() {
		$(this).on('click', function() {
			var $temp_text = $(this).children('.dropdown-toggle').html();
			$(this).children('.sub-menu').prepend('<li class="subtitle">' + $temp_text + '</li>'); 
		});
	});


	// Load Resize 
	$(window).on("load resize", function(event) { 
		var windowWidth = $(window).width();  		 
		if (windowWidth<1010) {
			$('body').addClass('small-device'); 
		} else {
			$('body').removeClass('small-device');  
		} 
		
	});
  
 
});
function abrir_modal_edicion(url){
	$('#edicion').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_edicion(){
	$('#edicion').modal('hide');
}
function abrir_modal_eliminacion(url){
	$('#eliminacion').load(url, function(){
		$(this).modal('show');
	});
}
function cerrar_modal_eliminacion(){
	$('#eliminacion').modal('hide');
}
function activarBoton(){
	if($('#boton_creacion').prop('disabled')){
		$('#boton_creacion').prop('disabled', false);
	}
	else{
		$('#boton_creacion').prop('disabled', true);
	}
}
function notificacionError(mensaje){
	Swal.fire({
		title: 'Error!',
		text: mensaje,
		icon: 'error'
	})
}
function notificacionSuccessCreacion(mensaje){
	Swal.fire({
		title: 'Registro Valido!',
		text: mensaje,
		icon: 'success'
	})
}
function notificacionSuccessEdicion(mensaje){
	Swal.fire({
		title: 'Edición Valida!',
		text: mensaje,
		icon: 'success'
	})
}

function notificacionSuccessEliminacion(mensaje){
	Swal.fire({
		title: 'Eliminación Valida!',
		text: mensaje,
		icon: 'success'
	})
}
document.addEventListener("DOMContentLoaded", function() {

    function addEventListeners(selector, title) {
        var icono = document.querySelector(selector);
        if (icono) {
            var enlace = icono.parentNode;

            icono.addEventListener("mouseover", function() {
                enlace.title = title;
                icono.classList.add("hover");
            });

            icono.addEventListener("mouseout", function() {
                enlace.title = "";
                icono.classList.remove("hover");
            });
        }
    }

    addEventListeners(".fa-plus", "Añadir");
    addEventListeners(".fa-pencil-square-o", "Editar");
    addEventListeners(".fa-times", "Eliminar");
    addEventListeners(".fa-lock", "Cambiar Contraseña");
});


function soloLetras(evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    if ((charCode < 65 || charCode > 90) && (charCode < 97 || charCode > 122) && (charCode !== 32) && (charCode !== 209) && (charCode !== 241)) {
        return false;
    }
    return true;
}

function soloNumeros(evt) {
	var charCode = (evt.which) ? evt.which : event.keyCode;
	if (charCode > 31 && (charCode < 48 || charCode > 57)) {
		return false;
	}
	return true;
}