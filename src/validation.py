def validate_data(df):
    diff_canal = (df['salon_ventas'] + df['canales_on_line']
                  - df['ventas_totales_canal_venta']).abs().max()

    diff_pago = (df['efectivo'] + df['tarjetas_debito'] +
                 df['tarjetas_credito'] + df['otros_medios']
                 - df['ventas_totales_medio_pago']).abs().max()

    if diff_canal >= 1:
        raise ValueError("Inconsistencia en canal de venta")

    if diff_pago >= 1:
        raise ValueError("Inconsistencia en medios de pago")
