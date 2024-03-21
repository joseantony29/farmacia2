let form_producto = document.getElementById('form_producto');
let user_rol = document.getElementById('user_rol');
user_rol = String(user_rol.value)
console.log(user_rol);
let getData = async () => {
    // PRODUCTO LIST
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#listado_productos',
        {
            'action': 'search_productos',
        },
        [
            {"data": "id"},
            {"data": "nombre"},
            {"data": "almacen.nombre"},
            {"data": "laboratorio.nombre"},
            {"data": "total_stock"},
            {"data": "id"},
        ],
        [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons;
                    if (!(user_rol == 'AT')) {
                        buttons = '<a href="#" rel="edit" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Editar producto"><i class="fa fa-edit"></i></a>';
                        buttons += '<a href="#" rel="detail" class="btn btn-icon btn-dark ml-2" data-bs-toggle="tooltip" data-bs-placement="top" title="Detalles de productos"><i class="fa fa-info"></i></a>';

                    } else {
                        buttons = '<a href="#" rel="detail" class="btn btn-icon btn-dark ml-2" data-bs-toggle="tooltip" data-bs-placement="top" title="Detalles de productos"><i class="fa fa-info"></i></a>';
                    }
                    return buttons
                }
            },
        ],
        '/listado-de-productos/'
    );

}


$( async function () {
    await getData();

	// PRODUCTO SEND FORM
	form_producto.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_producto);
        await SendDataJsonForm(type_actions['productos'][action.value], parameters, async () => {  
            await getData();
            $('#smallmodal').modal('hide');   
            $("#form_producto")[0].reset(); 
        });
    });

    // REGISTER PRODUCTO
    $('#btn_nuevo_producto').on('click', function () {
        $('#form_producto')[0].reset();
        $('input[name="action"]').val('nuevo_producto');
        $('#smallmodal').modal('show');
    });

    // EDITAR PRODUCTO
    $('#listado_productos tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_producto')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('edit_producto');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);
        $('select[name="almacen"]').val(data.almacen.id);
        $('select[name="tipo_insumo"]').val(data.tipo_insumo.id);
        $('select[name="laboratorio"]').val(data.laboratorio.id);
        $('select[name="if_expire_date"]').val(data.if_expire_date);
        $('input[name="stock_minimo"]').val(data.stock_minimo);
        $('input[name="total_stock"]').val(data.total_stock);

        $('#smallmodal').modal('show');
    });

    // detalles de productos
    $('#listado_productos tbody').on('click', 'a[rel="detail"]', function () {
        $('#form_producto')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        window.location.replace(`/detalle-de-producto/${data.id}`)
    });
    
});