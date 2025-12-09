
## example
# mapeos
product_id = 1 # almacenan los ids de los productos
tax_ids = [193] # mapeamos en bases de datos IVA de starpos a IVA en odoo
partner_id = 47 # almacenan los ids de los clientes en starpos
company_id = 6 # almacenan los ids de las compañias en starpos
sale_journal_id = 35 # mapeamos en bases de datos puntos de venta de starpos a diarios de odoo
bank_journal_id = 40 # almacenan los ids de los diarios bancarios en starpos
cash_journal_id = 58 # almacenan los ids de los diarios bancarios en starpos
doc_type_FA_id = 1 # mapeamos en bases de datos tipos de comprobantes de starpos a tipos de comprobantes en odoo
doc_type_FB_id = 6 # mapeamos en bases de datos tipos de comprobantes de starpos a tipos de comprobantes en odoo
doc_type_NCB_id = 8 # mapeamos en bases de datos tipos de comprobantes de starpos a tipos de comprobantes en odoo
# datos de la venta
invoice_number_1 = '0002-00002234'
invoice_number_2 = '002-00002235'
refund_number_1 = '0002-00002236'
quantity = 1.0
price_unit = 123
date = '2024-06-01'
# IMPORTANTE: este dato "l10n_ar_afip_auth_code" hace que públicar la factura
# NO se comunique con ARCA (por más que el diari esté configurado como electrínico)
l10n_ar_afip_auth_code = '68448767638166'
l10n_ar_afip_auth_code_due = '2024-06-01'
l10n_ar_afip_result = 'A' # ('A', 'Accepted in ARCA'), ('O', 'Accepted in ARCA with Observations')
# opcionales
customer_ref = 'CUST-001' # referencia genérica de la venta
invoice_origin = 'Starpos reference 1' # podria usarse para referencia de starpos


#############################################
# Facturas (account.move)
# Lineas de factura (account.move.line)
#############################################
vals1 = {
    'partner_id': partner_id,
    'l10n_latam_document_type_id': doc_type_FA_id,
    'l10n_latam_document_number': invoice_number_1,
    'company_id': company_id,
    'journal_id': sale_journal_id,
    'invoice_date': date,
    'move_type': 'out_invoice',
    'ref': customer_ref,
    'invoice_origin': invoice_origin,
    'l10n_ar_afip_auth_mode': 'CAE',
    'l10n_ar_afip_auth_code': l10n_ar_afip_auth_code,
    'l10n_ar_afip_auth_code_due': l10n_ar_afip_auth_code_due,
    'l10n_ar_afip_result': l10n_ar_afip_result,
    'invoice_line_ids': [(0, 0, {
        'product_id': product_id,
        'quantity': quantity,
        'price_unit': price_unit,
        'tax_ids': [(6, 0, tax_ids)],
        'move_type': 'out_invoice',
    })]
}
vals2 = {
    'partner_id': partner_id,
    'l10n_latam_document_type_id': doc_type_FB_id,
    'l10n_latam_document_number': invoice_number_2,
    'company_id': company_id,
    'journal_id': sale_journal_id,
    'invoice_date': date,
    'move_type': 'out_invoice',
    'ref': customer_ref,
    'invoice_origin': invoice_origin,
    'l10n_ar_afip_auth_mode': 'CAE',
    'l10n_ar_afip_auth_code': l10n_ar_afip_auth_code,
    'l10n_ar_afip_auth_code_due': l10n_ar_afip_auth_code_due,
    'l10n_ar_afip_result': l10n_ar_afip_result,
    'invoice_line_ids': [(0, 0, {
        'product_id': product_id,
        'quantity': quantity,
        'price_unit': price_unit,
        'tax_ids': [(6, 0, tax_ids)],
        'move_type': 'out_invoice',
    })]
}

# en este ejemplo estamos creando dos facturas de una y pagando ambas con dos pagos
# solo tiene sentido si ambas facturas son de mismo cliente
# es simplemente para mostrar que se podrían mandar varios comprobantes en una llamada
invoices = env['account.move'].create([vals1, vals2])
invoices.action_post()


payments = self.env['account.payment.register'].with_context(
    active_model='account.move',
    active_ids=invoices.ids
).create([{
    'amount': 148.83,
    'journal_id': bank_journal_id,
}, {
    'amount': 148.83,
    'journal_id': cash_journal_id,
}])

[payment.action_create_payments() for payment in payments]


## RECTIFICATIVA
refund1 = {
    'partner_id': partner_id,
    'l10n_latam_document_type_id': doc_type_NCB_id,
    'l10n_latam_document_number': refund_number_1,
    'reversed_entry_id': invoices[0].id,  # opcional, ide de la factura que se rectificó, id de la factura a la que se le hace la nota de credito
    'company_id': company_id,
    'journal_id': sale_journal_id,
    'invoice_date': date,
    'move_type': 'out_refund',
    'ref': customer_ref,
    'invoice_origin': invoice_origin,
    'l10n_ar_afip_auth_mode': 'CAE',
    'l10n_ar_afip_auth_code': l10n_ar_afip_auth_code,
    'l10n_ar_afip_auth_code_due': l10n_ar_afip_auth_code_due,
    'l10n_ar_afip_result': l10n_ar_afip_result,
    'invoice_line_ids': [(0, 0, {
        'product_id': product_id,
        'quantity': quantity,
        'price_unit': price_unit,
        'tax_ids': [(6, 0, tax_ids)],
        'move_type': 'out_invoice',
    })]
}
refund = env['account.move'].create([refund1])
# IMPORTANTE: al publicar un refund, si el mismo está vinculado a una reversed_entry_id, odoo va a intentar conciliar ambas deudas
refund.action_post()
