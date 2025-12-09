## example
# mapeos
product_id = 1 # almacenan los ids de los productos
partner_id = 47 # almacenan los ids de los clientes en starpos
company_id = 6 # almacenan los ids de las compañias en starpos
# datos de la venta
quantity = 1.0
date = '2024-06-01'
# opcionales
# no hay ningún campo nativo de odoo que nos permita vinculad picking y factura, la sugerencia es usar el campo origin
origin = 'Starpos reference 1' # podria usarse para referencia de starpos

picking_vals_1 = {
    'partner_id': partner_id,
    'origin': origin,
    'move_ids': [(0, 0, {
        'product_id': product_id,
        'product_uom_qty': quantity,
    })],
}
picking_vals_2 = {
    'partner_id': partner_id,
    'origin': origin,
    'move_ids': [(0, 0, {
        'product_id': product_id,
        'product_uom_qty': quantity,
    })],
}
pickings = env['stock.picking'].with_company(company_id).with_context(restricted_picking_type_code='outgoing').create([picking_vals_1, picking_vals_2])
# este método va a funcionar bien si los productos tiene stock o son consumibles. Segun el caso podemos ver de complejizar
pickings.button_validate()

