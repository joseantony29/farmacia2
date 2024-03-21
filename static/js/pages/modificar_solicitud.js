let form_ingreso = document.getElementById('form_register');
let form_search = document.getElementById('search-input');

let vents = {
    items : {
        descripcion: '',
        beneficiado: '',
        perfil:'',
        recipe: '',
        estado:'',
        det: []
    },
    get_ids: function () {
        var ids =  [];
        $.each(this.items.det, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    add: function (item) {
        this.items.det.push(item);
        this.list()
    },
    search_productos: async function () {
        /** PRODUCT LIST **/
        await getDataTable(
            // paging
            true,
            // searching
            true,
            // ordering
            true,
            '#id_datatable_productos',
            {
                'action': 'search_productos_table',
                'ids': JSON.stringify(vents.get_ids()),
            },
            [
                {"data": "nombre"},
                {"data": "id"},
            ],
            [
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="#" rel="select_product" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" title="Seleccionar producto"><i class="fa fa-hand-o-up"></i></a>';
                        return buttons
                    }
                },
            ],
            '/buscar-productos/'
        );
    },
    list: function () {
        
        tblCate = $('#detalle').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering:  false,
            searching: false,
            paging: false,
            "language": {
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "Ningún dato disponible en esta tabla",
                "sInfo": "Mostrando _START_ al _END_ de un total de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando 0 al 0 de un total de 0 registros",
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
            data: this.items.det,
            columns: [
                {"data": "nombre"},
                {"data": "cantidad"},
                {"data": "cantidad_entregada"},
                {"data": "total_stock"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return data;
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {                        
                        return '<input type="number" value="'+ parseInt(data) +'" name="cantidad" class="form-control form-control-sm cantidad" required min="1" readonly autocomplete="off">';
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {
                        let total_stock = row.total_stock
                        let cantidad = row.cantidad;
                        if (cantidad > total_stock) {
                            return '<input type="number" value="'+ parseInt(data) +'" name="cantidad_entregada" class="form-control form-control-sm cantidad_entregada" required min="0" max="'+ parseInt(total_stock) +'" autocomplete="off">';
                        } else{
                            return '<input type="number" value="'+ parseInt(data) +'" name="cantidad_entregada" class="form-control form-control-sm cantidad_entregada" required min="0" max="'+ parseInt(cantidad) +'" autocomplete="off">';
                        }                    
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return data;
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        buttons = '<a href="#" rel="delete" class="btn btn-icon btn-danger"><i class="fa fa-trash"></i></a> ';                       
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });

    },
};

$('#id_estado').select2({
    theme: 'bootstrap4',
    language: 'es',
    placeholder: 'Selecionar el estado',
    allowClear: true
});

let estados_permisos = {
    'ON':{
        'AD': [
            { 'id':'PR', 'text': 'En Proceso' },
            { 'id':'AP', 'text': 'Aprobado' },
            { 'id':'RE', 'text': 'Rechazado' },
        ],
        'AL': [
            { 'id':'EE', 'text': 'En Espera de Entrega' },
            { 'id':'AP', 'text': 'Aprobado' },
        ]
    },
    'PR':{
        'AD': [
            { 'id':'PR', 'text': 'En Proceso' },
            { 'id':'AP', 'text': 'Aprobado' },
            { 'id':'RE', 'text': 'Rechazado' },
        ],
        'AL': [
            { 'id':'EE', 'text': 'En Espera de Entrega' },
            { 'id':'AP', 'text': 'Aprobado' },
            { 'id':'RE', 'text': 'Rechazado' },
        ]
    }
}

let select2 = $('#id_estado');
let opcionesActuales = select2.find('option');
let tipo_solicitud = document.getElementById('tipo_solicitud');
let rol = document.getElementById('rol'); // Asegúrate de que este valor sea válido y exista en estados_permisos
tipo_solicitud = String(tipo_solicitud.value)
rol = String(rol.value)
// Verificar si el rol es válido y si tiene opciones permitidas
if (estados_permisos[tipo_solicitud][rol] && Array.isArray(estados_permisos[tipo_solicitud][rol])) {
    // Obtener la opción seleccionada por defecto
    let opcionSeleccionada = select2.val();

    // Iterar sobre las opciones actuales
    opcionesActuales.each(function() {
        var opcionActual = $(this);
        var idActual = opcionActual.val();
        var textoActual = opcionActual.text();

        // Verificar si la opción actual está en el listado permitido y no es la seleccionada por defecto
        var estaPermitida = estados_permisos[tipo_solicitud][rol].some(function(opcionPermitida) {
            return opcionPermitida.id === idActual && opcionPermitida.text === textoActual;
        });

        // Si la opción actual no está en el listado permitido y no es la seleccionada por defecto, eliminarla
        if (!estaPermitida && idActual !== opcionSeleccionada) {
            opcionActual.remove();
        }
    });

    // Asegurarse de que las opciones permitidas no se dupliquen
    estados_permisos[tipo_solicitud][rol].forEach(function(opcionPermitida) {
        if (!opcionesActuales.filter(`[value="${opcionPermitida.id}"]`).length) {
            // Crear y agregar la nueva opción si no existe
            var newOption = new Option(opcionPermitida.text, opcionPermitida.id, false, false);
            select2.append(newOption);
        }
    });

    // Actualizar el Select2 para reflejar los cambios
    select2.trigger('change');
} else {
    console.error('El rol especificado no es válido o no tiene opciones permitidas.');
}

// FORMATTING WHEN DISPLAYING THE RESULT OF THE SELECT
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    let option = $(
        '<div class="col text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b style="color:#000000">Nombre:</b> <b style="color:#000000">' + repo.text+ '</b><br>' +
        '<b style="color:#000000">Codigo:</b> <b style="color:#000000">' + repo.id + '</b><br>' +
        '<b style="color:#000000">Disponibilidad:</b> <b style="color:#000000">' + repo.others.total_stock + '</b><br>' +
        '</p>' +
        '</div>');

    return option;
}

$(function () {

    vents.list()

    // auto complete search
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            type: "POST", 
            url: '/buscar-productos/',
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: "search_productos",
                    ids: JSON.stringify(vents.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                var results = [];
              
                $.each(data, function (index, res) {
                    results.push({
                        id: res.id,
                        text: res.nombre,
                        others:res,
                    });
                });
    
                return {
                    results: results
                };
            },
            cache: true

        },
        placeholder: 'Buscar producto ...', 
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cantidad = 0;
        data.nombre = data.text;
        data.cantidad_entregada = 0
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

    // asignar valor cantidad
    $('#detalle tbody').on('change keyup', '.cantidad', function () {
        let cantidad = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
            vents.items.det[tr.row].cantidad = parseInt(cantidad);
    });

    // asignar valor cantidad
    $('#detalle tbody').on('change keyup', '.cantidad_entregada', function () {
        let cantidad_entregada = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
            vents.items.det[tr.row].cantidad_entregada = parseInt(cantidad_entregada);
    });

    // delete individual element
    $('#detalle tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        vents.items.det.splice(tr.row, 1);
        vents.list();
        notifier.show('Exito!', 'Se ha eliminado correctamente', 'success', '', 4000);
    });
    /// remove all detail
    $('a[rel="btn_delete"]').on('click', function () {
        if (vents.items.det.length === 0) return false;
        vents.items.det = [];
        vents.list();
        notifier.show('Exito!', 'Se ha eliminado correctamente', 'success', '', 4000);
    });
    /** OPEN MODAL PRODUCT **/
    $('a[rel="open_modal_product"]').on('click', function () {
        vents.search_productos()
        $('#modal_search_product').modal('show');
    });
    // PRODUCT SELECT
    $('#id_datatable_productos tbody').on('click', 'a[rel="select_product"]', function () {
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var productos = tblCate.row(tr.row).data();
        let data = {
            id: productos.id,
            text: productos.nombre,
            nombre: productos.nombre,
            cantidad: 0,
            cantidad_entregada:0,
        }
        vents.add(data);
        $('#modal_search_product').modal('hide');   
    });

    $('.beneficiado').select2({
        placeholder: 'Seleccione el beneficiado',
        theme:'bootstrap4',
        language: "es",
        allowClear: true
    });

    /** OPEN MODAL BENEFICIADOS **/
    $('button[rel="open_modal_beneficiado"]').on('click', function () {
        $("#form_beneficiado")[0].reset();
        $('#modal_beneficiados').modal('show');
    });

    $('#form_beneficiado').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        SendDataJsonForm('/registrar-beneficiado-modal/', parameters, function () {
            $("#modal_beneficiados").modal('hide');

            var ci = $(".cedula").val();
            var nombre = $(".nombre").val();
            var apellido = $(".apellido").val();

            var data = {
                id: ci,
                text: ci,
                nombre: nombre,
                apellido: apellido,

            };
            var newOption = new Option(`${data.text }-${data.nombre}`, data.id, true, true);
            $('.beneficiado').append(newOption).trigger('change');
    
            $("#form_beneficiado")[0].reset();
            // $('.titular_modal').val(null).trigger('change');
            
        });    
    });

    // event submit
    $('#form_register').on('submit', async function (e) {
        e.preventDefault();
        
        if (vents.items.det.length === 0) {
            notifier.show('Ocurrio un error!', 'Debe al menos tener un producto en la solicitud', 'danger', '', 4000);
            return false;
        }

        var imagefield = document.getElementById("id_recipe");

        vents.items.descripcion = $('textarea[name="descripcion"]').val();
        vents.items.recipe = imagefield.files[0]
        vents.items.beneficiado = $('select[name="beneficiado"]').val();
        (tipo_solicitud == 'PR') ? vents.items.perfil = $('select[name="perfil"]').val(): '';
        vents.items.estado = $('select[name="estado"]').val();

        var parameters = new FormData();
        parameters.append('vents', JSON.stringify(vents.items));
        parameters.append('recipe', imagefield.files[0]);

        btn_submit.disabled = true;
        await SendDataJsonForm(window.location.pathname, parameters, function () {
            window.location.replace('/solictudes-de-medicamentos/');
        })
    });
});