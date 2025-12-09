# 1. Crear la factura (Draft)
invoice = env['account.move'].create({
    'move_type': 'out_invoice',
    'partner_id': partner_id,
    'invoice_line_ids': [(0, 0, {
        'product_id': product_id,
        'price_unit': base_amount,
        'tax_ids': [(6, 0, [iva_21_id, perc_santafe_id])] # [cite: 497]
    })]
})

# 2. Buscar la línea de impuesto específica para "pisar" el valor
# [cite: 487, 501, 502]
tax_line = env['account.move.line'].search([
    ('move_id', '=', invoice.id),
    ('tax_line_id', '=', perc_santafe_id)
], limit=1)

if tax_line:
    # Escribimos el balance para evitar errores de redondeo [cite: 468, 513]
    # Odoo ajustará debit/credit automáticamente según el signo
    tax_line.write({
        'debit': amount_pos if amount_pos > 0 else 0,
        'credit': abs(amount_pos) if amount_pos < 0 else 0
    })
    
# 3. Validar / Postear la factura
invoice.action_post()