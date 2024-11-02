class EstadoEnvio:
    PENDIENTE = 'pendiente'
    EN_TRANSITO = 'en_transito'
    ENTREGADO = 'entregado'
    CANCELADO = 'cancelado'

    CHOICES = [
        (PENDIENTE, 'Pendiente'),
        (EN_TRANSITO, 'En Tránsito'),
        (ENTREGADO, 'Entregado'),
        (CANCELADO, 'Cancelado'),
    ]
