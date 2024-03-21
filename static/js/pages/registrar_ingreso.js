let form_ingreso = document.getElementById('form_register');
let form_search = document.getElementById('search-input');

let vents = {
    items : {
        fecha: '',
        descripcion: '',
        tipo_ingreso: '',
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
        console.log('hola');
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
                {"data": "tipo_insumo.nombre"},
                {"data": "almacen.nombre"},
                {"data": "total_stock"},
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
                {"data": "lote"},
                {"data": "cantidad"},
                {"data": "f_vencimiento"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '<input type="text" value="'+ data +'"name="lote" class="form-control form-control-sm lote" required autocomplete="off">';
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {                        
                        return '<input type="number" value="'+ parseInt(data) +'" name="cantidad" class="form-control form-control-sm cantidad" required min="1" autocomplete="off">';
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '<input type="date" value="'+ data +'"name="f_vencimiento" class="form-control form-control-sm f_vencimiento" required autocomplete="off">';
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

$('#id_tipo_ingreso').select2({
    theme: 'bootstrap4',
    language: 'es',
    placeholder: 'Selecionar tipo de ingreso',
    allowClear: true
});

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
                        others: res
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
        data.cantidad = 1;
        data.nombre = data.text;
        data.lote = "";
        data.f_vencimiento = "";
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

    // asignar valor cantidad
    $('#detalle tbody').on('change keyup', '.cantidad', function () {
        let cantidad = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
            vents.items.det[tr.row].cantidad = parseInt(cantidad);
    });

    // asignar valor lote
    $('#detalle tbody').on('change keyup', '.lote', function () {
        let lote = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
            vents.items.det[tr.row].lote = lote;
    });

    // asignar valor f_vencimiento
    $('#detalle tbody').on('change keyup', '.f_vencimiento', function () {
        let f_vencimiento = $(this).val();
        var tr = tblCate.cell($(this).closest('td, li')).index();
            vents.items.det[tr.row].f_vencimiento = f_vencimiento;
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
            lote: "",
            f_vencimiento : "",
            nombre: productos.nombre,
            others: productos,
            cantidad: 1,
        }
        vents.add(data);
        $('#modal_search_product').modal('hide');   
    });
    // event submit
    $('#form_register').on('submit', async function (e) {
        e.preventDefault();
        
        if (vents.items.det.length === 0) {
            notifier.show('Ocurrio un error!', 'Debe al menos tener un producto en el ingreso', 'danger', '', 4000);
            return false;
        }
        vents.items.descripcion = $('textarea[name="descripcion"]').val();
        vents.items.fecha = $('input[name="fecha"]').val();
        vents.items.tipo_ingreso = $('select[name="tipo_ingreso"]').val();
        // return false;
        var parameters = new FormData();
        parameters.append('vents', JSON.stringify(vents.items));
    
        btn_submit.disabled = true;
        console.log(vents.items);
        await SendDataJsonBuyForm(window.location.pathname, parameters, function () {
            window.location.replace('/listado-de-ingresos/');
        })
    });
});